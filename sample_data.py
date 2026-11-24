"""
PlantCare AI - Sample Data & Botanical Knowledge Base
Contains seed plants, encyclopedia library, general care notes,
and manually selected demonstration plant profiles.
"""
from datetime import date, timedelta

TODAY = date.today()

# Pre-seeded sample plants for new accounts and guest mode
SEED_PLANTS = [
    {
        "name": "Monty",
        "species": "Monstera deliciosa (Swiss Cheese Plant)",
        "nickname": "The Jungle King",
        "location": "Living Room Window",
        "age": "1 year 4 months",
        "growth_stage": "Vegetative / Foliage",
        "watering_frequency_days": 7,
        "last_watered_date": (TODAY - timedelta(days=6)).isoformat(),  # Due tomorrow/soon
        "sunlight": "Bright Indirect Light",
        "humidity": "Moderate to High (60%+)",
        "fertilization_frequency_weeks": 4,
        "last_fertilized_date": (TODAY - timedelta(days=22)).isoformat(),
        "fertilizer_type": "Balanced 10-10-10 Liquid Fertilizer",
        "has_flowers": 0,
        "flowers_info": "Rarely blooms indoors; requires warm tropical greenhouse conditions to produce spathes.",
        "has_fruits": 0,
        "fruits_info": "Not fruiting indoors. In wild habitats produces edible monster-fruit when fully ripened.",
        "harvest_info": "Foliage ornamental plant. Clean large fenestrated leaves monthly with a damp microfiber cloth.",
        "image_preset": "monstera",
        "notes": "Loves moss pole climbing. Currently unfurling a new leaf with 5 fenestrations!"
    },
    {
        "name": "Luna",
        "species": "Sansevieria trifasciata (Snake Plant / Mother-in-Law's Tongue)",
        "nickname": "Indestructible Luna",
        "location": "Bedroom Nightstand",
        "age": "2 years",
        "growth_stage": "Mature",
        "watering_frequency_days": 18,
        "last_watered_date": (TODAY - timedelta(days=20)).isoformat(),  # Overdue for water!
        "sunlight": "Low to Medium Indirect Light",
        "humidity": "Low / Average Home Humidity (30-40%)",
        "fertilization_frequency_weeks": 8,
        "last_fertilized_date": (TODAY - timedelta(days=50)).isoformat(),
        "fertilizer_type": "Mild Cactus & Succulent Feed (half strength)",
        "has_flowers": 0,
        "flowers_info": "Produces subtle fragrant greenish-white flower stalks when root-bound in spring.",
        "has_fruits": 0,
        "fruits_info": "Non-fruiting ornamental.",
        "harvest_info": "Not for harvest. Air-purifying champion that releases oxygen at night.",
        "image_preset": "snake_plant",
        "notes": "Very drought tolerant. Always allow soil to dry completely before watering."
    },
    {
        "name": "Sunny",
        "species": "Solanum lycopersicum (Sweet 100 Cherry Tomato)",
        "nickname": "Balcony Snacker",
        "location": "Sunny Balcony Terrace",
        "age": "3 months",
        "growth_stage": "Fruiting",
        "watering_frequency_days": 2,
        "last_watered_date": (TODAY - timedelta(days=2)).isoformat(),  # Due today!
        "sunlight": "Direct Sunlight (6-8 hours daily)",
        "humidity": "Moderate (45-60%)",
        "fertilization_frequency_weeks": 2,
        "last_fertilized_date": (TODAY - timedelta(days=15)).isoformat(),  # Overdue fertilizer
        "fertilizer_type": "High-Potassium & Calcium Tomato Food",
        "has_flowers": 1,
        "flowers_info": "Bright yellow self-pollinating star flowers blooming along top trusses.",
        "has_fruits": 1,
        "fruits_info": "18 small round green and orange-blush cherry tomatoes developing.",
        "harvest_info": "Harvest when tomatoes turn deep scarlet red and release easily with a gentle twist.",
        "image_preset": "tomato",
        "notes": "Staked with bamboo canes. Check daily for suckers between main stem and branches."
    },
    {
        "name": "Aroma Basil",
        "species": "Ocimum basilicum (Genovese Italian Basil)",
        "nickname": "Pesto Power",
        "location": "Kitchen Windowsill",
        "age": "7 weeks",
        "growth_stage": "Vegetative / Harvesting",
        "watering_frequency_days": 3,
        "last_watered_date": (TODAY - timedelta(days=1)).isoformat(),  # Good
        "sunlight": "Bright Morning Sun (4-6 hours)",
        "humidity": "Moderate (50%)",
        "fertilization_frequency_weeks": 3,
        "last_fertilized_date": (TODAY - timedelta(days=7)).isoformat(),
        "fertilizer_type": "Organic Seaweed & Fish Emulsion Extract",
        "has_flowers": 0,
        "flowers_info": "Pinch off flower buds as soon as they appear to preserve leaf aromatic oils and sweetness.",
        "has_fruits": 0,
        "fruits_info": "Herbaceous culinary plant (no edible fruits).",
        "harvest_info": "Harvest top pairs of leaves right above a leaf node to stimulate bushy double-stem growth.",
        "image_preset": "basil",
        "notes": "Harvested 12 fresh leaves for homemade margarita pizza last weekend!"
    }
]

# Sample growth history for pre-seeded plants
SEED_GROWTH_HISTORY = [
    {
        "plant_name": "Monty",
        "log_date": (TODAY - timedelta(days=60)).isoformat(),
        "height_cm": 45.0,
        "leaf_count": 6,
        "stage": "Vegetative",
        "milestone": "Repotted into 10-inch terracotta pot with airy aroid soil mix (bark + perlite)."
    },
    {
        "plant_name": "Monty",
        "log_date": (TODAY - timedelta(days=20)).isoformat(),
        "height_cm": 58.0,
        "leaf_count": 8,
        "stage": "Vegetative",
        "milestone": "Mounted new coir moss pole. First leaf with double fenestrations opened!"
    },
    {
        "plant_name": "Sunny",
        "log_date": (TODAY - timedelta(days=40)).isoformat(),
        "height_cm": 25.0,
        "leaf_count": 14,
        "stage": "Flowering",
        "milestone": "First cluster of bright yellow flowers opened on top branch."
    },
    {
        "plant_name": "Sunny",
        "log_date": (TODAY - timedelta(days=10)).isoformat(),
        "height_cm": 62.0,
        "leaf_count": 28,
        "stage": "Fruiting",
        "milestone": "First 6 green cherry tomatoes formed! Staked with support ties."
    }
]

# Botanical Plant Encyclopedia Library (12 diverse popular species)
PLANT_ENCYCLOPEDIA = [
    {
        "name": "Monstera Deliciosa",
        "species": "Monstera deliciosa",
        "category": "Indoor Foliage",
        "difficulty": "Beginner Friendly",
        "watering_frequency_days": 7,
        "watering_summary": "Water when top 2-3 inches of soil dry out. Avoid soggy roots.",
        "sunlight": "Bright Indirect Light",
        "humidity": "Moderate to High (55-70%)",
        "fertilization_frequency_weeks": 4,
        "fertilizer_recommendation": "Balanced 10-10-10 foliage houseplant feed in spring/summer.",
        "growth_stages": "Seedling -> Vegetative -> Fenestrated Mature",
        "has_flowers": "Rare indoors",
        "has_fruits": "Only in wild tropics",
        "harvest_info": "Ornamental plant. Prune yellowed lower stems to maintain vigorous growth.",
        "pet_safe": "Toxic to cats & dogs (contains calcium oxalate crystals)",
        "propagation": "Stem cuttings with at least one node and aerial root in water.",
        "description": "Famous for iconic split leaves and tropical presence. Tolerant of missed waterings."
    },
    {
        "name": "Snake Plant (Sansevieria)",
        "species": "Sansevieria trifasciata",
        "category": "Succulent & Air Purifying",
        "difficulty": "Easiest (Unkillable)",
        "watering_frequency_days": 18,
        "watering_summary": "Thrives on neglect. Allow soil to dry 100% between thorough waterings.",
        "sunlight": "Low to Bright Indirect Light",
        "humidity": "Low / Any (30-50%)",
        "fertilization_frequency_weeks": 8,
        "fertilizer_recommendation": "Half-strength cactus food once every two months.",
        "growth_stages": "Slow grower; produces vertical upright architectural spears.",
        "has_flowers": "Rarely produces sweet-scented greenish bloom stalks when mature.",
        "has_fruits": "None indoors",
        "harvest_info": "Not edible. Architectural air-cleaning ornamental.",
        "pet_safe": "Mildly toxic to pets if chewed",
        "propagation": "Leaf cuttings in soil/water or rhizome division when repotting.",
        "description": "Ideal beginner plant. Purifies indoor air and survives low light and erratic care."
    },
    {
        "name": "Golden Pothos (Devil's Ivy)",
        "species": "Epipremnum aureum",
        "category": "Trailing Vine",
        "difficulty": "Beginner Friendly",
        "watering_frequency_days": 6,
        "watering_summary": "Water when top 50% of potting mix feels dry. Leaves droop slightly when thirsty.",
        "sunlight": "Low to Bright Indirect Light",
        "humidity": "Moderate (40-60%)",
        "fertilization_frequency_weeks": 4,
        "fertilizer_recommendation": "General houseplant fertilizer once monthly in growing season.",
        "growth_stages": "Fast trailing vine reaching 6-10 feet.",
        "has_flowers": "Does not bloom indoors",
        "has_fruits": "None indoors",
        "harvest_info": "Trim vine tips regularly to encourage bushy, fuller pot growth.",
        "pet_safe": "Toxic to pets (calcium oxalates)",
        "propagation": "Super easy. Root 4-6 inch node cuttings in a jar of water within 10 days.",
        "description": "Hardy trailing vine with marbled heart-shaped green and gold leaves."
    },
    {
        "name": "Fiddle Leaf Fig",
        "species": "Ficus lyrata",
        "category": "Indoor Statement Tree",
        "difficulty": "Intermediate",
        "watering_frequency_days": 8,
        "watering_summary": "Sensitive to overwatering. Water thoroughly only when top 2 inches dry.",
        "sunlight": "Bright, Filtered Sunlight (Must have consistent light)",
        "humidity": "Moderate to High (50-65%)",
        "fertilization_frequency_weeks": 4,
        "fertilizer_recommendation": "High nitrogen (3-1-2 ratio) liquid plant food during active growth.",
        "growth_stages": "Sapling -> Branched Indoor Tree (up to 8 feet tall)",
        "has_flowers": "No indoor flowering",
        "has_fruits": "Non-fruiting indoors",
        "harvest_info": "Prune apical bud to encourage lateral branch canopy development.",
        "pet_safe": "Toxic to pets (sap irritates skin and mouth)",
        "propagation": "Stem tip cuttings or air-layering in warm spring.",
        "description": "Sculptural tree with broad violin-shaped leaves that make a dramatic focal point."
    },
    {
        "name": "ZZ Plant (Zanzibar Gem)",
        "species": "Zamioculcas zamiifolia",
        "category": "Foliage / Low Light",
        "difficulty": "Easiest",
        "watering_frequency_days": 16,
        "watering_summary": "Stores water in underground potato-like rhizomes. Water sparingly.",
        "sunlight": "Low Light to Bright Indirect",
        "humidity": "Low to Normal Home Humidity",
        "fertilization_frequency_weeks": 8,
        "fertilizer_recommendation": "Diluted balanced liquid fertilizer 2-3 times per year.",
        "growth_stages": "Slow steady growth with glossy composite leaflets.",
        "has_flowers": "Rarely produces a small spadix at soil level.",
        "has_fruits": "None",
        "harvest_info": "Wipe shiny leaves with water to keep photosynthetic pores dust-free.",
        "pet_safe": "Toxic if ingested by pets",
        "propagation": "Divide underground potato rhizomes or individual leaf stems.",
        "description": "Ultra glossy, feather-like stems. Forgives dark corners and forgotten waterings."
    },
    {
        "name": "Peace Lily",
        "species": "Spathiphyllum wallisii",
        "category": "Flowering Houseplant",
        "difficulty": "Beginner Friendly",
        "watering_frequency_days": 5,
        "watering_summary": "Loves consistently moist (not soggy) soil. Dramatically droops when dry.",
        "sunlight": "Medium to Bright Indirect Light (tolerates low light)",
        "humidity": "High (60%+)",
        "fertilization_frequency_weeks": 6,
        "fertilizer_recommendation": "Balanced blooming houseplant fertilizer diluted to quarter strength.",
        "growth_stages": "Clump-forming glossy evergreen with upright white flowers.",
        "has_flowers": "Yes, elegant pure-white spathes bloom repeatedly in spring and summer.",
        "has_fruits": "None indoors",
        "harvest_info": "Trim spent flower stems down at the base to spur new blooms.",
        "pet_safe": "Toxic to pets (oral irritation)",
        "propagation": "Easy root ball division during spring repotting.",
        "description": "Communicates thirst clearly by drooping and bounces back rapidly after watering."
    },
    {
        "name": "Sweet Italian Basil",
        "species": "Ocimum basilicum",
        "category": "Edible Herb",
        "difficulty": "Beginner Friendly",
        "watering_frequency_days": 3,
        "watering_summary": "Keep soil evenly moist. Prefers bottom watering to prevent fungal issues.",
        "sunlight": "Full Direct Sun (6+ hours daily)",
        "humidity": "Moderate (45-55%)",
        "fertilization_frequency_weeks": 2,
        "fertilizer_recommendation": "Organic fish/seaweed emulsion or balanced vegetable feed.",
        "growth_stages": "Seedling -> Branching Bush -> Harvestable Herb",
        "has_flowers": "Produces small white flower spikes (pinch them off to extend leaf harvest).",
        "has_fruits": "None (herb)",
        "harvest_info": "Snip top clusters above two leaf nodes weekly. Yields abundant leaves for pesto.",
        "pet_safe": "100% Non-toxic & safe for pets",
        "propagation": "Stem tip cuttings root vigorously in water within 5-7 days.",
        "description": "Aromatic culinary staple for windowsill gardens and fresh pasta, pizza, and salads."
    },
    {
        "name": "Cherry Tomato (Sweet 100)",
        "species": "Solanum lycopersicum",
        "category": "Edible Fruit / Vegetable",
        "difficulty": "Intermediate",
        "watering_frequency_days": 2,
        "watering_summary": "Deep, consistent watering. Uneven watering causes fruit splitting/blossom end rot.",
        "sunlight": "Full Direct Sun (8+ hours daily)",
        "humidity": "Moderate (50-65%)",
        "fertilization_frequency_weeks": 2,
        "fertilizer_recommendation": "Tomato fertilizer rich in potassium and calcium once fruit sets.",
        "growth_stages": "Seedling -> Vegetative -> Flowering -> Green Fruit -> Ripe Fruit",
        "has_flowers": "Clusters of bright yellow star-shaped pollinator flowers.",
        "has_fruits": "Clusters of sweet, juicy, cherry-sized round red tomatoes.",
        "harvest_info": "Pick when uniform red and firm. Best flavor picked warm in late afternoon.",
        "pet_safe": "Leaves & stems are toxic to pets; ripe fruit is safe in moderation.",
        "propagation": "Grow from seed or root side shoot suckers.",
        "description": "High-yield producer for sunny balconies, patios, and container vegetable gardens."
    },
    {
        "name": "Aloe Vera",
        "species": "Aloe barbadensis Miller",
        "category": "Medicinal Succulent",
        "difficulty": "Easiest",
        "watering_frequency_days": 14,
        "watering_summary": "Water deeply then allow completely dry soil. Reduce to once monthly in winter.",
        "sunlight": "Bright Direct to Filtered Sun",
        "humidity": "Low Humidity (dry air preferred)",
        "fertilization_frequency_weeks": 8,
        "fertilizer_recommendation": "Light cactus fertilizer once in spring and once in summer.",
        "growth_stages": "Rosette of plump serrated leaves with internal soothing gel.",
        "has_flowers": "Tubular yellow/orange blossoms on tall central spikes in mature outdoor plants.",
        "has_fruits": "None indoors",
        "harvest_info": "Cut lower thickest outer leaves for natural soothing skin aloe gel.",
        "pet_safe": "Toxic to pets if chewed (aloins cause upset stomach)",
        "propagation": "Separate baby 'pups' that sprout at the base with their own roots.",
        "description": "Beloved medicinal succulent that thrives in sunny windows with minimal attention."
    },
    {
        "name": "Spider Plant",
        "species": "Chlorophytum comosum",
        "category": "Hanging Basket / Air Purifier",
        "difficulty": "Beginner Friendly",
        "watering_frequency_days": 6,
        "watering_summary": "Water when top 1 inch is dry. Use filtered water to prevent brown leaf tips.",
        "sunlight": "Bright Indirect Light",
        "humidity": "Moderate (40-60%)",
        "fertilization_frequency_weeks": 4,
        "fertilizer_recommendation": "Standard liquid houseplant food diluted by half.",
        "growth_stages": "Arching ribbon foliage -> Long runner stolons with plantlets.",
        "has_flowers": "Tiny star-shaped white blossoms on long arching stems.",
        "has_fruits": "None",
        "harvest_info": "Trim off baby spider plantlets to propagate new independent plants.",
        "pet_safe": "100% Non-toxic & pet safe (has mild calming catnip-like effect on cats)",
        "propagation": "Clip off dangling plantlets and root in water or moist soil immediately.",
        "description": "Resilient arching variegated ribbons that send out playful dangling baby spiderettes."
    },
    {
        "name": "English Lavender",
        "species": "Lavandula angustifolia",
        "category": "Aromatic Flower / Herb",
        "difficulty": "Intermediate",
        "watering_frequency_days": 7,
        "watering_summary": "Drought hardy once established. Requires gritty, well-draining soil.",
        "sunlight": "Full Direct Sun (6-8 hours daily)",
        "humidity": "Low Humidity (hates stuffy, humid conditions)",
        "fertilization_frequency_weeks": 6,
        "fertilizer_recommendation": "Minimal feeding needed; excess nitrogen diminishes fragrance.",
        "growth_stages": "Woody perennial shrub with silvery foliage and purple flower spikes.",
        "has_flowers": "Fragrant purple spikes blooming continuously from late spring to summer.",
        "has_fruits": "Small seeds",
        "harvest_info": "Cut flower stems when bottom third of florets open. Hang upside down to dry.",
        "pet_safe": "Mildly toxic to pets in large quantities (contains linalool)",
        "propagation": "Semi-hardwood cuttings taken in late summer.",
        "description": "Classic Mediterranean aromatic herb known for soothing floral scent and pollinator magnetism."
    },
    {
        "name": "String of Pearls",
        "species": "Senecio rowleyanus",
        "category": "Trailing Succulent",
        "difficulty": "Intermediate",
        "watering_frequency_days": 12,
        "watering_summary": "Water when the small translucent 'leaf windows' on the beads narrow/pucker.",
        "sunlight": "Bright Indirect Light with some gentle morning sun",
        "humidity": "Low Humidity",
        "fertilization_frequency_weeks": 6,
        "fertilizer_recommendation": "Succulent fertilizer at 1/4 strength during spring.",
        "growth_stages": "Cascading bead-like spherical succulent leaves.",
        "has_flowers": "Cinnamon-scented tiny brush-like white flowers in winter.",
        "has_fruits": "None",
        "harvest_info": "Coil long stems on top of the soil to root and create a denser, fuller top crown.",
        "pet_safe": "Toxic to pets (can cause vomiting and lethargy)",
        "propagation": "Lay stem cuttings flat across moist succulent soil.",
        "description": "Charming succulent trailing bead necklaces over shelves and hanging macramé pots."
    }
]

# General plant-care reference notes; they are not image-based diagnoses.
PLANT_DOCTOR_KNOWLEDGE = [
    {
        "issue": "Overwatering & Poor Drainage",
        "symptoms": ["Yellowing lower leaves", "Soft mushy stems", "Soil stays wet for over 10 days", "Fungus gnats near soil"],
        "severity": "High",
        "root_cause": "Roots are suffocated by standing water without oxygen, creating anaerobic fungal conditions.",
        "safe_guidance": [
            "Stop watering immediately and allow the root zone to dry out.",
            "Verify that the pot has unobstructed drainage holes at the bottom.",
            "Aerify the soil gently using a wooden chopstick around the root perimeter.",
            "If severe, unpot the plant, inspect for brown mushy roots, trim them with sterilized scissors, and repot in fresh airy potting mix."
        ]
    },
    {
        "issue": "Underwatering / Chronic Dehydration",
        "symptoms": ["Limp drooping stems", "Dry crispy brown leaf tips", "Soil pulled away from pot edges", "Curling inward leaves"],
        "severity": "Medium",
        "root_cause": "Plant has expended cellular moisture and capillary pressure has collapsed.",
        "safe_guidance": [
            "Give the plant a gentle, thorough bottom-watering bath: set pot in a shallow bowl of room-temperature water for 25 minutes.",
            "Let excess water drain out completely before returning to saucer.",
            "Establish a routine reminder schedule using PlantCare AI's watering notifications.",
            "Avoid placing plant directly in hot heat vents or air conditioning drafts."
        ]
    },
    {
        "issue": "Low Humidity & Dry Air",
        "symptoms": ["Brown crispy leaf margins", "Unfurling leaves get stuck or tear", "Brittle new shoots"],
        "severity": "Low to Medium",
        "root_cause": "Indoor heating or AC drops ambient humidity below tropical plant tolerance (under 40%).",
        "safe_guidance": [
            "Group humidity-loving plants together to create a natural micro-climate transpirational dome.",
            "Place a shallow pebble tray filled with water beneath the pot (keep pot bottom above water line).",
            "Use a room cool-mist ultrasonic humidifier nearby during winter heating periods.",
            "Avoid misting fuzzy-leaved plants like African Violets directly to prevent fungal leaf spotting."
        ]
    },
    {
        "issue": "Spider Mites (Tetranychidae)",
        "symptoms": ["Fine dusty webbing between leaf stems", "Tiny yellow/bronze stippling speckles on leaf surfaces", "Dull fading foliage"],
        "severity": "Medium",
        "root_cause": "Microscopic sap-sucking arachnids that proliferate in warm, dry indoor air.",
        "safe_guidance": [
            "Quarantine the infested plant away from other plants to stop spread.",
            "Take the plant to the shower or sink and rinse the undersides of leaves thoroughly with lukewarm water spray.",
            "Spray leaves thoroughly with a gentle solution of mild castile soap or cold-pressed organic neem oil (1 tsp neem + 1/2 tsp soap per quart warm water).",
            "Repeat the safe treatment every 5-7 days for 3 weeks to break the egg hatching cycle."
        ]
    },
    {
        "issue": "Powdery Mildew Fungal Infection",
        "symptoms": ["White talcum-like powdery spots on upper leaf surfaces", "Distorted new growth", "Premature leaf drop"],
        "severity": "Medium",
        "root_cause": "Fungal spores taking advantage of poor air circulation and high humidity with cool night temperatures.",
        "safe_guidance": [
            "Isolate the plant and snip off heavily coated leaves with clean garden shears.",
            "Wipe mildly affected leaves with a gentle organic solution: 1 part milk to 9 parts water, or 1 tsp baking soda + 1/2 tsp horticultural oil in 1 quart water.",
            "Increase air circulation around the plant using a gentle oscillating room fan.",
            "Water soil directly without wetting the upper foliage."
        ]
    },
    {
        "issue": "Nutrient Deficiency (Nitrogen or Micronutrients)",
        "symptoms": ["Overall pale lime-green foliage", "Stunted new leaf growth", "Interveinal chlorosis (yellow leaves with dark green veins)"],
        "severity": "Low",
        "root_cause": "Soil nutrient reserves are depleted after months of watering and active growth.",
        "safe_guidance": [
            "Apply a balanced, water-soluble organic liquid fertilizer diluted to half label strength.",
            "For acid-loving or iron-deficient plants, apply chelated iron or organic worm castings top-dressing.",
            "Never apply fertilizer to bone-dry soil; always moisten soil with plain water first to avoid root fertilizer burn.",
            "Check that soil pH is within the optimal absorption range (6.0 - 6.8 for most houseplants)."
        ]
    },
    {
        "issue": "Sunburn / Light Scorch",
        "symptoms": ["Bleached white or crispy dark brown scorched patches on leaves facing the window", "Colors look washed out"],
        "severity": "Low to Medium",
        "root_cause": "Intense direct midday solar radiation exceeding the plant's light adaptation capacity.",
        "safe_guidance": [
            "Move the plant 2 to 4 feet back from south- or west-facing glass windows.",
            "Hang a sheer white curtain to diffuse direct UV rays into soft bright indirect light.",
            "Damaged leaf tissue cannot turn green again; you may trim dried scorched edges with clean scissors for aesthetics.",
            "Acclimate plants gradually over 2 weeks when shifting to higher light locations."
        ]
    }
]

# Manually selected example profiles; they are not generated from uploaded images.
DEMO_ID_PRESETS = {
    "monstera": {
        "species_name": "Monstera deliciosa",
        "common_name": "Swiss Cheese Plant / Split-Leaf Philodendron",
        "family": "Araceae",
        "leaf_features": "Broad glossy cordate leaves with characteristic natural perforated fenestrations.",
        "growth_habit": "Climbing evergreen epiphyte with aerial adventitious roots.",
        "care_quick_match": {
            "watering_days": 7,
            "sunlight": "Bright Indirect Light",
            "humidity": "Moderate to High",
            "fertilizer_weeks": 4
        }
    },
    "snake_plant": {
        "species_name": "Sansevieria trifasciata",
        "common_name": "Snake Plant / Mother-in-Law's Tongue",
        "family": "Asparagaceae",
        "leaf_features": "Erect, rigid sword-shaped succulent foliage with horizontal grey-green banding and yellow margins.",
        "growth_habit": "Upright architectural clumping succulent from rhizomatous base.",
        "care_quick_match": {
            "watering_days": 18,
            "sunlight": "Low to Bright Indirect",
            "humidity": "Low / Average",
            "fertilizer_weeks": 8
        }
    },
    "pothos": {
        "species_name": "Epipremnum aureum",
        "common_name": "Golden Pothos / Devil's Ivy",
        "family": "Araceae",
        "leaf_features": "Heart-shaped glossy foliage with distinct yellow-cream variegation and trailing nodes.",
        "growth_habit": "Vigorous cascading and climbing vining habit.",
        "care_quick_match": {
            "watering_days": 6,
            "sunlight": "Low to Bright Indirect",
            "humidity": "Moderate",
            "fertilizer_weeks": 4
        }
    },
    "ficus": {
        "species_name": "Ficus lyrata",
        "common_name": "Fiddle Leaf Fig",
        "family": "Moraceae",
        "leaf_features": "Heavily veined, broad lyre-shaped leathery leaves with wavy margins.",
        "growth_habit": "Upright branching banyan tree.",
        "care_quick_match": {
            "watering_days": 8,
            "sunlight": "Bright Filtered Light",
            "humidity": "Moderate to High",
            "fertilizer_weeks": 4
        }
    },
    "tomato": {
        "species_name": "Solanum lycopersicum",
        "common_name": "Garden Cherry Tomato",
        "family": "Solanaceae",
        "leaf_features": "Pinnately compound aromatic glandular leaves with toothed margins and yellow star blossoms.",
        "growth_habit": "Vigorous herbaceous flowering and fruiting vine requiring staking.",
        "care_quick_match": {
            "watering_days": 2,
            "sunlight": "Full Direct Sunlight",
            "humidity": "Moderate",
            "fertilizer_weeks": 2
        }
    },
    "basil": {
        "species_name": "Ocimum basilicum",
        "common_name": "Genovese Sweet Basil",
        "family": "Lamiaceae",
        "leaf_features": "Opposite ovate glossy tender green leaves emitting sweet clove-anise essential oils.",
        "growth_habit": "Branching herbaceous aromatic annual.",
        "care_quick_match": {
            "watering_days": 3,
            "sunlight": "Full Direct Sun",
            "humidity": "Moderate",
            "fertilizer_weeks": 3
        }
    }
}
