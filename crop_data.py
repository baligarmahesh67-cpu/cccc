"""Editable crop profiles for the demonstrator.

Important: rainfall intervals are prototype ranking heuristics, not official
agronomic thresholds. Crop choice must be localized by district, soil test,
variety, planting date and current advisories before real farm use.
"""

CROP_PROFILES = [
    {
        "name": "Paddy (Rice)",
        "soil_types": ["alluvial", "clay", "loamy"],
        "seasons": ["Kharif"],
        "rainfall_mm": [1000, 2500],
        "water": ["high"],
        "description": "A candidate for suitable fields with reliable water availability.",
        "evidence": "ICAR's Karnataka advisory describes paddy sowing mainly from June to August and notes that much of the state's paddy area is irrigated.",
        "source": "https://icar.gov.in/en/icar-kharif-agro-advisories-farmers-2025",
    },
    {
        "name": "Finger Millet (Ragi)",
        "soil_types": ["red", "laterite", "loamy"],
        "seasons": ["Kharif"],
        "rainfall_mm": [450, 1200],
        "water": ["low", "moderate"],
        "description": "A rainfed millet candidate commonly grown in Karnataka.",
        "evidence": "ICAR's Karnataka advisory lists June-July sowing and rainfed cultivation for finger millet.",
        "source": "https://icar.gov.in/en/icar-kharif-agro-advisories-farmers-2025",
    },
    {
        "name": "Maize",
        "soil_types": ["red", "black", "alluvial", "loamy"],
        "seasons": ["Kharif", "Rabi", "Summer"],
        "rainfall_mm": [400, 1200],
        "water": ["moderate", "high"],
        "description": "A versatile cereal candidate; irrigation needs vary with soil and season.",
        "evidence": "ICAR's Karnataka advisory describes Kharif sowing around May-July and Rabi sowing around September-October, with irrigation intervals differing by soil.",
        "source": "https://icar.gov.in/en/icar-kharif-agro-advisories-farmers-2025",
    },
    {
        "name": "Pigeonpea (Red Gram / Tur)",
        "soil_types": ["red", "black", "loamy"],
        "seasons": ["Kharif"],
        "rainfall_mm": [500, 1100],
        "water": ["low", "moderate"],
        "description": "A pulse crop candidate; intercropping options may be considered locally.",
        "evidence": "ICAR identifies pigeonpea among important Karnataka crops and discusses pigeonpea-based intercropping and moisture conservation.",
        "source": "https://www.icar.gov.in/en/node/17269",
    },
    {
        "name": "Groundnut",
        "soil_types": ["red", "sandy", "loamy"],
        "seasons": ["Kharif", "Summer"],
        "rainfall_mm": [450, 1100],
        "water": ["low", "moderate"],
        "description": "An oilseed candidate; sow only when adequate moisture is available.",
        "evidence": "ICAR's Karnataka advisory mentions groundnut in red-soil moisture-conservation systems and cautions against dry sowing without sufficient root-zone moisture.",
        "source": "https://icar.gov.in/en/icar-kharif-agro-advisories-farmers-2025",
    },
    {
        "name": "Sorghum (Jowar)",
        "soil_types": ["black", "red", "loamy"],
        "seasons": ["Kharif", "Rabi"],
        "rainfall_mm": [300, 900],
        "water": ["low", "moderate"],
        "description": "A millet/cereal candidate included among Karnataka's important crops.",
        "evidence": "ICAR lists sorghum among important crops grown in Karnataka.",
        "source": "https://www.icar.gov.in/en/node/17269",
    },
    {
        "name": "Sunflower",
        "soil_types": ["black", "red", "loamy"],
        "seasons": ["Kharif", "Rabi"],
        "rainfall_mm": [300, 900],
        "water": ["low", "moderate"],
        "description": "An oilseed candidate; local sowing windows and varieties need confirmation.",
        "evidence": "ICAR lists sunflower among important crops in Karnataka.",
        "source": "https://www.icar.gov.in/en/node/17269",
    },
    {
        "name": "Safflower",
        "soil_types": ["black", "loamy"],
        "seasons": ["Rabi"],
        "rainfall_mm": [250, 700],
        "water": ["low"],
        "description": "A low-water oilseed candidate for suitable local conditions.",
        "evidence": "ICAR lists safflower among important crops in Karnataka.",
        "source": "https://www.icar.gov.in/en/node/17269",
    },
]

SOIL_TYPES = ["red", "black", "alluvial", "clay", "sandy", "loamy", "laterite"]
SEASONS = ["Kharif", "Rabi", "Summer"]
WATER_LEVELS = ["low", "moderate", "high"]
