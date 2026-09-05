"""
advisory.py
-----------
Agricultural Advisory Engine for AI Crop Disease Detection System.
Provides curated, actionable agronomic recommendations including:
- Biological / Organic remedies
- Chemical fungicide/pesticide treatments & dosage
- Cultural and preventive field practices
- Urgency level and immediate 24-48 hour response actions
"""

import re
from typing import Dict, Any, List

# Comprehensive knowledge base mapping PlantVillage disease classes to agronomic advisory
DISEASE_ADVISORY_DATABASE: Dict[str, Dict[str, Any]] = {
    "Apple___Apple_scab": {
        "crop": "Apple",
        "condition": "Apple Scab",
        "pathogen": "Fungus (Venturia inaequalis)",
        "severity": "High",
        "urgency": "Action required within 48 hours to stop spread to fruit clusters.",
        "symptoms": "Olive-green to velvety brown-black spots on leaves and fruit with curled, distorted foliage.",
        "organic_remedies": [
            "Apply liquid copper or sulfur sprays early in the morning before spore dispersal.",
            "Spray bio-fungicide containing Bacillus subtilis (Serenade) at 7-day intervals.",
            "Rake and compost or burn fallen leaves in autumn to eliminate overwintering fungal ascospores."
        ],
        "chemical_treatments": [
            "Captan 50 WP: 2.0 to 2.5 g per liter of water at green tip and petal fall stages.",
            "Mancozeb 75% WP: 2 g per liter of water as a protective spray.",
            "Myclobutanil or Difenoconazole for systemic curative action if lesions are already visible."
        ],
        "preventive_practices": [
            "Prune tree canopy annually during winter to maximize air circulation and sun penetration.",
            "Avoid overhead sprinkler irrigation; keep leaf surface dry.",
            "Select scab-resistant cultivars such as Liberty, Enterprise, or Prima for new plantings."
        ],
        "favorable_conditions": "Cool (15-24°C), wet weather with continuous leaf moisture for 9+ hours."
    },
    "Apple___Black_rot": {
        "crop": "Apple",
        "condition": "Black Rot (Frog-eye Leaf Spot)",
        "pathogen": "Fungus (Botryosphaeria obtusa)",
        "severity": "Moderate",
        "urgency": "Inspect branches for cankers and remove infected mummified apples within 3 days.",
        "symptoms": "Circular brown leaf spots with purple margins ('frog-eye' appearance); black rot on fruit.",
        "organic_remedies": [
            "Spray Copper Hydroxide or Bordeaux mixture (4:4:50) at tight cluster stage.",
            "Prune out dead wood, fire blight strikes, and mummified fruits hanging on branches.",
            "Apply bio-rational sulfur sprays during early fruit development."
        ],
        "chemical_treatments": [
            "Captan 80 WDG: 1.5 - 2.0 kg/ha during pink bud and petal fall stages.",
            "Thiophanate-methyl 70 WP: 1 g per liter of water mixed with a protective contact fungicide.",
            "Strictly observe 14-day pre-harvest interval (PHI) for chemical sprays."
        ],
        "preventive_practices": [
            "Sterilize pruning shears with 70% isopropyl alcohol between branch cuts.",
            "Maintain balanced nitrogen fertilization; excess vegetative growth promotes infection.",
            "Promptly clear leaf litter and fruit drops from orchard floor."
        ],
        "favorable_conditions": "Warm (20-27°C) humid periods following spring rains."
    },
    "Apple___Cedar_apple_rust": {
        "crop": "Apple",
        "condition": "Cedar Apple Rust",
        "pathogen": "Fungus (Gymnosporangium juniperi-virginianae)",
        "severity": "Moderate",
        "urgency": "Apply protective fungicide before anticipated rain events when galls on junipers are active.",
        "symptoms": "Bright yellow-orange or reddish spots on upper leaf surfaces; raised tube-like structures beneath.",
        "organic_remedies": [
            "Spray wettable sulfur (3-4 g/L) at pink bud through petal fall.",
            "Remove eastern red cedar / juniper trees within a 1-2 km radius of the apple orchard if possible.",
            "Apply neem oil extracts at early bud emergence to disrupt fungal germination."
        ],
        "chemical_treatments": [
            "Myclobutanil (Immunox): 1.5 ml per liter of water at pink stage.",
            "Mancozeb 75% WP: 2 g per liter from pink bud until 2 weeks after petal fall.",
            "Triadimefon or Tebuconazole for targeted systemic rust control."
        ],
        "preventive_practices": [
            "Plant resistant apple varieties like Redfree, Liberty, Freedom, or Williams Pride.",
            "Scout nearby ornamental junipers and prune out brown gelatinous rust galls before spring rains."
        ],
        "favorable_conditions": "Warm spring rains (12-24°C) causing orange gelatinous horns on juniper galls."
    },
    "Apple___healthy": {
        "crop": "Apple",
        "condition": "Healthy Foliage",
        "pathogen": "None (Disease Free)",
        "severity": "Healthy",
        "urgency": "No remedial action required. Maintain current proactive orchard care.",
        "symptoms": "Uniform green, vibrant leaf surface with no lesions, discoloration, or pest infestations.",
        "organic_remedies": [
            "Continue applying compost tea or foliar sea-kelp spray every 3 weeks for enhanced vigor.",
            "Encourage beneficial predators like ladybugs, hoverflies, and predatory mites."
        ],
        "chemical_treatments": [
            "No chemical fungicides or bactericides needed at this stage."
        ],
        "preventive_practices": [
            "Maintain consistent drip irrigation schedule and soil mulch.",
            "Perform bi-weekly routine leaf scouting to catch any early outbreaks promptly."
        ],
        "favorable_conditions": "Optimal agronomic growing conditions."
    },
    "Corn_(maize)___Cercospora_leaf_spot_Gray_leaf_spot": {
        "crop": "Corn (Maize)",
        "condition": "Gray Leaf Spot (Cercospora)",
        "pathogen": "Fungus (Cercospora zeae-maydis)",
        "severity": "High",
        "urgency": "Evaluate field threshold; apply fungicide if lesions appear on the ear leaf or higher before silking.",
        "symptoms": "Rectangular, pale brown to gray lesions strictly restricted by leaf veins (blocky shape).",
        "organic_remedies": [
            "Foliar spray of Potassium silicate solution (2 ml/L) to strengthen plant cell walls.",
            "Apply biological bio-fungicide Bacillus pumilus to suppress fungal sporulation."
        ],
        "chemical_treatments": [
            "Azoxystrobin + Difenoconazole (e.g., Amistar Top): 1.0 ml per liter of water.",
            "Pyraclostrobin (Headline): 0.5 - 0.75 L/ha applied at VT (tasseling) stage.",
            "Propiconazole 25% EC: 1 ml per liter of water at first sign of disease onset."
        ],
        "preventive_practices": [
            "Practice 2-year crop rotation with non-host crops (soybean, sorghum, or pulses).",
            "Till under corn residue in fields with severe history to speed up decomposition of spores.",
            "Select hybrids with high Cercospora resistance ratings."
        ],
        "favorable_conditions": "Warm (25-32°C), humid weather (>90% RH) and persistent morning dews."
    },
    "Corn_(maize)___Common_rust_": {
        "crop": "Corn (Maize)",
        "condition": "Common Rust",
        "pathogen": "Fungus (Puccinia sorghi)",
        "severity": "Moderate",
        "urgency": "Spray within 48 hours if rust pustules appear on upper leaves before silking.",
        "symptoms": "Golden-brown to cinnamon-brown powdery pustules on both upper and lower leaf surfaces.",
        "organic_remedies": [
            "Foliar spray of neem seed kernel extract (NSKE 5%) or cold-pressed neem oil (5 ml/L).",
            "Spray Trichoderma viride or Bacillus subtilis culture to colonize and outcompete rust spores."
        ],
        "chemical_treatments": [
            "Mancozeb 75% WP: 2.0 - 2.5 g per liter of water.",
            "Azoxystrobin + Propiconazole: 1.5 ml per liter applied at early blister stage.",
            "Tebuconazole 25.9% EC: 1.0 ml per liter for rapid curative knockdown."
        ],
        "preventive_practices": [
            "Plant rust-resistant certified hybrid maize seed.",
            "Ensure balanced fertilization; avoid excessive nitrogen that produces tender, susceptible tissue."
        ],
        "favorable_conditions": "Cool to moderate temperatures (16-25°C) with high relative humidity (>95%)."
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "crop": "Corn (Maize)",
        "condition": "Northern Corn Leaf Blight",
        "pathogen": "Fungus (Exserohilum turcicum)",
        "severity": "Critical",
        "urgency": "Immediate treatment needed if lesions approach ear leaf prior to grain filling.",
        "symptoms": "Long, elliptical, grayish-green or tan cigar-shaped lesions (2.5 to 15 cm long).",
        "organic_remedies": [
            "Apply bio-formulations of Pseudomonas fluorescens (10 g/L) at 10-day intervals.",
            "Spray copper oxychloride (2.5 g/L) early before lesions coalesce."
        ],
        "chemical_treatments": [
            "Azoxystrobin 18.2% + Difenoconazole 11.4% SC: 1 ml per liter of water.",
            "Mancozeb 75% WP: 2.5 g per liter of water at 10-14 day intervals.",
            "Fluxapyroxad + Pyraclostrobin: high-efficacy dual-mode action for commercial stands."
        ],
        "preventive_practices": [
            "Implement deep autumn plowing to bury crop debris infected with chlamydospores.",
            "Adhere to crop rotation away from continuous maize production for at least 1-2 seasons.",
            "Ensure proper field plant spacing to enhance sunlight interception and airflow."
        ],
        "favorable_conditions": "Moderate temperatures (18-27°C) accompanied by frequent rains and heavy dew."
    },
    "Corn_(maize)___healthy": {
        "crop": "Corn (Maize)",
        "condition": "Healthy Maize Crop",
        "pathogen": "None (Disease Free)",
        "severity": "Healthy",
        "urgency": "Crop in excellent condition. Continue standard agronomic calendar.",
        "symptoms": "Broad, vibrant deep-green leaves with sturdy stalks and clean photosynthetic tissue.",
        "organic_remedies": [
            "Apply zinc sulfate micronutrient spray (0.5%) if soil tests show deficiency.",
            "Side-dress with well-decomposed farmyard manure or vermicompost."
        ],
        "chemical_treatments": [
            "No chemical intervention required."
        ],
        "preventive_practices": [
            "Maintain regular weeding during critical first 30-45 days after sowing.",
            "Monitor soil moisture levels during tasseling and silking to prevent drought stress."
        ],
        "favorable_conditions": "Normal sunny growing conditions."
    },
    "Pepper,_bell___Bacterial_spot": {
        "crop": "Bell Pepper",
        "condition": "Bacterial Spot",
        "pathogen": "Bacterium (Xanthomonas campestris pv. vesicatoria)",
        "severity": "High",
        "urgency": "Halt overhead irrigation immediately; spray copper-mancozeb tank mix within 24 hours.",
        "symptoms": "Small, water-soaked, dark brown blistering lesions on leaves; severe leaf drop exposing fruit to sunscald.",
        "organic_remedies": [
            "Spray Copper Octanoate (copper soap) or Copper Hydroxide (2 g/L) in early morning.",
            "Apply Bacillus amyloliquefaciens (Double Nickel 55) bio-bactericide.",
            "Use certified pathogen-free pepper seeds or hot water seed soak (50°C for 25 minutes)."
        ],
        "chemical_treatments": [
            "Copper Oxychloride (2.5 g/L) mixed with Mancozeb (2 g/L) to counter copper-resistant bacterial strains.",
            "Streptomycin sulfate + Tetracycline (plant-grade antibiotic, where permitted by local regulations): 0.5 g/L.",
            "Kasugamycin 3% SL: 1.5 - 2.0 ml per liter of water."
        ],
        "preventive_practices": [
            "Never work in pepper fields while foliage is wet from rain or morning dew.",
            "Switch from overhead sprinkling to drip irrigation under plastic mulch.",
            "Rotate peppers with non-solanaceous crops (beans, corn, cabbage) for 2-3 years."
        ],
        "favorable_conditions": "High temperatures (24-30°C) with frequent rainfall and splashing water."
    },
    "Pepper,_bell___healthy": {
        "crop": "Bell Pepper",
        "condition": "Healthy Pepper Plant",
        "pathogen": "None (Disease Free)",
        "severity": "Healthy",
        "urgency": "No action required. Plant shows optimal vegetative health.",
        "symptoms": "Glossy green leaves, sturdy branching, and blossom sets with no necrotic spots.",
        "organic_remedies": [
            "Apply seaweed extract foliar tonic every 14 days to boost immunity.",
            "Mulch bed with clean straw to conserve moisture and suppress weeds."
        ],
        "chemical_treatments": [
            "No chemical treatments required."
        ],
        "preventive_practices": [
            "Maintain soil calcium levels to prevent blossom end rot in developing peppers.",
            "Keep monitoring for aphids, thrips, and whiteflies on undersides of leaves."
        ],
        "favorable_conditions": "Warm, sunny, well-aerated conditions."
    },
    "Potato___Early_blight": {
        "crop": "Potato",
        "condition": "Early Blight",
        "pathogen": "Fungus (Alternaria solani)",
        "severity": "High",
        "urgency": "Initiate protective spray program within 24-48 hours before lower leaves defoliate.",
        "symptoms": "Dark brown to black circular spots with concentric target-board rings, starting on older leaves.",
        "organic_remedies": [
            "Spray Trichoderma harzianum or Bacillus subtilis bio-fungicide (5-10 g/L).",
            "Apply copper sulfate or copper hydroxide (2 g/L) at 7-10 day intervals.",
            "Remove and destroy lower infected senescing leaves to reduce inoculum load."
        ],
        "chemical_treatments": [
            "Mancozeb 75% WP: 2.5 g per liter of water as a protective cover.",
            "Chlorothalonil 75% WP: 2.0 g per liter of water.",
            "Difenoconazole 25% EC (Score): 0.5 ml per liter of water for systemic eradication.",
            "Azoxystrobin 23% SC: 1.0 ml per liter of water."
        ],
        "preventive_practices": [
            "Avoid overhead irrigation; use furrow or drip systems to avoid wetting foliage.",
            "Maintain adequate nitrogen and potassium fertility; stressed plants succumb earlier.",
            "Harvest tubers only after vine maturity to prevent spore contact during digging."
        ],
        "favorable_conditions": "Alternating wet and dry periods with temperatures between 24°C and 29°C."
    },
    "Potato___Late_blight": {
        "crop": "Potato",
        "condition": "Late Blight",
        "pathogen": "Oomycete (Phytophthora infestans)",
        "severity": "Critical",
        "urgency": "CRITICAL EMERGENCY: Can devastate an entire field in 5-7 days. Spray immediately (within 24 hours).",
        "symptoms": "Large, irregular water-soaked pale green to brown lesions with white fuzzy mold on leaf undersides in high humidity.",
        "organic_remedies": [
            "Spray Bordeaux mixture (1% copper sulfate + hydrated lime) as preventive barrier.",
            "Apply Copper Octanoate every 5 days during persistent cool, wet forecasts.",
            "Immediately roguer (uproot and bury) heavily infected plants inside plastic sacks."
        ],
        "chemical_treatments": [
            "Cymoxanil 8% + Mancozeb 64% WP (Curzate): 2.5 g per liter of water (strong kickback action).",
            "Metalaxyl-M + Mancozeb (Ridomil Gold): 2.5 g per liter of water.",
            "Dimethomorph 50% WP: 1.0 g per liter mixed with Mancozeb (2 g/L).",
            "Mandipropamid (Revus): 0.8 ml per liter of water."
        ],
        "preventive_practices": [
            "Plant only certified disease-free seed tubers; never use market potatoes for seed.",
            "Hill potatoes deeply to create a soil barrier preventing sporangia from washing into tubers.",
            "Destroy cull piles and volunteer potato plants near the field before planting season."
        ],
        "favorable_conditions": "Cool (10-21°C), overcast weather with high humidity (>90%) and frequent rain or fog."
    },
    "Potato___healthy": {
        "crop": "Potato",
        "condition": "Healthy Potato Crop",
        "pathogen": "None (Disease Free)",
        "severity": "Healthy",
        "urgency": "Foliage in great health. Continue preventive management.",
        "symptoms": "Lush, dark green canopy without yellowing, necrotic spots, or wilting.",
        "organic_remedies": [
            "Apply humic acid and foliar micronutrient blend during tuber initiation stage.",
            "Foliar spray with compost extract for microbial leaf surface protection."
        ],
        "chemical_treatments": [
            "No chemical fungicides needed; keep preventive stock ready for rainy spells."
        ],
        "preventive_practices": [
            "Ensure regular ridging and hilling up around the stems at 30 and 45 days.",
            "Monitor soil moisture to prevent tuber hollow heart and scab."
        ],
        "favorable_conditions": "Moderate sunshine and well-drained loam soil."
    },
    "Tomato___Bacterial_spot": {
        "crop": "Tomato",
        "condition": "Bacterial Spot",
        "pathogen": "Bacterium (Xanthomonas spp.)",
        "severity": "High",
        "urgency": "Discontinue overhead sprinkling immediately; apply bactericidal spray within 24 hours.",
        "symptoms": "Small (1-3 mm), dark brown to black circular lesions, greasy appearance, often with yellow halo.",
        "organic_remedies": [
            "Spray copper hydroxide (Kocide 3000) at 1.5 - 2.0 g/L.",
            "Apply bio-agent Bacillus subtilis or Streptomyces lydicus.",
            "Treat seed with 1.3% sodium hypochlorite for 1 minute before sowing."
        ],
        "chemical_treatments": [
            "Copper Hydroxide + Mancozeb tank mix (prevents copper-resistant bacterial strains).",
            "Kasugamycin 3% SL: 1.5 ml/L applied every 7-10 days.",
            "Streptocycline (antibacterial formulation, where approved): 0.5 g per 10 liters of water."
        ],
        "preventive_practices": [
            "Sterilize nursery trays and stakes with 10% bleach solution before use.",
            "Stake and prune tomato plants to keep foliage elevated away from wet soil.",
            "Avoid harvesting or cultivating fields while plants are wet."
        ],
        "favorable_conditions": "Warm (24-30°C) temperatures combined with high humidity and rain splashes."
    },
    "Tomato___Early_blight": {
        "crop": "Tomato",
        "condition": "Early Blight",
        "pathogen": "Fungus (Alternaria solani / Alternaria alternata)",
        "severity": "High",
        "urgency": "Prune infected bottom leaves and initiate fungicidal spray within 48 hours.",
        "symptoms": "Dark brown circular spots with distinctive concentric 'target rings' surrounded by yellow halo on lower leaves.",
        "organic_remedies": [
            "Spray cold-pressed neem oil (0.5% v/v) mixed with potassium soap as an emulsifier.",
            "Apply copper-based fungicides (Bordeaux mixture 1% or Copper Oxychloride 2.5 g/L).",
            "Foliar spray of Trichoderma viride bio-fungicide (5 g/L)."
        ],
        "chemical_treatments": [
            "Chlorothalonil 75% WP: 2 g per liter of water as a preventative protective spray.",
            "Mancozeb 75% WP: 2 g per liter of water applied every 7-10 days.",
            "Azoxystrobin + Difenoconazole: 1.0 ml per liter for strong systemic curative control.",
            "Pyraclostrobin (Cabrio): 1.5 g per liter of water."
        ],
        "preventive_practices": [
            "Strip bottom 20-30 cm of leaves (bottom pruning) to prevent soil-splash inoculation.",
            "Lay down black plastic mulch or straw mulch around the base of all plants.",
            "Water only at the base using drip lines or soaker hoses, never from overhead sprinklers."
        ],
        "favorable_conditions": "Warm temperatures (24-29°C) with alternating dry and humid/rainy spells."
    },
    "Tomato___Late_blight": {
        "crop": "Tomato",
        "condition": "Late Blight",
        "pathogen": "Oomycete (Phytophthora infestans)",
        "severity": "Critical",
        "urgency": "CRITICAL EMERGENCY: Spreads aggressively across the whole crop in 3-5 days. Spray within 24 hours.",
        "symptoms": "Large, irregular greasy water-soaked pale-green to brown lesions; white cottony fungal growth on underside under humid conditions.",
        "organic_remedies": [
            "Bordeaux mixture (1:1:100) or Copper Hydroxide spray at 4-5 day intervals.",
            "Immediate removal and deep burial (or burning) of heavily infected plants.",
            "Do NOT compost diseased tomato foliage."
        ],
        "chemical_treatments": [
            "Metalaxyl 8% + Mancozeb 64% WP (Ridomil Gold): 2.5 g per liter of water.",
            "Cymoxanil 8% + Mancozeb 64% WP (Curzate): 2.5 g per liter of water.",
            "Dimethomorph 50% WP (Acrobat): 1.5 g per liter of water.",
            "Fenamidone 10% + Mancozeb 50% WG (Sectin): 2.5 g per liter of water."
        ],
        "preventive_practices": [
            "Maintain wide plant spacing (60 x 45 cm minimum) to promote rapid leaf drying.",
            "Never plant tomatoes adjacent to potato fields.",
            "Select late-blight resistant tomato hybrids such as Mountain Magic, Defiant, or Plum Regal."
        ],
        "favorable_conditions": "Cool (15-22°C), wet, foggy weather with high humidity (>90%)."
    },
    "Tomato___Leaf_Mold": {
        "crop": "Tomato",
        "condition": "Leaf Mold",
        "pathogen": "Fungus (Passalora fulva / Cladosporium fulvum)",
        "severity": "Moderate",
        "urgency": "Increase greenhouse ventilation immediately; apply fungicide within 48 hours.",
        "symptoms": "Pale greenish-yellow patches on upper leaf surface; velvety olive-brown mold growth on underside.",
        "organic_remedies": [
            "Spray sulfur-based wettable powder (2 g/L) or copper soap.",
            "Apply bio-fungicide Bacillus amyloliquefaciens to foliage.",
            "Ventilate polyhouse or greenhouse; keep relative humidity below 85%."
        ],
        "chemical_treatments": [
            "Chlorothalonil 75% WP: 2 g per liter of water.",
            "Mancozeb 75% WP: 2 g per liter of water.",
            "Difenoconazole 25% EC: 0.5 ml per liter of water.",
            "Cyprodinil + Fludioxonil (Switch 62.5 WG): 0.8 g per liter."
        ],
        "preventive_practices": [
            "Maximize greenhouse venting and run circulating fans to keep leaves dry.",
            "Prune lower suckers to improve internal canopy aeration.",
            "Avoid evening watering that leaves the foliage wet overnight."
        ],
        "favorable_conditions": "High humidity (>85% RH) and temperatures between 21°C and 27°C, common in tunnels."
    },
    "Tomato___Septoria_leaf_spot": {
        "crop": "Tomato",
        "condition": "Septoria Leaf Spot",
        "pathogen": "Fungus (Septoria lycopersici)",
        "severity": "High",
        "urgency": "Prune spotted leaves and apply protective fungicide spray within 48 hours.",
        "symptoms": "Numerous tiny (1.5 - 3 mm) circular spots with dark brown margins and grayish-white centers dotted with tiny black specks.",
        "organic_remedies": [
            "Spray Copper Oxychloride 50% WP (2.5 g/L) or Copper Sulfate pentahydrate.",
            "Apply biological bio-control agent Trichoderma harzianum as foliar wash.",
            "Carefully hand-pick and dispose of lower affected leaves."
        ],
        "chemical_treatments": [
            "Chlorothalonil 75% WP: 2.0 g per liter of water (apply every 7-10 days).",
            "Mancozeb 75% WP: 2.5 g per liter of water.",
            "Azoxystrobin 23% SC: 1 ml per liter of water.",
            "Tebuconazole 25.9% EC: 1 ml per liter of water for systemic eradication."
        ],
        "preventive_practices": [
            "Mulch heavily around the base of plants to create a barrier against soil splash.",
            "Practice minimum 2-year crop rotation without solanaceous hosts.",
            "Stake and tie plants upright to keep leaves away from the ground."
        ],
        "favorable_conditions": "Extended wet weather, high humidity, and temperatures between 20°C and 26°C."
    },
    "Tomato___Spider_mites_Two-spotted_spider_mite": {
        "crop": "Tomato",
        "condition": "Two-Spotted Spider Mites",
        "pathogen": "Pest / Acarid (Tetranychus urticae)",
        "severity": "High",
        "urgency": "Spray miticide / botanical wash within 24 hours before webbing covers flower clusters.",
        "symptoms": "Yellow stippling or bronzing on leaf surfaces; fine silky webbing on undersides and growing tips; curled, scorched foliage.",
        "organic_remedies": [
            "Spray insecticidal soap (potassium salts of fatty acids) or neem oil (1% v/v) thoroughly on undersides.",
            "Release predatory mites such as Phytoseiulus persimilis or Neoseiulus californicus.",
            "Strong overhead water wash to knock down mite colonies and disrupt webs."
        ],
        "chemical_treatments": [
            "Abamectin 1.9% EC: 0.5 ml per liter of water (highly potent translaminar miticide).",
            "Spiromesifen 22.9% SC (Oberon): 1 ml per liter of water.",
            "Fenazaquin 10% EC: 1.5 ml per liter of water.",
            "Avoid synthetic pyrethroids as they kill beneficial predatory insects and cause mite resurgence."
        ],
        "preventive_practices": [
            "Avoid plant moisture stress; spider mites thrive on water-stressed dusty crops.",
            "Keep farm perimeter free of broadleaf weeds that host overwintering mites.",
            "Maintain overhead humidity in protected structures during hot, dry spells."
        ],
        "favorable_conditions": "Hot (>30°C), dry, dusty conditions with low relative humidity."
    },
    "Tomato___Target_Spot": {
        "crop": "Tomato",
        "condition": "Target Spot",
        "pathogen": "Fungus (Corynespora cassiicola)",
        "severity": "Moderate",
        "urgency": "Begin protective fungicide treatment within 48 hours to preserve canopy cover.",
        "symptoms": "Small pinpoint brown lesions that enlarge into circular spots with light brown centers and dark concentric rings.",
        "organic_remedies": [
            "Apply Copper Octanoate or Bordeaux mixture at weekly intervals.",
            "Foliar spray with Bacillus subtilis bio-fungicide.",
            "Remove diseased foliage from the bottom third of the vine."
        ],
        "chemical_treatments": [
            "Pyraclostrobin + Boscalid (Pristine): 1.0 - 1.2 g per liter of water.",
            "Chlorothalonil 75% WP: 2 g per liter of water.",
            "Azoxystrobin 23% SC: 1 ml per liter of water.",
            "Fluopyram + Trifloxystrobin: 0.8 ml per liter of water."
        ],
        "preventive_practices": [
            "Ensure proper spacing between rows to enhance airflow.",
            "Avoid overhead irrigation; schedule watering during the early morning.",
            "Plow under or destroy crop residues immediately post-harvest."
        ],
        "favorable_conditions": "Moderate to warm temperatures (20-28°C) with prolonged periods of leaf wetness."
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "crop": "Tomato",
        "condition": "Tomato Yellow Leaf Curl Virus (TYLCV)",
        "pathogen": "Begomovirus (Transmitted by Whitefly Bemisia tabaci)",
        "severity": "Critical",
        "urgency": "Control whitefly vectors immediately; rogue and destroy infected plants showing severe stunting.",
        "symptoms": "Severe stunting of plants; leaves curled upward (cupping), reduced in size, with intense interveinal yellowing (chlorosis); flower drop.",
        "organic_remedies": [
            "Install yellow sticky traps (15-20 traps per acre) at canopy level to monitor and mass-trap whiteflies.",
            "Foliar spray of neem oil (5 ml/L) mixed with Beauveria bassiana entomopathogenic fungus (5 g/L).",
            "Cover seedlings in nurseries with 50-mesh insect-proof netting."
        ],
        "chemical_treatments": [
            "No chemical cure exists for viral particles; control the whitefly vector:",
            "Thiamethoxam 25% WG: 0.5 g per liter of water (foliar spray or drench).",
            "Imidacloprid 17.8% SL: 0.5 ml per liter of water.",
            "Diafenthiuron 50% WP: 1.2 g per liter of water for resistant whitefly populations.",
            "Pyriproxyfen 10% EC: 1.5 ml per liter of water to sterilize adult whiteflies and kill nymphs."
        ],
        "preventive_practices": [
            "Plant TYLCV-resistant or tolerant tomato hybrids (e.g., Tycoon, Saaho, US-440).",
            "Eradicate weed hosts (Solanum nigrum, Datura, Parthenium) around field edges.",
            "Implement a 2-month crop-free fallow period between solanaceous plantings."
        ],
        "favorable_conditions": "Warm, dry conditions favoring explosive whitefly vector reproduction."
    },
    "Tomato___Tomato_mosaic_virus": {
        "crop": "Tomato",
        "condition": "Tomato Mosaic Virus (ToMV)",
        "pathogen": "Tobamovirus (Mechanically Transmitted)",
        "severity": "High",
        "urgency": "Immediately isolate or remove infected plants; sterilize all hand tools and wash hands with milk/detergent.",
        "symptoms": "Mottled light and dark green patterns on leaves, fern-like distortion, blistering, and stunted plant growth.",
        "organic_remedies": [
            "Soak seeds in 10% trisodium phosphate (TSP) solution for 30 minutes before planting.",
            "Dip hands and pruning shears in non-fat dry milk solution (20% w/v) to deactivate viral particles during trellising.",
            "Carefully bag and discard symptomatic plants to prevent touch transmission."
        ],
        "chemical_treatments": [
            "No chemical viricides exist. Management relies on strict sanitation and vector hygiene.",
            "Apply micronutrient zinc and boron sprays to help healthy surrounding plants maintain vigor."
        ],
        "preventive_practices": [
            "Never smoke or handle tobacco products before working in tomato crops (tobacco mosaic virus cross-infection).",
            "Use certified virus-free commercial seed.",
            "Sterilize trellising twine, cages, and stakes in 10% bleach before reusing."
        ],
        "favorable_conditions": "Easily spread mechanically by hands, tools, clothes, and sap contact at any temperature."
    },
    "Tomato___healthy": {
        "crop": "Tomato",
        "condition": "Healthy Tomato Crop",
        "pathogen": "None (Disease Free)",
        "severity": "Healthy",
        "urgency": "No treatment required. Crop shows optimal physiological health.",
        "symptoms": "Uniform deep green foliage, robust stem girth, healthy flower trusses, and no signs of pathogen damage.",
        "organic_remedies": [
            "Apply foliar fish amino acid or vermiwash spray (20 ml/L) to sustain balanced vegetative growth.",
            "Keep soil well-aerated and maintain organic compost layer."
        ],
        "chemical_treatments": [
            "No chemical intervention needed."
        ],
        "preventive_practices": [
            "Continue prophylactic weekly scouting of undersides of leaves and leaf axils.",
            "Maintain consistent soil moisture through drip irrigation to prevent calcium-deficiency blossom end rot.",
            "Stake and prune side shoots on sunny dry mornings."
        ],
        "favorable_conditions": "Optimal agronomic conditions (22-28°C, balanced nutrition, regulated moisture)."
    }
}


def clean_label_name(raw_label: str) -> str:
    """
    Converts a raw PlantVillage class string into a human-friendly crop & disease name.
    Example: 'Tomato___Early_blight' -> 'Tomato - Early Blight'
    """
    if not raw_label:
        return "Unknown Condition"
    
    parts = raw_label.split("___")
    crop = parts[0].replace("_", " ").replace("(", " (").strip()
    condition = parts[1].replace("_", " ").strip() if len(parts) > 1 else ""
    
    # Capitalize cleanly
    crop = " ".join([w.capitalize() for w in crop.split()])
    condition = " ".join([w.capitalize() for w in condition.split()])
    
    if condition.lower() == "healthy":
        return f"{crop} (Healthy)"
    return f"{crop}: {condition}"


def get_advisory(label: str, crop: Optional[str] = None) -> Dict[str, Any]:
    """
    Looks up agricultural advisory by dataset class label or fuzzy match,
    integrated with plant_leaf_disease_database_200plus.json.
    """
    # ── 1. HEALTHY LEAF CASE ──
    if label == "HEALTHY_LEAF" or label.endswith("___healthy") or (crop and "healthy" in label.lower()):
        crop_clean = crop or (label.split("___")[0].replace("_", " ") if "___" in label else "Crop")
        return {
            "class_id": f"{crop_clean}___healthy",
            "display_name": f"{crop_clean} (Healthy)",
            "crop": crop_clean,
            "condition": "Healthy Foliage",
            "pathogen": "None (Disease Free)",
            "severity": "Healthy",
            "urgency": "No disease symptoms detected. Maintain regular proactive crop management.",
            "symptoms": "Uniform vibrant green leaf surface with no lesions, necrosis, or chlorosis.",
            "organic_remedies": [
                "Continue applying compost tea or foliar sea-kelp spray every 2-3 weeks for plant vigor.",
                "Maintain balanced N-P-K soil fertility; avoid excessive nitrogen fertilizer.",
                "Encourage beneficial predatory insects such as ladybugs, spiders, and lacewings."
            ],
            "chemical_treatments": [
                "No chemical fungicides or bactericides required for healthy crops."
            ],
            "preventive_practices": [
                "Inspect crop canopy twice weekly during early morning for early disease signs.",
                "Water at the base of plants using drip irrigation; keep foliage dry.",
                "Ensure proper plant spacing for maximum sunlight penetration and air circulation."
            ],
            "favorable_conditions": "Optimal crop growth conditions with good air circulation and balanced soil moisture."
        }

    # ── 2. Direct lookup in curated DISEASE_ADVISORY_DATABASE ──
    if label in DISEASE_ADVISORY_DATABASE:
        data = dict(DISEASE_ADVISORY_DATABASE[label])
        data["class_id"] = label
        data["display_name"] = clean_label_name(label)
        return data

    # ── 3. Lookup in plant_leaf_disease_database_200plus.json ──
    try:
        from utils.disease_database import DiseaseKnowledgeBase
        db = DiseaseKnowledgeBase.get_instance()
        entry = db.find_disease_by_class_key(label)
        if not entry and crop:
            entry = db.get_disease(crop, label)

        if entry:
            crop_name = entry.get("crop", crop or "Crop")
            dis_name = entry.get("disease_name", label)
            cause = entry.get("cause", "Plant Pathogen")
            severity = entry.get("severity", "Moderate").title()
            symptoms = f"{entry.get('symptoms', '')}. Visual features: {entry.get('visual_features', '')}"

            # Determine cause-specific treatments
            is_fungal = any(k in cause.lower() for k in ["alternaria", "phytophthora", "puccinia", "venturia", "cercospora", "fungus", "mold", "mildew"])
            is_bacterial = any(k in cause.lower() for k in ["xanthomonas", "pseudomonas", "bacteria", "erwinia", "ralstonia"])
            is_viral = any(k in cause.lower() for k in ["virus", "viroid", "mosaic", "curl"])

            if is_fungal:
                organic = [
                    "Apply copper oxychloride (3 g/L) or Bordeaux mixture (1%) as protective spray.",
                    "Spray bio-fungicide Trichoderma harzianum or Bacillus subtilis at 7-day intervals.",
                    "Remove heavily infected leaves and compost/burn them away from fields."
                ]
                chemical = [
                    "Apply Mancozeb 75% WP (2.5 g/L) or Chlorothalonil (2 g/L) as protective contact spray.",
                    "Use systemic curative fungicide like Azoxystrobin or Difenoconazole if lesions are spreading.",
                    "Ensure adequate spray coverage on both upper and lower leaf surfaces."
                ]
            elif is_bacterial:
                organic = [
                    "Spray Copper Hydroxide (2.5 g/L) during early vegetative development.",
                    "Apply neem cake soil amendment to stimulate antagonistic rhizobacteria.",
                    "Sterilize all pruning and harvesting tools with 70% alcohol between plants."
                ]
                chemical = [
                    "Apply Copper Oxychloride 50 WP (2.5 g/L) mixed with Streptomycin sulphate (100 ppm).",
                    "Avoid overhead sprinkler irrigation to stop bacterial splash dissemination."
                ]
            elif is_viral:
                organic = [
                    "Apply cold-pressed neem oil (5 ml/L) weekly to deter insect vectors (whiteflies, aphids).",
                    "Install yellow sticky traps (15-20 traps/acre) to monitor and capture vectors.",
                    "Rogue and bury severely stunted or mottled plants immediately."
                ]
                chemical = [
                    "Spray systemic insecticide (e.g. Imidacloprid 17.8 SL at 0.5 ml/L or Thiamethoxam 25 WG at 0.3 g/L) to manage vector populations.",
                    "Note: Chemical pesticides do not cure viral infections directly; control insect vectors."
                ]
            else:
                organic = ["Apply neem-based bio-rational formulations and improve field aeration."]
                chemical = ["Consult local agricultural extension service for registered fungicides."]

            return {
                "class_id": label,
                "display_name": f"{crop_name}: {dis_name}",
                "crop": crop_name,
                "condition": dis_name,
                "pathogen": cause,
                "severity": severity,
                "urgency": f"Action recommended within 48 hours to suppress {dis_name} spread.",
                "symptoms": symptoms,
                "organic_remedies": organic,
                "chemical_treatments": chemical,
                "preventive_practices": [
                    "Practice 2-3 year crop rotation with non-host botanical families.",
                    "Ensure clean seed stock and certified pathogen-free nursery transplants.",
                    "Avoid overhead irrigation; water at plant base to keep canopy dry."
                ],
                "favorable_conditions": "Warm, humid weather with prolonged leaf wetness.",
                "similar_diseases": entry.get("similar_diseases", [])
            }
    except Exception as e:
        pass

    # ── 4. Fuzzy match by condition name ──
    for key, advisory in DISEASE_ADVISORY_DATABASE.items():
        if key.lower() == label.lower() or advisory["condition"].lower() == label.lower():
            res = dict(advisory)
            res["class_id"] = key
            res["display_name"] = clean_label_name(key)
            return res

    # ── 5. General fallback advisory ──
    return {
        "class_id": label,
        "display_name": clean_label_name(label),
        "crop": label.split("___")[0].replace("_", " ") if "___" in label else "Crop",
        "condition": label.split("___")[1].replace("_", " ") if "___" in label else label,
        "pathogen": "Unspecified Plant Pathogen",
        "severity": "Moderate",
        "urgency": "Inspect affected plants and isolate diseased foliage for further diagnostic confirmation.",
        "symptoms": "Leaf discoloration, spotting, or lesions detected on foliage.",
        "organic_remedies": [
            "Apply a broad-spectrum botanical spray such as cold-pressed neem oil (5 ml/L).",
            "Spray bio-fungicide containing Bacillus subtilis or Trichoderma spp.",
            "Remove heavily infected leaves and destroy them away from the cropping area."
        ],
        "chemical_treatments": [
            "Consult a local certified agricultural extension officer for registered chemicals.",
            "Apply a broad-spectrum protective contact fungicide such as Mancozeb (2.5 g/L) or Copper Oxychloride (2.5 g/L)."
        ],
        "preventive_practices": [
            "Avoid overhead irrigation to minimize leaf moisture duration.",
            "Maintain optimal plant spacing to ensure rapid airflow and sunlight penetration.",
            "Practice 2-3 season crop rotation with non-host species."
        ],
        "favorable_conditions": "Humid conditions with stagnant air and persistent surface moisture."
    }


def list_supported_diseases() -> List[Dict[str, Any]]:
    """Returns an overview list of all supported crops and diseases from the JSON database."""
    try:
        from utils.disease_database import DiseaseKnowledgeBase
        db = DiseaseKnowledgeBase.get_instance()
        if db.is_loaded and db.diseases:
            summary = []
            for d in db.diseases:
                crop = d.get("crop", "Unknown")
                name = d.get("disease_name", "Unknown")
                class_id = f"{crop}___{name.replace(' ', '_')}"
                summary.append({
                    "class_id": class_id,
                    "crop": crop,
                    "condition": name,
                    "severity": d.get("severity", "Moderate").title(),
                    "pathogen": d.get("cause", "N/A"),
                    "display_name": f"{crop}: {name}",
                    "symptoms": d.get("symptoms", "")
                })
            return summary
    except Exception:
        pass

    # Fallback to local dictionary
    summary_list = []
    for class_id, info in DISEASE_ADVISORY_DATABASE.items():
        summary_list.append({
            "class_id": class_id,
            "crop": info["crop"],
            "condition": info["condition"],
            "severity": info["severity"],
            "pathogen": info["pathogen"],
            "display_name": clean_label_name(class_id)
        })
    return summary_list


if __name__ == "__main__":
    print(f"Total crop disease advisory profiles configured: {len(DISEASE_ADVISORY_DATABASE)}")
    sample = get_advisory("Tomato___Late_blight")
    print(f"Sample Advisory Loaded: {sample['display_name']} -> Severity: {sample['severity']}")
