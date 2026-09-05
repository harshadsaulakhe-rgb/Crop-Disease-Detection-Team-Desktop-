# 🌿 AgriCure AI: Crop Disease Detection & Advisory System

An end-to-end AgriTech platform that combines **Deep Convolutional Neural Networks (CNN)** with an **Actionable Agronomic Advisory Engine** to help farmers detect crop leaf pathologies in seconds and receive immediate organic and chemical remediation plans.

---

## 📌 Features

- 🔬 **Deep CNN Pathology Model**: 4-Block Convolutional Neural Network built with Keras & TensorFlow trained on the **PlantVillage Dataset**.
- 📸 **Multi-Source Image Pipeline**: Handles drag-and-drop file uploads, mobile camera snapshots, and automatic EXIF orientation correction using **Pillow** and **OpenCV**.
- 📋 **Comprehensive Agricultural Advisory**: Maps 20+ disease categories to actionable scientific recommendations:
  - 🌿 **Organic & Biological Solutions** (Neem oil, *Trichoderma*, copper soap, bio-fungicides).
  - 🧪 **Chemical Treatments** (Mancozeb, Chlorothalonil, Azoxystrobin, dosage, safety precautions).
  - 🛡️ **Preventive Cultural Practices** (Drip irrigation, canopy pruning, sanitation).
  - 🚨 **Emergency 24-48 Hour Protocol** (Urgency alerts).
- 🔊 **Voice Advisory for Farmers (TTS)**: Built-in text-to-speech audio reader allowing field workers to listen to instructions in real time.
- ⚡ **Instant Testing Demos**: Built-in 1-click test chips for Tomato Late Blight, Potato Early Blight, Corn Rust, and Apple Scab.
- 📱 **Modern Responsive UI**: Clean, glassmorphic emerald theme optimized for smartphones, tablets, and field conditions.

---

## 🏗️ System Architecture

```
   +----------------------------------------------------------------+
   |                     Farmer Web Interface                       |
   |           (HTML5, Modern CSS Glassmorphism, JS)                |
   |   - Drag & Drop / Camera Capture / Quick Preset Chips          |
   |   - Confidence Meter & Severity Badge                          |
   |   - Tabbed Advisory Dashboard + Voice Audio Reader             |
   +-------------------------------+--------------------------------+
                                   |
                     HTTP POST /predict (Multipart Form)
                                   |
   +-------------------------------v--------------------------------+
   |                        Flask API Server                        |
   |                           (app.py)                             |
   +-------------------------------+--------------------------------+
                                   |
                +------------------+------------------+
                |                                     |
   +------------v-------------+          +------------v-------------+
   |  Image Preprocessing     |          |      Advisory Engine     |
   |   (OpenCV & Pillow)      |          |       (advisory.py)      |
   | - EXIF Auto-Transpose    |          | - Organic Remedies       |
   | - RGB Normalization      |          | - Chemical Fungicides    |
   | - Resize to 224x224      |          | - Preventive Practices   |
   +------------+-------------+          | - Urgency & Pathogens    |
                |                        +------------+-------------+
   +------------v-------------+                       |
   |    Deep CNN Inference    |                       |
   |   (TensorFlow / Keras)   |                       |
   |  - disease_model.h5      |                       |
   |  - Softmax Top-3 Ranking |                       |
   +------------+-------------+                       |
                |                                     |
                +------------------+------------------+
                                   |
                     JSON Response with Advisory
                                   v
   +----------------------------------------------------------------+
   |                 Rendered Farmer Advisory UI                    |
   +----------------------------------------------------------------+
```

---

## 📁 Directory Structure

```text
crop-disease-detection/
├── app.py                      # Flask backend server with /predict API and UI serving
├── train.py                    # Complete CNN training script with data augmentation
├── advisory.py                 # Agricultural advisory knowledge base & query logic
├── requirements.txt            # Python package dependencies
├── README.md                   # Project documentation & setup instructions
├── .gitignore                  # Git ignore file for models, caches, and uploads
├── utils/
│   ├── __init__.py
│   ├── image_processor.py      # OpenCV & Pillow preprocessing pipeline
│   └── model_loader.py         # Keras model loader, inference & top-k ranking
├── templates/
│   └── index.html              # Farmer-centric responsive single-page web app
├── static/
│   ├── css/
│   │   └── style.css           # Modern AgriTech glassmorphic styling
│   └── js/
│       └── app.js              # Fetch API handler, camera stream, audio reader
├── models/
│   ├── class_indices.json      # Mapping of 23 PlantVillage disease categories
│   └── disease_model.h5        # Trained Keras CNN model weights (generated)
└── data/
    ├── README.md               # Dataset organization instructions
    └── PlantVillage/           # PlantVillage dataset directory
```

---

## 🚀 Step-by-Step Local Setup Guide

### 1. Prerequisites
Make sure Python 3.9, 3.10, or 3.11 is installed on your computer.
Check with:
```bash
python --version
```
*(If Python is not installed, download it from [python.org](https://www.python.org/downloads/) and ensure **"Add Python to PATH"** is checked during installation).*

---

### 2. Clone or Navigate to Project Directory
```bash
cd "e:/basic hackthon"
```

---

### 3. Create & Activate Virtual Environment

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
*(If you see an execution policy error, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first).*

**On Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**On Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 4. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 5. Initialize or Train the CNN Model

#### Option A: Instant Test Model (No 2GB download required)
To test the web app and API immediately without waiting to download the full dataset:
```bash
python train.py --generate-sample-model
```

#### Option B: Full Training with PlantVillage Dataset
1. Download the [PlantVillage Dataset on Kaggle](https://www.kaggle.com/datasets/emmarex/plantdisease).
2. Extract the folders into `data/PlantVillage/`.
3. Run the training script:
```bash
python train.py --data data/PlantVillage --epochs 25 --batch-size 32
```
The script will:
- Augment images with random rotations, shears, shifts, and zooms.
- Train the 4-stage CNN model with `EarlyStopping` and `ReduceLROnPlateau`.
- Save the best weights as `models/disease_model.h5`.
- Save accuracy and loss curves to `models/training_history.png`.

---

### 6. Run the Web Application
```bash
python app.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 📡 API Reference

### `POST /predict`
Uploads a crop leaf image for disease diagnosis and advisory lookup.

**Request:**
- Content-Type: `multipart/form-data`
- Body Parameter: `image` (binary file) or `file` (binary file)
- *Alternative:* JSON payload with `{"image_base64": "data:image/jpeg;base64,..."}`

**Sample cURL Request:**
```bash
curl -X POST http://127.0.0.1:5000/predict \
     -F "image=@sample_leaf.jpg"
```

**Sample JSON Response:**
```json
{
  "success": true,
  "prediction": {
    "class_id": "Tomato___Late_blight",
    "display_name": "Tomato: Late Blight",
    "crop": "Tomato",
    "condition": "Late Blight",
    "confidence": 0.9842,
    "confidence_percent": "98.42%",
    "severity": "Critical",
    "urgency": "CRITICAL EMERGENCY: Spreads aggressively across the whole crop in 3-5 days. Spray within 24 hours.",
    "top_candidates": [
      { "rank": 1, "class_id": "Tomato___Late_blight", "display_name": "Tomato: Late Blight", "confidence_percent": "98.42%" },
      { "rank": 2, "class_id": "Tomato___Early_blight", "display_name": "Tomato: Early Blight", "confidence_percent": "1.20%" },
      { "rank": 3, "class_id": "Tomato___healthy", "display_name": "Tomato (Healthy)", "confidence_percent": "0.38%" }
    ]
  },
  "advisory": {
    "pathogen": "Oomycete (Phytophthora infestans)",
    "symptoms": "Large, irregular greasy water-soaked pale-green to brown lesions; white cottony fungal growth on underside under humid conditions.",
    "organic_remedies": [
      "Bordeaux mixture (1:1:100) or Copper Hydroxide spray at 4-5 day intervals.",
      "Immediate removal and deep burial of heavily infected plants."
    ],
    "chemical_treatments": [
      "Metalaxyl 8% + Mancozeb 64% WP (Ridomil Gold): 2.5 g per liter of water.",
      "Cymoxanil 8% + Mancozeb 64% WP (Curzate): 2.5 g per liter of water."
    ],
    "preventive_practices": [
      "Maintain wide plant spacing (60 x 45 cm minimum) to promote rapid leaf drying.",
      "Never plant tomatoes adjacent to potato fields."
    ],
    "favorable_conditions": "Cool (15-22°C), wet, foggy weather with high humidity (>90%)."
  },
  "processing_time_ms": 38.6
}
```

---

### `GET /api/diseases`
Returns the full directory of supported crop diseases and their severity levels.

### `GET /health`
Returns service status, model memory state, and registered category count.

---

## 📤 Push Codebase to GitHub

To push this codebase to the team repository:

```bash
git init
git add .
git commit -m "feat: complete AI crop disease detection & advisory system codebase"
git branch -M main
git remote add origin https://github.com/harshadsaulakhe-rgb/Crop-Disease-Detection-Team-Desktop-.git
git push -u origin main
```

---

## 👥 Team & License
Developed for the **AgriTech AI Innovation Challenge**.
Licensed under the [MIT License](LICENSE).
