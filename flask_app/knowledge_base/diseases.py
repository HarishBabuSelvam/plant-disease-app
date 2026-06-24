# flask_app/knowledge_base/diseases.py
# Complete Plant Disease Knowledge Base

DISEASE_KNOWLEDGE = {

    "Pepper__bell___Bacterial_spot": {
        "display_name": "Pepper Bell - Bacterial Spot",
        "plant": "Pepper (Bell)",
        "disease": "Bacterial Spot",
        "is_healthy": False,
        "cause": "Caused by Xanthomonas campestris bacteria. Spreads through infected seeds, rain splash, and contaminated tools.",
        "symptoms": [
            "Small water-soaked spots on leaves",
            "Spots turn brown with yellow borders",
            "Raised scab-like spots on fruits",
            "Premature leaf and fruit drop",
            "Dark streaks on stems"
        ],
        "treatment": [
            "Apply copper-based bactericide spray immediately",
            "Remove and destroy all infected plant parts",
            "Avoid overhead irrigation - use drip irrigation",
            "Spray every 7-10 days during wet weather",
            "Use streptomycin spray if infection is severe"
        ],
        "prevention": [
            "Use certified disease-free seeds",
            "Rotate crops every 2-3 years",
            "Avoid working with plants when wet",
            "Disinfect all gardening tools regularly",
            "Maintain proper plant spacing for air circulation"
        ],
        "recovery_chance": 72,
        "recovery_message": "Good recovery if treated within 1 week. Early detection is key.",
        "severity": "Medium",
        "spread_risk": "High",
        "treatment_time": "2-3 weeks"
    },

    "Pepper__bell___healthy": {
        "display_name": "Pepper Bell - Healthy",
        "plant": "Pepper (Bell)",
        "disease": "Healthy",
        "is_healthy": True,
        "cause": "No disease detected. Your plant appears to be in excellent health!",
        "symptoms": [
            "Deep green vibrant leaves",
            "No spots lesions or discoloration",
            "Strong upright stems",
            "Normal fruit development"
        ],
        "treatment": [
            "No treatment needed",
            "Continue regular watering schedule",
            "Maintain balanced fertilization",
            "Monitor regularly for early signs of disease"
        ],
        "prevention": [
            "Water at the base of plant not on leaves",
            "Ensure good drainage to prevent root rot",
            "Apply balanced NPK fertilizer monthly",
            "Inspect plants weekly for early disease signs"
        ],
        "recovery_chance": 100,
        "recovery_message": "Your plant is perfectly healthy! Keep up the great care.",
        "severity": "None",
        "spread_risk": "None",
        "treatment_time": "N/A"
    },

    "Potato___Early_blight": {
        "display_name": "Potato - Early Blight",
        "plant": "Potato",
        "disease": "Early Blight",
        "is_healthy": False,
        "cause": "Caused by the fungus Alternaria solani. Spreads through infected plant debris and airborne spores. Favored by warm temperatures and high humidity.",
        "symptoms": [
            "Dark brown circular spots with concentric rings",
            "Yellow halo surrounding the spots",
            "Spots appear first on older lower leaves",
            "Leaves turn yellow and drop prematurely",
            "Dark sunken spots may appear on tubers"
        ],
        "treatment": [
            "Apply chlorothalonil or mancozeb fungicide",
            "Remove and destroy infected leaves immediately",
            "Apply fungicide every 7-14 days",
            "Ensure adequate potassium fertilization",
            "Improve air circulation by proper plant spacing"
        ],
        "prevention": [
            "Use certified disease-free seed potatoes",
            "Practice 3-year crop rotation",
            "Remove and compost plant debris after harvest",
            "Avoid excessive nitrogen fertilization",
            "Apply mulch to prevent soil splash"
        ],
        "recovery_chance": 80,
        "recovery_message": "High recovery chance with early fungicide treatment. Act within 5 days of spotting symptoms.",
        "severity": "Medium",
        "spread_risk": "Medium",
        "treatment_time": "2-3 weeks"
    },

    "Potato___Late_blight": {
        "display_name": "Potato - Late Blight",
        "plant": "Potato",
        "disease": "Late Blight",
        "is_healthy": False,
        "cause": "Caused by Phytophthora infestans - the same pathogen that caused the Irish Potato Famine. Spreads rapidly in cool wet conditions.",
        "symptoms": [
            "Large irregular water-soaked lesions on leaves",
            "White fuzzy mold on underside of leaves",
            "Dark brown to black lesions spreading rapidly",
            "Infected tubers show reddish-brown dry rot",
            "Entire plant can collapse within days"
        ],
        "treatment": [
            "Apply metalaxyl or cymoxanil fungicide IMMEDIATELY",
            "Remove all infected plants and tubers urgently",
            "Do NOT compost infected material - burn or bin it",
            "Spray neighboring plants preventively",
            "Harvest remaining tubers early if infection is widespread"
        ],
        "prevention": [
            "Plant resistant varieties",
            "Avoid planting in low-lying wet areas",
            "Destroy volunteer potato plants",
            "Apply preventive fungicide in wet weather",
            "Ensure excellent drainage in planting area"
        ],
        "recovery_chance": 45,
        "recovery_message": "Low recovery chance - this disease spreads extremely fast. Immediate action required.",
        "severity": "Very High",
        "spread_risk": "Very High",
        "treatment_time": "Act within 24-48 hours"
    },

    "Potato___healthy": {
        "display_name": "Potato - Healthy",
        "plant": "Potato",
        "disease": "Healthy",
        "is_healthy": True,
        "cause": "No disease detected. Your potato plant is thriving!",
        "symptoms": [
            "Lush green foliage",
            "No lesions or discoloration",
            "Strong upright growth",
            "Healthy tuber development underground"
        ],
        "treatment": [
            "No treatment needed",
            "Continue hilling soil around stems",
            "Maintain consistent watering",
            "Monitor for Colorado potato beetles"
        ],
        "prevention": [
            "Hill soil regularly to protect tubers",
            "Water deeply but infrequently",
            "Apply balanced fertilizer at planting",
            "Inspect weekly for signs of blight"
        ],
        "recovery_chance": 100,
        "recovery_message": "Excellent! Your potato plant is in perfect health.",
        "severity": "None",
        "spread_risk": "None",
        "treatment_time": "N/A"
    },

    "Tomato_Bacterial_spot": {
        "display_name": "Tomato - Bacterial Spot",
        "plant": "Tomato",
        "disease": "Bacterial Spot",
        "is_healthy": False,
        "cause": "Caused by Xanthomonas vesicatoria bacteria. Spreads through rain wind contaminated tools and infected seeds.",
        "symptoms": [
            "Small dark water-soaked spots on leaves",
            "Spots develop yellow halos over time",
            "Raised scab-like lesions on fruits",
            "Leaves curl and drop prematurely",
            "Infected seedlings may die"
        ],
        "treatment": [
            "Apply copper hydroxide spray immediately",
            "Combine copper with mancozeb for better effect",
            "Remove badly infected leaves and fruits",
            "Spray every 5-7 days in wet weather",
            "Avoid overhead watering"
        ],
        "prevention": [
            "Use disease-resistant tomato varieties",
            "Use pathogen-free certified seeds",
            "Sanitize tools with 10% bleach solution",
            "Practice 2-3 year crop rotation",
            "Install windbreaks to reduce spread"
        ],
        "recovery_chance": 70,
        "recovery_message": "Moderate recovery if caught early. Copper sprays are most effective in early stages.",
        "severity": "Medium",
        "spread_risk": "High",
        "treatment_time": "3-4 weeks"
    },

    "Tomato_Early_blight": {
        "display_name": "Tomato - Early Blight",
        "plant": "Tomato",
        "disease": "Early Blight",
        "is_healthy": False,
        "cause": "Caused by Alternaria solani fungus. Overwinters in soil and infected debris. Spreads via airborne spores.",
        "symptoms": [
            "Dark brown spots with concentric rings on older leaves",
            "Yellow V-shaped lesions at leaf edges",
            "Stems show dark elongated lesions",
            "Fruit develops dark sunken spots near stem",
            "Lower leaves affected first moving upward"
        ],
        "treatment": [
            "Apply chlorothalonil mancozeb or copper fungicide",
            "Remove and bag all infected lower leaves",
            "Fertilize with balanced NPK to reduce stress",
            "Apply mulch to prevent soil splash",
            "Repeat fungicide every 7-10 days"
        ],
        "prevention": [
            "Stake plants to improve air circulation",
            "Water at soil level - avoid wetting leaves",
            "Remove plant debris at end of season",
            "Rotate tomato crops every 3 years",
            "Apply preventive fungicide at first sign of humidity"
        ],
        "recovery_chance": 85,
        "recovery_message": "Very good recovery chance if treated early. Most plants recover fully with consistent fungicide treatment.",
        "severity": "Medium",
        "spread_risk": "Medium",
        "treatment_time": "2-3 weeks"
    },

    "Tomato_Late_blight": {
        "display_name": "Tomato - Late Blight",
        "plant": "Tomato",
        "disease": "Late Blight",
        "is_healthy": False,
        "cause": "Caused by Phytophthora infestans water mold. Spreads extremely rapidly via airborne spores in cool wet weather.",
        "symptoms": [
            "Large irregular greenish-gray water-soaked patches",
            "White mold growth on leaf undersides",
            "Brown-black lesions on stems",
            "Fruits show large firm brown rotted areas",
            "Entire plant blackens and collapses quickly"
        ],
        "treatment": [
            "Apply metalaxyl plus mancozeb fungicide URGENTLY",
            "Remove ALL infected plant material immediately",
            "Do NOT compost - burn or dispose in sealed bags",
            "Apply fungicide to all surrounding plants",
            "Consider removing entire plant if over 50% infected"
        ],
        "prevention": [
            "Plant late-blight resistant varieties",
            "Ensure excellent air circulation between plants",
            "Apply preventive copper fungicide in rainy periods",
            "Avoid overhead irrigation completely",
            "Monitor weather and act before rain events"
        ],
        "recovery_chance": 40,
        "recovery_message": "Low recovery chance. URGENT action required within 24 hours.",
        "severity": "Very High",
        "spread_risk": "Very High",
        "treatment_time": "Immediate - within 24 hours"
    },

    "Tomato_Leaf_Mold": {
        "display_name": "Tomato - Leaf Mold",
        "plant": "Tomato",
        "disease": "Leaf Mold",
        "is_healthy": False,
        "cause": "Caused by Passalora fulva fungus. Common in greenhouses. Thrives in high humidity above 85%.",
        "symptoms": [
            "Pale green or yellow patches on upper leaf surface",
            "Olive-green to brown fuzzy mold on leaf underside",
            "Infected leaves curl wither and drop",
            "Flowers and fruits rarely affected",
            "Rapid spread in humid warm conditions"
        ],
        "treatment": [
            "Improve greenhouse ventilation immediately",
            "Apply chlorothalonil or copper fungicide",
            "Remove and destroy all affected leaves",
            "Reduce relative humidity below 75%",
            "Increase plant spacing for better airflow"
        ],
        "prevention": [
            "Use leaf mold resistant tomato varieties",
            "Maintain relative humidity below 80%",
            "Ventilate greenhouses well daily",
            "Avoid wetting foliage when watering",
            "Apply preventive fungicide in humid spells"
        ],
        "recovery_chance": 78,
        "recovery_message": "Good recovery if humidity is controlled. Ventilation is more important than fungicide.",
        "severity": "Medium",
        "spread_risk": "Medium",
        "treatment_time": "2-4 weeks"
    },

    "Tomato_Septoria_leaf_spot": {
        "display_name": "Tomato - Septoria Leaf Spot",
        "plant": "Tomato",
        "disease": "Septoria Leaf Spot",
        "is_healthy": False,
        "cause": "Caused by Septoria lycopersici fungus. Overwinters in infected plant debris. Spreads through rain splash.",
        "symptoms": [
            "Many small circular spots with dark borders",
            "Spots have white-gray centers with dark specks",
            "Begins on lowest leaves progresses upward",
            "Heavy infection causes complete defoliation",
            "Stems and flower stalks rarely affected"
        ],
        "treatment": [
            "Apply mancozeb or chlorothalonil fungicide",
            "Remove all infected leaves immediately",
            "Apply mulch to prevent soil splash onto leaves",
            "Spray every 7-10 days throughout season",
            "Improve drainage around plant base"
        ],
        "prevention": [
            "Remove plant debris thoroughly after harvest",
            "Rotate crops to avoid same spot planting",
            "Stake plants to keep foliage off ground",
            "Water with drip irrigation only",
            "Apply preventive fungicide from transplanting"
        ],
        "recovery_chance": 75,
        "recovery_message": "Good recovery with consistent fungicide treatment. Removing infected leaves stops upward spread.",
        "severity": "Medium",
        "spread_risk": "Medium",
        "treatment_time": "3-4 weeks"
    },

    "Tomato_Spider_mites_Two_spotted_spider_mite": {
        "display_name": "Tomato - Spider Mites",
        "plant": "Tomato",
        "disease": "Spider Mite Infestation",
        "is_healthy": False,
        "cause": "Caused by Tetranychus urticae - a tiny arachnid not a fungus. Thrives in hot dry conditions. Spreads through wind and plant contact.",
        "symptoms": [
            "Tiny yellow or white speckled dots on leaf surface",
            "Fine silky webbing on underside of leaves",
            "Leaves turn bronze yellow then brown",
            "Stippled dusty appearance on upper leaf surface",
            "Severe infestation causes leaves to drop"
        ],
        "treatment": [
            "Spray plants forcefully with water to dislodge mites",
            "Apply insecticidal soap or neem oil spray",
            "Use miticide for severe cases",
            "Introduce predatory mites as biological control",
            "Repeat treatment every 3-5 days for 2-3 weeks"
        ],
        "prevention": [
            "Maintain adequate soil moisture",
            "Regularly mist plant leaves in dry weather",
            "Avoid excessive nitrogen fertilizer",
            "Inspect undersides of leaves weekly",
            "Keep weeds down around plants"
        ],
        "recovery_chance": 82,
        "recovery_message": "Good recovery if treated early. Neem oil and water spraying are very effective.",
        "severity": "Medium",
        "spread_risk": "High",
        "treatment_time": "2-3 weeks"
    },

    "Tomato__Target_Spot": {
        "display_name": "Tomato - Target Spot",
        "plant": "Tomato",
        "disease": "Target Spot",
        "is_healthy": False,
        "cause": "Caused by Corynespora cassiicola fungus. Spreads via airborne spores. Favored by warm temperatures and high humidity.",
        "symptoms": [
            "Circular brown lesions with distinctive concentric rings",
            "Looks similar to a dart target",
            "Yellow halo surrounds the target-like spots",
            "Affects leaves stems and fruits",
            "Small dark raised spots on fruits"
        ],
        "treatment": [
            "Apply azoxystrobin or chlorothalonil fungicide",
            "Remove infected plant material promptly",
            "Improve air circulation by pruning lower leaves",
            "Apply fungicide every 7 days in humid weather",
            "Ensure balanced fertilization to reduce plant stress"
        ],
        "prevention": [
            "Space plants adequately 60cm apart minimum",
            "Stake and prune for good air circulation",
            "Avoid overhead irrigation",
            "Remove crop debris after harvest",
            "Apply preventive fungicide during humid periods"
        ],
        "recovery_chance": 77,
        "recovery_message": "Moderate to good recovery with fungicide treatment. Improving air circulation is essential.",
        "severity": "Medium",
        "spread_risk": "Medium",
        "treatment_time": "2-3 weeks"
    },

    "Tomato__Tomato_YellowLeaf__Curl_Virus": {
        "display_name": "Tomato - Yellow Leaf Curl Virus",
        "plant": "Tomato",
        "disease": "Yellow Leaf Curl Virus",
        "is_healthy": False,
        "cause": "Caused by TYLCV virus transmitted by the whitefly Bemisia tabaci. Cannot spread through soil or tools - only through whitefly feeding.",
        "symptoms": [
            "Upward curling and cupping of young leaves",
            "Yellowing of leaf margins",
            "Stunted bushy plant growth",
            "Significantly reduced fruit production",
            "Flowers may drop without setting fruit"
        ],
        "treatment": [
            "Control whitefly population with insecticide immediately",
            "Apply imidacloprid or thiamethoxam for whiteflies",
            "Use yellow sticky traps to monitor whiteflies",
            "Remove and destroy severely infected plants",
            "There is NO cure - focus on controlling the whitefly"
        ],
        "prevention": [
            "Use TYLCV-resistant tomato varieties",
            "Install insect-proof netting in greenhouses",
            "Apply reflective silver mulch to repel whiteflies",
            "Introduce natural whitefly predators",
            "Remove infected plants immediately to prevent spread"
        ],
        "recovery_chance": 30,
        "recovery_message": "Very low recovery - there is no cure for this virus. Focus on controlling whiteflies.",
        "severity": "High",
        "spread_risk": "High",
        "treatment_time": "No cure - manage vector"
    },

    "Tomato__Tomato_mosaic_virus": {
        "display_name": "Tomato - Mosaic Virus",
        "plant": "Tomato",
        "disease": "Tomato Mosaic Virus",
        "is_healthy": False,
        "cause": "Caused by Tomato Mosaic Virus (ToMV). Spreads through direct contact contaminated hands tools and infected seeds.",
        "symptoms": [
            "Mottled light and dark green mosaic pattern on leaves",
            "Leaves appear blistered or have raised dark areas",
            "Stunted plant growth",
            "Fruits may be discolored with brown streaks",
            "Young leaves may appear narrow and distorted"
        ],
        "treatment": [
            "Remove and destroy all infected plants immediately",
            "There is NO chemical cure for this virus",
            "Disinfect all tools with 1% bleach or 70% alcohol",
            "Wash hands thoroughly before touching healthy plants",
            "Control aphids which may spread the virus"
        ],
        "prevention": [
            "Use certified virus-free seeds and transplants",
            "Use ToMV-resistant tomato varieties",
            "Wash hands before and after handling plants",
            "Avoid using tobacco near plants",
            "Disinfect pots trays and tools before reuse"
        ],
        "recovery_chance": 25,
        "recovery_message": "Very low recovery - no cure exists. Remove infected plants immediately to protect healthy ones.",
        "severity": "High",
        "spread_risk": "Very High",
        "treatment_time": "No cure - remove plant"
    },

    "Tomato_healthy": {
        "display_name": "Tomato - Healthy",
        "plant": "Tomato",
        "disease": "Healthy",
        "is_healthy": True,
        "cause": "No disease detected. Your tomato plant looks perfectly healthy!",
        "symptoms": [
            "Deep green vibrant leaves",
            "No spots lesions or discoloration",
            "Strong stems and healthy growth",
            "Normal flower and fruit development"
        ],
        "treatment": [
            "No treatment needed",
            "Continue regular watering at soil level",
            "Maintain weekly feeding with tomato fertilizer",
            "Keep staking and pruning suckers regularly"
        ],
        "prevention": [
            "Water consistently to avoid drought stress",
            "Feed with potassium-rich fertilizer when fruiting",
            "Inspect leaves weekly top and bottom",
            "Remove yellowing lower leaves promptly"
        ],
        "recovery_chance": 100,
        "recovery_message": "Your tomato plant is in perfect health! Keep up the excellent care routine.",
        "severity": "None",
        "spread_risk": "None",
        "treatment_time": "N/A"
    }
}


def get_disease_info(class_name):
    """Look up disease information by class name"""
    if class_name in DISEASE_KNOWLEDGE:
        return DISEASE_KNOWLEDGE[class_name]

    class_lower = class_name.lower().replace(" ", "_")
    for key in DISEASE_KNOWLEDGE:
        if key.lower().replace(" ", "_") == class_lower:
            return DISEASE_KNOWLEDGE[key]

    for key in DISEASE_KNOWLEDGE:
        if class_lower in key.lower() or key.lower() in class_lower:
            return DISEASE_KNOWLEDGE[key]

    return _default_disease_info(class_name)


def _default_disease_info(class_name):
    """Return default info for unknown diseases"""
    is_healthy = 'healthy' in class_name.lower()
    parts = class_name.replace('___', '_').replace('__', '_').split('_')
    plant = parts[0].capitalize() if parts else 'Unknown'
    return {
        "display_name": class_name.replace('_', ' ').title(),
        "plant": plant,
        "disease": "Unknown Disease",
        "is_healthy": is_healthy,
        "cause": "Detailed information not available for this condition.",
        "symptoms": ["Consult a local agricultural expert for diagnosis"],
        "treatment": ["Consult a plant pathologist or extension service"],
        "prevention": ["Maintain good plant hygiene and regular monitoring"],
        "recovery_chance": 60,
        "recovery_message": "Consult an expert for specific recovery guidance.",
        "severity": "Unknown",
        "spread_risk": "Unknown",
        "treatment_time": "Consult expert"
    }


def get_severity_color(severity):
    """Returns color code based on severity level"""
    colors = {
        "None": "#28a745",
        "Low": "#87c944",
        "Medium": "#ffc107",
        "High": "#fd7e14",
        "Very High": "#dc3545",
        "Unknown": "#6c757d"
    }
    return colors.get(severity, "#6c757d")


def get_recovery_color(recovery_chance):
    """Returns color based on recovery probability"""
    if recovery_chance >= 80:
        return "#28a745"
    elif recovery_chance >= 60:
        return "#ffc107"
    elif recovery_chance >= 40:
        return "#fd7e14"
    else:
        return "#dc3545"


def get_all_diseases():
    """Returns list of all disease names"""
    return list(DISEASE_KNOWLEDGE.keys())


def get_statistics():
    """Returns knowledge base statistics"""
    total = len(DISEASE_KNOWLEDGE)
    healthy = sum(1 for d in DISEASE_KNOWLEDGE.values() if d['is_healthy'])
    avg_recovery = sum(
        d['recovery_chance'] for d in DISEASE_KNOWLEDGE.values()
    ) / total
    return {
        "total_entries": total,
        "healthy_classes": healthy,
        "disease_classes": total - healthy,
        "avg_recovery": round(avg_recovery, 1)
    }