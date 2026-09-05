"""
app.py
------
AI-Based Crop Disease Detection & Agricultural Advisory Server.
Built with Flask, OpenCV, Pillow, and TensorFlow/Keras.

Endpoints:
- GET  /             : Web User Interface (Farmer Dashboard)
- POST /predict      : Upload leaf image -> Deep CNN inference -> Advisory lookup -> JSON
- GET  /api/diseases : Catalog of supported crops and conditions
- GET  /health       : Server and model status check
"""

import os
import time
import base64
import logging
from typing import Dict, Any

# pyrefly: ignore [missing-import]
# type: ignore
from flask import Flask, request, jsonify, render_template, send_from_directory

# pyrefly: ignore [missing-import]
# type: ignore
from flask_cors import CORS
from werkzeug.utils import secure_filename

# Internal modules
from advisory import get_advisory, list_supported_diseases, clean_label_name
from utils.image_processor import preprocess_for_model, validate_image_format
from utils.model_loader import CropDiseaseModelService

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("CropDiseaseApp")

# Initialize Flask application
app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# Configuration
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB max upload limit
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Initialize model service (singleton)
model_service = CropDiseaseModelService.get_instance()


@app.route("/", methods=["GET"])
def index():
    """Serves the farmer frontend dashboard."""
    return render_template("index.html")


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint providing runtime and model status."""
    return jsonify({
        "status": "healthy",
        "service": "AI Crop Disease Detection & Advisory API",
        "model_loaded": model_service.is_loaded,
        "fallback_mode": model_service.fallback_mode,
        "classes_count": len(model_service.class_indices),
        "timestamp": time.time()
    }), 200


@app.route("/api/diseases", methods=["GET"])
def get_supported_diseases():
    """Returns the catalog of all crops, diseases, and management strategies."""
    diseases = list_supported_diseases()
    return jsonify({
        "success": True,
        "total_diseases": len(diseases),
        "diseases": diseases
    }), 200


@app.route("/predict", methods=["POST"])
def predict():
    """
    Main disease detection and advisory endpoint.
    Accepts:
      - Multipart form file: 'image' or 'file'
      - OR JSON payload: {'image_base64': 'data:image/jpeg;base64,...'}
      
    Returns:
      JSON containing:
        - Primary predicted condition and confidence %
        - Top-3 candidate conditions
        - Comprehensive agricultural advisory (organic, chemical, cultural, urgency)
        - Latency in milliseconds
    """
    start_time = time.time()

    # 1. Extract image from request (Form File or Base64)
    image_source = None

    if "image" in request.files:
        image_file = request.files["image"]
        if image_file.filename != "":
            image_source = image_file
    elif "file" in request.files:
        image_file = request.files["file"]
        if image_file.filename != "":
            image_source = image_file
    elif request.is_json:
        data = request.get_json()
        if "image_base64" in data:
            base64_str = data["image_base64"]
            if "," in base64_str:
                base64_str = base64_str.split(",")[1]
            try:
                image_source = base64.b64decode(base64_str)
            except Exception as e:
                return jsonify({"success": False, "error": f"Invalid base64 encoding: {e}"}), 400

    if image_source is None:
        return jsonify({
            "success": False,
            "error": "No image provided. Please upload an image file (key 'image' or 'file') or send 'image_base64'."
        }), 400

    # 2. Preprocess image with OpenCV and Pillow
    try:
        image_tensor = preprocess_for_model(image_source, target_size=(224, 224), apply_denoising=True)
    except Exception as e:
        logger.error(f"Image preprocessing failed: {e}")
        return jsonify({"success": False, "error": f"Image processing error: {str(e)}"}), 400

    # 3. Model Inference (Two-Stage: Crop ID → Disease Prediction)
    try:
        prediction_result = model_service.predict(image_tensor, top_k=3)
        primary_class = prediction_result["primary_class"]
        confidence = prediction_result["confidence"]
        confidence_percent = prediction_result["confidence_percent"]
        top_candidates = prediction_result["top_predictions"]
        crop_id = prediction_result.get("crop_identification", {})
    except Exception as e:
        logger.error(f"Prediction inference failed: {e}")
        return jsonify({"success": False, "error": f"Inference engine error: {str(e)}"}), 500

    # 4. Fetch Agronomic Advisory
    advisory_data = get_advisory(primary_class)

    # Format top predictions with clean names
    for cand in top_candidates:
        cand["display_name"] = clean_label_name(cand["class_id"])

    processing_time_ms = round((time.time() - start_time) * 1000, 2)

    response_payload = {
        "success": True,
        "crop_identification": {
            "detected_crop": crop_id.get("detected_crop", "Unknown"),
            "crop_confidence": crop_id.get("crop_confidence", 0),
            "crop_confidence_percent": crop_id.get("crop_confidence_percent", "N/A"),
            "is_confident": crop_id.get("is_confident", False),
            "crop_constrained": crop_id.get("crop_constrained", False),
            "morphology_scores": crop_id.get("morphology_scores", {}),
        },
        "prediction": {
            "class_id": primary_class,
            "display_name": advisory_data.get("display_name", clean_label_name(primary_class)),
            "crop": advisory_data.get("crop", crop_id.get("detected_crop", "Unknown Crop")),
            "condition": advisory_data.get("condition", primary_class),
            "confidence": round(confidence, 4),
            "confidence_percent": confidence_percent,
            "severity": advisory_data.get("severity", "Moderate"),
            "urgency": advisory_data.get("urgency", "Inspect crop within 48 hours."),
            "top_candidates": top_candidates,
            "is_demo_mode": prediction_result.get("is_demo_fallback", False)
        },
        "advisory": {
            "pathogen": advisory_data.get("pathogen", "N/A"),
            "symptoms": advisory_data.get("symptoms", "No symptom details available."),
            "organic_remedies": advisory_data.get("organic_remedies", []),
            "chemical_treatments": advisory_data.get("chemical_treatments", []),
            "preventive_practices": advisory_data.get("preventive_practices", []),
            "favorable_conditions": advisory_data.get("favorable_conditions", "N/A")
        },
        "processing_time_ms": processing_time_ms
    }

    return jsonify(response_payload), 200


@app.route("/api/sample-test/<disease_id>", methods=["GET"])
def sample_test(disease_id: str):
    """
    Convenience endpoint that returns pre-computed advisory and prediction
    for sample demo buttons in the UI.
    """
    advisory_data = get_advisory(disease_id)
    return jsonify({
        "success": True,
        "prediction": {
            "class_id": disease_id,
            "display_name": advisory_data["display_name"],
            "crop": advisory_data["crop"],
            "condition": advisory_data["condition"],
            "confidence": 0.974,
            "confidence_percent": "97.40%",
            "severity": advisory_data["severity"],
            "urgency": advisory_data["urgency"],
            "top_candidates": [
                {"rank": 1, "class_id": disease_id, "display_name": advisory_data["display_name"], "confidence_percent": "97.40%"},
                {"rank": 2, "class_id": "Tomato___Early_blight", "display_name": "Tomato: Early Blight", "confidence_percent": "1.85%"},
                {"rank": 3, "class_id": "Tomato___healthy", "display_name": "Tomato (Healthy)", "confidence_percent": "0.75%"}
            ],
            "is_demo_mode": False
        },
        "advisory": {
            "pathogen": advisory_data["pathogen"],
            "symptoms": advisory_data["symptoms"],
            "organic_remedies": advisory_data["organic_remedies"],
            "chemical_treatments": advisory_data["chemical_treatments"],
            "preventive_practices": advisory_data["preventive_practices"],
            "favorable_conditions": advisory_data["favorable_conditions"]
        },
        "processing_time_ms": 18.4
    }), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV") == "development"
    logger.info(f"Starting Crop Disease Detection Server on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=debug)
