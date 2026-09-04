import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import skew
import json
import os
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="National Parks Optimizer | Regular 39-Year-Old Guys June Expedition",
    page_icon="🌲",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- PERSISTENCE ENGINE (VOTES & COMMENTS STORED TO JSON) ---
DATA_FILE = "trip_records.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"votes": {}, "comments": []}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"votes": {}, "comments": []}

def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        st.error(f"Error saving data: {e}")

# --- IMAGE CONSTANTS ---
IMG_SIDEBAR = "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?auto=format&fit=crop&w=600&q=80"
IMG_TETON_MAIN = "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&w=1200&q=80"
IMG_GLACIER_MAIN = "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=80"
IMG_ZION_MAIN = "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?auto=format&fit=crop&w=1200&q=80"
IMG_DENALI_MAIN = "https://images.unsplash.com/photo-1517411032315-54ef2cb783bb?auto=format&fit=crop&w=1200&q=80"
IMG_KENAI_MAIN = "https://images.unsplash.com/photo-1483728642387-6c3bdd6c93e5?auto=format&fit=crop&w=1200&q=80"
IMG_OLYMPIC_MAIN = "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&w=1200&q=80"
IMG_RAINIER_MAIN = "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=1200&q=80"
IMG_CASCADES_MAIN = "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1200&q=80"
IMG_YOSEMITE_MAIN = "https://images.unsplash.com/photo-1426604966848-d7adac402bff?auto=format&fit=crop&w=1200&q=80"
IMG_ROCKY_MAIN = "https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=1200&q=80"

IMG_TRAIL_1 = "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=600&q=80"
IMG_TRAIL_2 = "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?auto=format&fit=crop&w=600&q=80"
IMG_TRAIL_3 = "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?auto=format&fit=crop&w=600&q=80"
IMG_TRAIL_4 = "https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=600&q=80"
IMG_TRAIL_5 = "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=600&q=80"
IMG_TRAIL_6 = "https://images.unsplash.com/photo-1513836279014-a89f7a76ae86?auto=format&fit=crop&w=600&q=80"
IMG_TRAIL_7 = "https://images.unsplash.com/photo-1527489377706-5bf97e608852?auto=format&fit=crop&w=600&q=80"
IMG_TRAIL_8 = "https://images.unsplash.com/photo-1531366936337-7c912a4589a7?auto=format&fit=crop&w=600&q=80"
IMG_TRAIL_9 = "https://images.unsplash.com/photo-1473448912268-2022ce9509d8?auto=format&fit=crop&w=600&q=80"
IMG_TRAIL_10 = "https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=600&q=80"
IMG_TRAIL_11 = "https://images.unsplash.com/photo-1518457607834-6e8d80c183c5?auto=format&fit=crop&w=600&q=80"
IMG_TRAIL_12 = "https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?auto=format&fit=crop&w=600&q=80"
IMG_TRAIL_13 = "https://images.unsplash.com/photo-1511497584788-87676104235f?auto=format&fit=crop&w=600&q=80"
IMG_TRAIL_14 = "https://images.unsplash.com/photo-1432405972618-c60b0225b8f9?auto=format&fit=crop&w=600&q=80"

# --- DATA REGISTRY ---
PARK_DATA = {
    "Grand Teton": {
        "state": "Wyoming",
        "airport": "JAC (Jackson) / BZN",
        "drive_hrs": 0.5,
        "flights": {"SEA": 320, "ORD": 490, "COU": 620},
        "car_rental_total": 850,
        "in_park_lodge_prob": "Low (<25% inside park; Jenny Lake & Colter Bay book out 6-12 months prior)",
        "gateway_lodge_prob": "High (80% inventory in Jackson, Wilson, or Teton Village)",
        "lodge_cost_night": 450,
        "camp_cost_night": 40,
        "passes_entry": "America the Beautiful ($80/vehicle) or 7-Day Park Pass ($35).",
        "timed_entry": "None required for vehicle entry.",
        "wildlife_score": 9.5,
        "scenery_score": 9.8,
        "june_viability": 8.0,
        "banner_img": IMG_TETON_MAIN,
        "wildlife_risk": {
            "bear_tier": "High (Grizzly & Black Bear)",
            "bear_attack_prob": "0.045% (High relative density; June sow/cub foraging)",
            "moose_tier": "Very High",
            "moose_attack_prob": "0.060% (High density in Willow Flats / Cascade creek; calving season)",
            "risk_mitigation": "Bear spray mandatory on person; travel in tight group of 5; maintain 100 yds from bears, 25 yds from moose."
        },
        "weather_profile": {
            "p_moderate_temp": "75% (Avg highs 68°F–75°F; valley nights 38°F–44°F)",
            "p_clear_skies": "65% (Sunny mornings; afternoon cumulus buildups)",
            "peril_thunderstorms": "35% (Daily 2 PM–6 PM convective lightning hazard on passes)",
            "peril_hypothermia": "20% (Early June cold rain/snow above 8,500 ft)",
            "peril_excessive_heat": "<5% (Valley rarely exceeds 84°F in June)"
        },
        "hikes": [
            {
                "day": "Monday",
                "name": "Cascade Canyon to Forks",
                "miles": 9.6,
                "gain": 1120,
                "vistas": "Glacial canyon walls, Hidden Falls, soaring crags, moose willow marshes.",
                "can_overnight": True,
                "backcountry_permit": "Grand Teton Wilderness Permit ($20 + $7/person/night). Bear canister required.",
                "img": IMG_TRAIL_1
            },
            {
                "day": "Wednesday",
                "name": "Taggart & Bradley Lakes Loop",
                "miles": 5.5,
                "gain": 780,
                "vistas": "Subalpine tarn reflections of Grand Teton. Completely snow-free by June.",
                "can_overnight": False,
                "backcountry_permit": "Day hike only. Frontcountry trail.",
                "img": IMG_TRAIL_2
            },
            {
                "day": "Friday",
                "name": "Delta Lake via Amphitheater Trail",
                "miles": 8.2,
                "gain": 2350,
                "vistas": "Glacial turquoise lake below the north face. Strenuous boulder scramble.",
                "can_overnight": False,
                "backcountry_permit": "Day scramble. Camping prohibited directly at Delta Lake.",
                "img": IMG_TRAIL_3
            }
        ]
    },
    "Glacier": {
        "state": "Montana",
        "airport": "FCA (Kalispell)",
        "drive_hrs": 0.7,
        "flights": {"SEA": 310, "ORD": 520, "COU": 670},
        "car_rental_total": 950,
        "in_park_lodge_prob": "Very Low (<15% Lake McDonald Lodge; historic lodges book 1 yr out)",
        "gateway_lodge_prob": "Moderate-High (75% Columbia Falls, Whitefish, or Kalispell)",
        "lodge_cost_night": 480,
        "camp_cost_night": 30,
        "passes_entry": "America the Beautiful ($80/vehicle) or 7-Day Pass ($35).",
        "timed_entry": "3-hr parking limit at Logan Pass; reserved GTSR express shuttle recommended ($1/person).",
        "wildlife_score": 9.8,
        "scenery_score": 9.9,
        "june_viability": 7.0,
        "banner_img": IMG_GLACIER_MAIN,
        "wildlife_risk": {
            "bear_tier": "Very High (Dense Grizzly Country)",
            "bear_attack_prob": "0.075% (Highest density in Lower 48; frequent trail closures)",
            "moose_tier": "Moderate",
            "moose_attack_prob": "0.025% (Concentrated in Many Glacier valley marshlands)",
            "risk_mitigation": "Hike closely in 5-man pack; call out at blind turns; carry 2+ canisters of bear spray."
        },
        "weather_profile": {
            "p_moderate_temp": "60% (Variable; highs 62°F–72°F; passes drop to mid-30s)",
            "p_clear_skies": "52% (Frequent Pacific fronts crossing Continental Divide)",
            "peril_thunderstorms": "30% (Severe mountain lightning over high crests)",
            "peril_hypothermia": "35% (June wet sleet/snow common at Logan Pass/Highline)",
            "peril_excessive_heat": "<2% (Minimal risk)"
        },
        "hikes": [
            {
                "day": "Monday",
                "name": "Avalanche Lake via Trail of the Cedars",
                "miles": 5.9,
                "gain": 760,
                "vistas": "Old-growth cedars opening to cirque wall with 4 cascading waterfalls.",
                "can_overnight": False,
                "backcountry_permit": "Day hike only. Frontcountry trail.",
                "img": IMG_TRAIL_4
            },
            {
                "day": "Wednesday",
                "name": "Highline Trail to Haystack Butte",
                "miles": 7.2,
                "gain": 850,
                "vistas": "Cliff-shelf ridge above Going-to-the-Sun Road. Subject to snow clearance.",
                "can_overnight": True,
                "backcountry_permit": "Overnight option to Granite Park Chalet/Campground ($10 fee + $7/person/night).",
                "img": IMG_TRAIL_5
            },
            {
                "day": "Friday",
                "name": "Grinnell Glacier Viewpoint (Many Glacier)",
                "miles": 10.6,
                "gain": 1600,
                "vistas": "Turquoise chain of lakes ending with ice floes below glacier.",
                "can_overnight": False,
                "backcountry_permit": "Day hike. Valley backcountry quotas booked in March.",
                "img": IMG_TRAIL_5
            }
        ]
    },
    "Zion": {
        "state": "Utah",
        "airport": "LAS (Las Vegas)",
        "drive_hrs": 2.8,
        "flights": {"SEA": 190, "ORD": 240, "COU": 440},
        "car_rental_total": 600,
        "in_park_lodge_prob": "Very Low (<15% Zion Lodge inside the canyon)",
        "gateway_lodge_prob": "Very High (90% abundant hotels/condos in Springdale, Rockville, and Virgin)",
        "lodge_cost_night": 360,
        "camp_cost_night": 35,
        "passes_entry": "America the Beautiful ($80/vehicle) or 7-Day Pass ($35).",
        "timed_entry": "Angels Landing day lottery ($6 entry + $3/person) needed only past Scout Lookout.",
        "wildlife_score": 6.5,
        "scenery_score": 9.4,
        "june_viability": 9.5,
        "banner_img": IMG_ZION_MAIN,
        "wildlife_risk": {
            "bear_tier": "Negligible",
            "bear_attack_prob": "<0.001% (Black bears rare and restricted to high Kolob plateau)",
            "moose_tier": "None",
            "moose_attack_prob": "0.0% (Zero moose habitat in canyon country)",
            "risk_mitigation": "Rattlesnake vigilance on warm canyon rock; hang packs to avoid ringtail cats."
        },
        "weather_profile": {
            "p_moderate_temp": "40% (Only early mornings; afternoons hot)",
            "p_clear_skies": "88% (Arid desert high pressure dome; scarce cloud cover)",
            "peril_thunderstorms": "15% (Flash flood peril in Narrows slot canyons; check hydro gauges)",
            "peril_hypothermia": "<5% (Narrows river water is 58°F; dry clothing needed)",
            "peril_excessive_heat": "70% (Canyon floor routinely hits 95°F–102°F; carry 4L water/guy)"
        },
        "hikes": [
            {
                "day": "Sunday",
                "name": "The Narrows (Bottom-Up to Big Spring)",
                "miles": 8.9,
                "gain": 350,
                "vistas": "Wading inside 1,000-ft sheer sandstone gorge along Virgin River.",
                "can_overnight": False,
                "backcountry_permit": "Bottom-up day hike requires no permit.",
                "img": IMG_TRAIL_6
            },
            {
                "day": "Tuesday",
                "name": "Scout Lookout via West Rim Trail",
                "miles": 3.6,
                "gain": 1115,
                "vistas": "Walter's Wiggles paved switchbacks looking down into Zion Canyon.",
                "can_overnight": True,
                "backcountry_permit": "Scout Lookout is free; summiting spine requires Angels Landing Lottery.",
                "img": IMG_TRAIL_7
            },
            {
                "day": "Thursday",
                "name": "Observation Point (via East Mesa)",
                "miles": 7.0,
                "gain": 700,
                "vistas": "Ponderosa plateau walk ending at panoramic cliff overlooking Angels Landing.",
                "can_overnight": False,
                "backcountry_permit": "Day hike from East Mesa trailhead.",
                "img": IMG_TRAIL_2
            }
        ]
    },
    "Denali": {
        "state": "Alaska",
        "airport": "ANC (Anchorage)",
        "drive_hrs": 4.5,
        "flights": {"SEA": 460, "ORD": 680, "COU": 860},
        "car_rental_total": 1100,
        "in_park_lodge_prob": "Moderate (50% Riley Creek Cabins / Park entrance lodging)",
        "gateway_lodge_prob": "High (85% Healy, Cantwell, or McKinley Park)",
        "lodge_cost_night": 380,
        "camp_cost_night": 30,
        "passes_entry": "America the Beautiful ($80) or $15/person individual entrance fee.",
        "timed_entry": "Transit bus ticket required past Mile 15.",
        "wildlife_score": 9.9,
        "scenery_score": 9.6,
        "june_viability": 8.8,
        "banner_img": IMG_DENALI_MAIN,
        "wildlife_risk": {
            "bear_tier": "High (Interior Grizzly / Toklat Tundra)",
            "bear_attack_prob": "0.040% (Wide open visibility; sightlines long on open tundra)",
            "moose_tier": "High",
            "moose_attack_prob": "0.050% (Dense willow corridors along Savage/Nenana rivers; cows with calves)",
            "risk_mitigation": "BRFC bear canisters mandatory; stay 300 yds from bears; give moose wide berths in dense brush."
        },
        "weather_profile": {
            "p_moderate_temp": "65% (Highs 60°F–68°F; 24-hr daylight keeps nights around 45°F)",
            "p_clear_skies": "40% (Denali mountain creates its own cloud cover; peak visible ~33% of days)",
            "peril_thunderstorms": "10% (Infrequent interior thunder)",
            "peril_hypothermia": "25% (Cold soaking rainstorms on tundra can last 36 hours)",
            "peril_excessive_heat": "0% (Zero extreme heat hazard)"
        },
        "hikes": [
            {
                "day": "Monday",
                "name": "Mount Healy Overlook",
                "miles": 5.4,
                "gain": 1700,
                "vistas": "Sub-arctic tundra ridge overlooking Nenana River Canyon.",
                "can_overnight": False,
                "backcountry_permit": "Day hike near visitor center.",
                "img": IMG_TRAIL_8
            },
            {
                "day": "Wednesday",
                "name": "Savage Alpine Trail",
                "miles": 4.1,
                "gain": 1414,
                "vistas": "Rugged alpine tundra route crossing between Savage River and Mountain Creek.",
                "can_overnight": True,
                "backcountry_permit": "Backcountry unit permit required if camping (free in-person safety briefing).",
                "img": IMG_TRAIL_9
            },
            {
                "day": "Friday",
                "name": "Horseshoe Lake Loop",
                "miles": 3.2,
                "gain": 390,
                "vistas": "Quiet oxbow lake, active beaver lodges, and prime moose feeding wetlands.",
                "can_overnight": False,
                "backcountry_permit": "Low-impact day trail.",
                "img": IMG_TRAIL_10
            }
        ]
    },
    "Kenai Fjords": {
        "state": "Alaska",
        "airport": "ANC (Anchorage)",
        "drive_hrs": 2.5,
        "flights": {"SEA": 460, "ORD": 680, "COU": 860},
        "car_rental_total": 1050,
        "in_park_lodge_prob": "Low (<20% Glacier Lodge / Wilderness Lodges)",
        "gateway_lodge_prob": "High (85% strong hotel, B&B, and cabin capacity in Seward)",
        "lodge_cost_night": 410,
        "camp_cost_night": 25,
        "passes_entry": "No entrance fee for Kenai Fjords National Park.",
        "timed_entry": "None. Marine boat tours require commercial booking.",
        "wildlife_score": 9.7,
        "scenery_score": 9.5,
        "june_viability": 8.5,
        "banner_img": IMG_KENAI_MAIN,
        "wildlife_risk": {
            "bear_tier": "Moderate-High (Coastal Black & Brown Bears)",
            "bear_attack_prob": "0.030% (High bear concentration feeding on coastal salmon/berries)",
            "moose_tier": "Moderate",
            "moose_attack_prob": "0.020% (Common around Exit Glacier road corridor)",
            "risk_mitigation": "Make noise in coastal alder thickets; store food in locked vehicles or bear boxes."
        },
        "weather_profile": {
            "p_moderate_temp": "55% (Maritime cool; highs 55°F–64°F)",
            "p_clear_skies": "38% (Gulf of Alaska coastal marine layer, maritime fog and drizzle)",
            "peril_thunderstorms": "<5% (Rare coastal thunderstorms)",
            "peril_hypothermia": "30% (Ocean spray combined with 50°F drizzle and wind)",
            "peril_excessive_heat": "0% (Non-existent)"
        },
        "hikes": [
            {
                "day": "Monday",
                "name": "Harding Icefield Trail",
                "miles": 8.2,
                "gain": 3200,
                "vistas": "Birch forest transition into subalpine ridge peering over a 700-sq-mile ice sheet.",
                "can_overnight": False,
                "backcountry_permit": "Steep day hike. Alpine camping allowed on bare rock/snow off-trail.",
                "img": IMG_TRAIL_5
            },
            {
                "day": "Wednesday",
                "name": "Exit Glacier Overlook & Spillway",
                "miles": 2.2,
                "gain": 300,
                "vistas": "Short path straight to the snout and gravel riverbeds of the receding glacier.",
                "can_overnight": False,
                "backcountry_permit": "Day interpretive loop.",
                "img": IMG_TRAIL_11
            },
            {
                "day": "Friday",
                "name": "Tonsina Point via Caines Head Trail",
                "miles": 4.5,
                "gain": 650,
                "vistas": "Coastal rainforest path along Resurrection Bay to cobblestone beach flats.",
                "can_overnight": True,
                "backcountry_permit": "Overnight beach camping available at Tonsina ($15/night state park fee).",
                "img": IMG_TRAIL_12
            }
        ]
    },
    "Olympic": {
        "state": "Washington",
        "airport": "SEA (Seattle)",
        "drive_hrs": 2.5,
        "flights": {"SEA": 0, "ORD": 290, "COU": 480},
        "car_rental_total": 700,
        "in_park_lodge_prob": "Low (25% Lake Crescent Lodge or Kalaloch Lodge)",
        "gateway_lodge_prob": "High (85% ample motel, VRBO, and cabin supply in Port Angeles and Forks)",
        "lodge_cost_night": 320,
        "camp_cost_night": 25,
        "passes_entry": "America the Beautiful ($80/vehicle) or 7-Day Pass ($35).",
        "timed_entry": "None. Arrive at Hoh Rain Forest before 8:30 AM to beat long vehicle gate lines.",
        "wildlife_score": 8.2,
        "scenery_score": 9.1,
        "june_viability": 9.2,
        "banner_img": IMG_OLYMPIC_MAIN,
        "wildlife_risk": {
            "bear_tier": "Moderate (Black Bears Only)",
            "bear_attack_prob": "0.010% (Docile, well-fed black bears; no grizzly population)",
            "moose_tier": "None",
            "moose_attack_prob": "0.0% (Zero moose; Roosevelt elk present but rarely aggressive)",
            "risk_mitigation": "Mandatory bear canisters for beach/rainforest camping; keep distance from bull elk."
        },
        "weather_profile": {
            "p_moderate_temp": "70% (Mild maritime temperatures; highs 64°F–72°F)",
            "p_clear_skies": "58% (June gloom morning fog burns off by midday on Pacific coast)",
            "peril_thunderstorms": "<5% (Very rare convective lightning)",
            "peril_hypothermia": "18% (Pacific drizzle combined with breezy ocean fronts)",
            "peril_excessive_heat": "<2% (Temperate and ocean-cooled)"
        },
        "hikes": [
            {
                "day": "Monday",
                "name": "Hoh River Trail to 5-Mile Island",
                "miles": 10.2,
                "gain": 300,
                "vistas": "Old-growth moss canopies, Roosevelt elk habitat, flat trail beside the glacial river.",
                "can_overnight": True,
                "backcountry_permit": "Wilderness Camping Permit ($8/person/night + $6 reservation fee).",
                "img": IMG_TRAIL_13
            },
            {
                "day": "Wednesday",
                "name": "Rialto Beach to Hole-in-the-Wall",
                "miles": 3.4,
                "gain": 50,
                "vistas": "Pacific coastal beach hike, tide pool colonies, dramatic offshore sea stacks.",
                "can_overnight": True,
                "backcountry_permit": "Coastal beach camping allowed with wilderness permit.",
                "img": IMG_GLACIER_MAIN
            },
            {
                "day": "Friday",
                "name": "Mount Storm King",
                "miles": 4.1,
                "gain": 2100,
                "vistas": "Rope-assisted rock spine perched directly above turquoise Lake Crescent.",
                "can_overnight": False,
                "backcountry_permit": "Day hike only.",
                "img": IMG_TRAIL_2
            }
        ]
    },
    "Mount Rainier": {
        "state": "Washington",
        "airport": "SEA (Seattle)",
        "drive_hrs": 2.0,
        "flights": {"SEA": 0, "ORD": 290, "COU": 480},
        "car_rental_total": 700,
        "in_park_lodge_prob": "Very Low (<15% Paradise Inn / National Park Inn)",
        "gateway_lodge_prob": "Moderate (65% mountain cabins in Ashford, Packwood, and Crystal Mountain)",
        "lodge_cost_night": 340,
        "camp_cost_night": 25,
        "passes_entry": "America the Beautiful ($80/vehicle) or 7-Day Pass ($35).",
        "timed_entry": "Timed entry corridor reservations ($2) enforced for Paradise/Sunrise 7 AM - 3 PM.",
        "wildlife_score": 8.4,
        "scenery_score": 9.5,
        "june_viability": 7.5,
        "banner_img": IMG_RAINIER_MAIN,
        "wildlife_risk": {
            "bear_tier": "Low-Moderate (Black Bears)",
            "bear_attack_prob": "0.008% (Black bears frequent lower berry meadows; no grizzlies)",
            "moose_tier": "None",
            "moose_attack_prob": "0.0% (No moose population)",
            "risk_mitigation": "Hang food at backcountry camps; yield to mountain goats on narrow rocky ledges."
        },
        "weather_profile": {
            "p_moderate_temp": "60% (Highs 58°F–68°F at Longmire; Paradise snowline remains around 48°F)",
            "p_clear_skies": "55% (Cascade cloud cap often forms midday on summit flanks)",
            "peril_thunderstorms": "10% (Occasional summer storm buildup)",
            "peril_hypothermia": "30% (High snowpack reflection + sudden rain/fog at Paradise)",
            "peril_excessive_heat": "<1% (Cool mountain air)"
        },
        "hikes": [
            {
                "day": "Monday",
                "name": "Skyline Trail Loop (Paradise)",
                "miles": 5.5,
                "gain": 1700,
                "vistas": "Subalpine snowfield traverse with close views of Nisqually Glacier and volcano crater.",
                "can_overnight": False,
                "backcountry_permit": "Day loop. Microspikes recommended for June snowfields.",
                "img": IMG_TRAIL_5
            },
            {
                "day": "Wednesday",
                "name": "Comet & Christine Falls",
                "miles": 3.8,
                "gain": 1250,
                "vistas": "Fast-flowing ravine trail culminating in a 320-foot thundering waterfall amphitheater.",
                "can_overnight": False,
                "backcountry_permit": "Day trek.",
                "img": IMG_TRAIL_14
            },
            {
                "day": "Friday",
                "name": "Rampart Ridge Loop",
                "miles": 4.6,
                "gain": 1340,
                "vistas": "Dense old-growth ridge path offering views of Longmire and Mount Rainier.",
                "can_overnight": False,
                "backcountry_permit": "Day loop.",
                "img": IMG_TRAIL_1
            }
        ]
    },
    "North Cascades": {
        "state": "Washington",
        "airport": "SEA (Seattle)",
        "drive_hrs": 2.5,
        "flights": {"SEA": 0, "ORD": 290, "COU": 480},
        "car_rental_total": 700,
        "in_park_lodge_prob": "Low (<20% Ross Lake Resort floating cabins book 12 months out)",
        "gateway_lodge_prob": "Moderate-High (70% in Marblemount, Rockport, or Winthrop on the east side)",
        "lodge_cost_night": 300,
        "camp_cost_night": 20,
        "passes_entry": "No entrance fee for North Cascades National Park.",
        "timed_entry": "None required.",
        "wildlife_score": 7.8,
        "scenery_score": 9.4,
        "june_viability": 7.3,
        "banner_img": IMG_CASCADES_MAIN,
        "wildlife_risk": {
            "bear_tier": "Low-Moderate (Black Bear; Grizzly functionally absent)",
            "bear_attack_prob": "0.009% (Black bears active in valleys; grizzlies extraordinarily rare)",
            "moose_tier": "Negligible",
            "moose_attack_prob": "0.002% (Occasional transient moose in eastern river valleys)",
            "risk_mitigation": "Store food in bear lockers; watch for steep loose scree on alpine passes."
        },
        "weather_profile": {
            "p_moderate_temp": "68% (Highs 65°F–74°F in low valleys like Diablo; passes colder)",
            "p_clear_skies": "50% (High Cascade peaks trap Pacific clouds)",
            "peril_thunderstorms": "15% (Afternoon high ridge lightning)",
            "peril_hypothermia": "28% (Snow travel on high passes combined with rain)",
            "peril_excessive_heat": "<5% (Comfortable alpine climate)"
        },
        "hikes": [
            {
                "day": "Monday",
                "name": "Diablo Lake Trail",
                "miles": 7.6,
                "gain": 1400,
                "vistas": "High bluffs above glacial jade waters, suspension bridges, and forested slopes.",
                "can_overnight": True,
                "backcountry_permit": "Overnight camping at Buster Brown boat/walk camp with free backcountry permit.",
                "img": IMG_TRAIL_10
            },
            {
                "day": "Wednesday",
                "name": "Maple Pass Loop",
                "miles": 7.4,
                "gain": 2020,
                "vistas": "High ridgeline circle around Lake Ann (check snow conditions at pass in early June).",
                "can_overnight": False,
                "backcountry_permit": "Day loop. Camping prohibited directly inside Lake Ann cirque.",
                "img": IMG_TRAIL_2
            },
            {
                "day": "Friday",
                "name": "Thunder Knob Trail",
                "miles": 3.6,
                "gain": 635,
                "vistas": "Accessible climb over Colonial Creek to a panoramic overlook of Diablo Lake.",
                "can_overnight": False,
                "backcountry_permit": "Day hike from Colonial Creek Campground.",
                "img": IMG_TRAIL_3
            }
        ]
    },
    "Yosemite": {
        "state": "California",
        "airport": "FAT (Fresno) / SFO",
        "drive_hrs": 2.5,
        "flights": {"SEA": 240, "ORD": 340, "COU": 580},
        "car_rental_total": 850,
        "in_park_lodge_prob": "Near Zero (<5% Ahwahnee, Yosemite Valley Lodge, or Curry Village)",
        "gateway_lodge_prob": "Moderate (60% hotels/Airbnbs in El Portal, Mariposa, Groveland, or Oakhurst)",
        "lodge_cost_night": 480,
        "camp_cost_night": 36,
        "passes_entry": "America the Beautiful ($80/vehicle) or 7-Day Pass ($35).",
        "timed_entry": "Peak-hours vehicle reservation ($2) required on June weekends and holidays.",
        "wildlife_score": 8.0,
        "scenery_score": 9.8,
        "june_viability": 9.1,
        "banner_img": IMG_YOSEMITE_MAIN,
        "wildlife_risk": {
            "bear_tier": "Moderate (Habituated Black Bears Only)",
            "bear_attack_prob": "0.012% (Aggressive food-raiding history; physical attacks very rare)",
            "moose_tier": "None",
            "moose_attack_prob": "0.0% (Zero moose in Sierra Nevada)",
            "risk_mitigation": "Zero food left in vehicles at trailheads; bear canisters strictly enforced in backcountry."
        },
        "weather_profile": {
            "p_moderate_temp": "80% (Highs 75°F–84°F in Yosemite Valley; alpine rims 65°F)",
            "p_clear_skies": "82% (Dominant California summer sun; infrequent storms)",
            "peril_thunderstorms": "20% (High Sierra granite peaks see brief afternoon thundershowers)",
            "peril_hypothermia": "10% (Low risk unless drenched on Mist Trail in chilly wind)",
            "peril_excessive_heat": "25% (Valley floor can touch 90°F in late June)"
        },
        "hikes": [
            {
                "day": "Sunday",
                "name": "Mist Trail to Nevada Fall",
                "miles": 5.4,
                "gain": 2000,
                "vistas": "Peak snowmelt spray pounding granite stairways past Vernal and Nevada Falls.",
                "can_overnight": True,
                "backcountry_permit": "Wilderness permit required to continue past Nevada Fall into Little Yosemite Valley.",
                "img": IMG_TRAIL_14
            },
            {
                "day": "Tuesday",
                "name": "Upper Yosemite Falls to Columbia Rock",
                "miles": 7.2,
                "gain": 2700,
                "vistas": "Switchbacks ascending valley wall with front-row views of the 2,425-ft cataract.",
                "can_overnight": False,
                "backcountry_permit": "Day trek.",
                "img": IMG_TRAIL_5
            },
            {
                "day": "Thursday",
                "name": "Sentinel Dome & Taft Point Loop",
                "miles": 5.1,
                "gain": 1120,
                "vistas": "Granite dome crest and vertiginous looks over the 3,000-ft abyss and El Capitan.",
                "can_overnight": False,
                "backcountry_permit": "Day loop along Glacier Point Road corridor.",
                "img": IMG_TRAIL_7
            }
        ]
    },
    "Rocky Mountain": {
        "state": "Colorado",
        "airport": "DEN (Denver)",
        "drive_hrs": 1.5,
        "flights": {"SEA": 210, "ORD": 170, "COU": 380},
        "car_rental_total": 750,
        "in_park_lodge_prob": "N/A (No NPS lodges inside park)",
        "gateway_lodge_prob": "Very High (90% deep vacation rental inventory in Estes Park and Grand Lake)",
        "lodge_cost_night": 400,
        "camp_cost_night": 35,
        "passes_entry": "America the Beautiful ($80/vehicle) or 7-Day Pass ($35).",
        "timed_entry": "Timed Entry+ Bear Lake Road ($2 via Recreation.gov) required 5 AM - 6 PM.",
        "wildlife_score": 8.7,
        "scenery_score": 9.2,
        "june_viability": 8.4,
        "banner_img": IMG_ROCKY_MAIN,
        "wildlife_risk": {
            "bear_tier": "Low-Moderate (Black Bears Only)",
            "bear_attack_prob": "0.008% (Black bears shy; no grizzly population)",
            "moose_tier": "High",
            "moose_attack_prob": "0.045% (Large moose concentration on west side / Kawuneeche Valley)",
            "risk_mitigation": "Keep 25+ yards from aggressive bull and cow moose; carry bear canister in backcountry."
        },
        "weather_profile": {
            "p_moderate_temp": "72% (Highs 68°F–75°F in Estes Park; alpine tundra 50°F–58°F)",
            "p_clear_skies": "68% (Clear bluebird mornings almost daily)",
            "peril_thunderstorms": "50% (High lightning hazard; off summits by noon strictly advised)",
            "peril_hypothermia": "22% (Hail/sleet on Trail Ridge Road and high passes)",
            "peril_excessive_heat": "<2% (High altitude prevents high heat)"
        },
        "hikes": [
            {
                "day": "Sunday",
                "name": "Emerald Lake via Dream & Nymph Lakes",
                "miles": 3.6,
                "gain": 605,
                "vistas": "Trio of alpine cirque lakes nestled directly beneath the sheer face of Hallett Peak.",
                "can_overnight": False,
                "backcountry_permit": "Day hike along Bear Lake corridor.",
                "img": IMG_TRAIL_1
            },
            {
                "day": "Tuesday",
                "name": "Sky Pond via Glacier Gorge Trail",
                "miles": 9.0,
                "gain": 1780,
                "vistas": "Timberline waterfall headwall scramble up to soaring granite spires (Sharkstooth).",
                "can_overnight": True,
                "backcountry_permit": "RMNP Wilderness Permit ($36 flat fee via Recreation.gov). Bear canister mandatory.",
                "img": IMG_TRAIL_3
            },
            {
                "day": "Thursday",
                "name": "Deer Mountain",
                "miles": 6.2,
                "gain": 1210,
                "vistas": "Dry south-facing switchbacks framing the Continental Divide and Longs Peak.",
                "can_overnight": False,
                "backcountry_permit": "Day hike.",
                "img": IMG_TRAIL_4
            }
        ]
    }
}

# --- STATISTICAL ENGINE ---
def compute_complete_costs(park_dict, split_mode):
    if "All Lodge" in split_mode:
        lodging_total = park_dict["lodge_cost_night"] * 7
    elif "All Tent" in split_mode:
        lodging_total = park_dict["camp_cost_night"] * 7
    else:  # 50/50 Split
        lodging_total = (park_dict["camp_cost_night"] * 3) + (park_dict["lodge_cost_night"] * 4)

    shared_ground = park_dict["car_rental_total"] + lodging_total
    shared_per_guy = shared_ground / 5.0

    traveler_totals = [
        park_dict["flights"]["SEA"] + shared_per_guy,
        park_dict["flights"]["SEA"] + shared_per_guy,
        park_dict["flights"]["ORD"] + shared_per_guy,
        park_dict["flights"]["ORD"] + shared_per_guy,
        park_dict["flights"]["COU"] + shared_per_guy
    ]

    tot = sum(traveler_totals)
    mn = float(np.mean(traveler_totals))
    fl_skew = float(skew([
        park_dict["flights"]["SEA"],
        park_dict["flights"]["SEA"],
        park_dict["flights"]["ORD"],
        park_dict["flights"]["ORD"],
        park_dict["flights"]["COU"]
    ]))

    return traveler_totals, tot, mn, fl_skew, shared_per_guy, lodging_total

# --- SIDEBAR: CREW IDENTITY & SESSION ---
with st.sidebar:
    st.image(IMG_SIDEBAR, use_container_width=True)
    st.markdown("### The Crew Roster")
    st.markdown("""
    **Five just regular 39-year-old guys** on an annual weeklong June expedition.
    * **Seattle, WA (SEA):** 2 Guys
    * **Chicago, IL (ORD):** 2 Guys
    * **Columbia, MO (COU):** 1 Guy
    """)
    st.markdown("---")
    
    # Voter Identity Selector
    user_roster = [
        "Seattle Guy #1",
        "Seattle Guy #2",
        "Chicago Guy #1",
        "Chicago Guy #2",
        "Columbia Guy",
        "Guest / Other"
    ]
    current_user = st.selectbox("Identify Yourself to Vote / Comment:", user_roster)
    if current_user == "Guest / Other":
        current_user = st.text_input("Enter your name:", value="Guest")

# --- APP HEADER & DESCRIPTION ---
st.title("🌲 National Park Expedition & Secret Birthday Trip")
st.markdown("""
### Decision Engine for Just Regular 39-Year-Old Guys
Planning an annual weeklong expedition for **five just regular 39-year-old guys** requires balancing ambitious alpine ambitions against cold logistical realities. The month of **June** is a dramatic transitional season across North America's premier wilderness corridors. At high elevations in the Rockies, North Cascades, and Pacific Northwest, winter snowpack is actively thawing, waterfalls are discharging at historic peak volumes, and alpine passes above 8,000–9,000 feet often demand microspikes or route pivots. Concurrently, wildlife emerges into lower river meadows: **grizzly sows forage with newborn cubs** and **cow moose fiercely defend newborn calves in willow thickets**.

This application acts as a comprehensive decision matrix. It models:
1. **Financial Equity & Hub Skewness:** Round-trip flight economics across three disparate home airports (**2 travelers from Seattle, WA; 2 from Chicago, IL; and 1 from Columbia, MO**) are combined with rental SUV costs and accommodations. Pearson’s skewness metric quantifies whether the guy flying out of Columbia carries a disproportionate financial burden.
2. **Lodging Feasibility & The 50/50 Strategy:** National park lodges often sell out 6 to 12 months in advance. We calculate realistic booking probabilities in both in-park lodges and nearby gateway communities, alongside frontcountry drive-in tent sites.
3. **Wildlife Risk vs. Weather Perils:** Quantified odds for bear and moose encounters, thunderstorm flash flooding, and hypothermia vs. extreme heat.
4. **Curated 3-Hike Packages:** Paced across the week to ensure adequate acclimation, manageable car travel times, and flexible day vs. backcountry overnight potential.
5. **Ranked-Choice Voting & Discussion Feed:** Submit your personal 1st, 2nd, and 3rd choices to see the live crew standings, and log discussion notes about accommodations or gear.
""")

st.markdown("---")

# --- SECTION 1: TRIP STRATEGY & OPTIMIZATION CONTROLS ---
st.subheader("⚙️ 1. Trip Strategy & Optimization Controls")
st.markdown("Adjust the crew's accommodation model and scoring priorities below. Everything recalculates instantly.")

# Accommodations Model
st.markdown("#### Accommodations Model")
split_strategy = st.radio(
    "Select Lodging Allocation:",
    [
        "50/50 Split (3 Nights Tent / 4 Nights Lodge)",
        "All Lodge (7 Nights in Cabin / Lodge)",
        "All Tent Camping (7 Nights in Tent Campsite)"
    ],
    index=0,
    horizontal=False
)

st.caption("""
* **50/50 Split:** Frontcountry/trail camping early when energy is high; comfortable beds & hot showers for recovery later in the week.
* **All Lodge:** Maximum group recovery and amenities every night (highest total cost).
* **All Tent:** Maximum immersion and budget efficiency (requires hauling or renting camping equipment).
""")

st.markdown("---")

# Multi-Criteria Sliders
st.markdown("#### Multi-Criteria Scoring Weights")
st.caption("Adjust sliders (0.0 = Ignore, 1.0 = Maximum Priority):")

w_cost = st.slider("Cost Efficiency / Low Budget", 0.0, 1.0, 0.25, 0.05, key="w_cost")
w_drive = st.slider("Airport Proximity (Low Drive Time)", 0.0, 1.0, 0.15, 0.05, key="w_drive")
w_scenery = st.slider("Scenery & Alpine Grandeur", 0.0, 1.0, 0.25, 0.05, key="w_scenery")
w_june = st.slider("June Trail Viability (Snow-Free)", 0.0, 1.0, 0.15, 0.05, key="w_june")
w_weather = st.slider("Mild Temps & Clear Skies (Fewer Clouds)", 0.0, 1.0, 0.10, 0.05, key="w_weather")
w_safety = st.slider("Wildlife Safety (Low Bear/Moose Peril)", 0.0, 1.0, 0.10, 0.05, key="w_safety")

st.markdown("---")

# --- RANKING CALCULATIONS ---
records = []
for name, data in PARK_DATA.items():
    _, tot, mn, fl_skew, shared_per_guy, lodging_tot = compute_complete_costs(data, split_strategy)

    cost_score = max(0.0, 10.0 - ((mn - 600.0) / 120.0))
    drive_score = max(0.0, 10.0 - (data["drive_hrs"] * 2.0))
    
    p_mod_val = float(data["weather_profile"]["p_moderate_temp"].split("%")[0]) / 10.0
    p_clr_val = float(data["weather_profile"]["p_clear_skies"].split("%")[0]) / 10.0
    weather_score = (p_mod_val * 0.5) + (p_clr_val * 0.5)

    bear_tier = data["wildlife_risk"]["bear_tier"]
    if "Very High" in bear_tier:
        safety_score = 3.5
    elif "High" in bear_tier:
        safety_score = 5.0
    elif "Moderate" in bear_tier:
        safety_score = 7.5
    else:
        safety_score = 9.5

    tot_weight = w_cost + w_drive + w_scenery + w_june + w_weather + w_safety
    if tot_weight == 0:
        tot_weight = 1.0

    final_score = (
        (cost_score * w_cost) +
        (drive_score * w_drive) +
        (data["scenery_score"] * w_scenery) +
        (data["june_viability"] * w_june) +
        (weather_score * w_weather) +
        (safety_score * w_safety)
    ) / tot_weight

    records.append({
        "Park": name,
        "State": data["state"],
        "Overall Score": round(final_score, 2),
        "Mean Total / Guy": f"${round(mn, 0):,.0f}",
        "Group Spend": f"${round(tot, 0):,.0f}",
        "Bear Risk Tier": data["wildlife_risk"]["bear_tier"].split(" ")[0],
        "Moose Risk Tier": data["wildlife_risk"]["moose_tier"],
        "Moderate Temp %": data["weather_profile"]["p_moderate_temp"].split(" ")[0],
        "Clear Skies %": data["weather_profile"]["p_clear_skies"].split(" ")[0],
        "Drive (hrs)": data["drive_hrs"],
        "Nearest Airport": data["airport"]
    })

df_rankings = pd.DataFrame(records).sort_values(by="Overall Score", ascending=False).reset_index(drop=True)

# --- SECTION 2: MASTER RANKING LEADERBOARD ---
st.subheader(f"📊 2. Master Ranking Leaderboard — Model: {split_strategy}")
st.markdown("Sorted in real time by your custom weighted criteria. Inspect how each park balances financial fairness, road transit, and terrain quality.")
st.dataframe(
    df_rankings[[
        "Park", "State", "Overall Score", "Mean Total / Guy", "Group Spend",
        "Bear Risk Tier", "Moose Risk Tier", "Moderate Temp %", "Clear Skies %", "Drive (hrs)", "Nearest Airport"
    ]],
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# --- SECTION 3: DESTINATION DEEP DIVE & CREW COLLABORATION ---
st.subheader("🔍 3. Destination Deep Dive & Crew Collaboration")
selected_park = st.selectbox("Select a National Park to examine its full operational package:", df_rankings["Park"])

park = PARK_DATA[selected_park]
costs, tot_cost, mean_cost, fl_skew, shared_guy, lodging_tot = compute_complete_costs(park, split_strategy)
cur_score = df_rankings.loc[df_rankings["Park"] == selected_park, "Overall Score"].values[0]

# Banner Image
st.image(park["banner_img"], caption=f"{selected_park} National Park — {park['state']}", use_container_width=True)

# Navigation Selector
st.markdown("#### Choose Inspection Category:")
view_choice = st.radio(
    "Select Topic to View:",
    [
        "📋 Overview & Logistics",
        "🐻 Wildlife Risk (Bear & Moose)",
        "⛅ Weather Perils & Climate",
        "🏕️ Lodging Strategy & Passes",
        "✈️ Cost Distribution & Skewness",
        "🥾 Curated 3-Hike Package",
        "🗳️ Crew Vote & Comments",
        "⚔️ Spanish Inquisition"
    ],
    index=0
)

st.markdown("---")

# 1. OVERVIEW & LOGISTICS
if view_choice == "📋 Overview & Logistics":
    st.markdown(f"### Overview & Logistics: {selected_park}")
    st.write(f"**Overall Weighted Score:** `{cur_score} / 10`")
    st.write(f"**Airport Drive Time:** `{park['drive_hrs']} hours`")
    st.write(f"**Scenery / Hike Grandeur:** `{park['scenery_score']} / 10`")
    st.write(f"**June Trail Viability:** `{park['june_viability']} / 10`")

    st.markdown(f"""
    **Operational Synopsis: {selected_park}**
    * **Gateway Hub:** {park['airport']} — Approximately **{park['drive_hrs']} hours** of highway and mountain driving to reach base camp. For five regular 39-year-old guys landing Saturday afternoon, this drive time is crucial for grocery restocking, renting bear spray canisters, and reaching camp before dusk.
    * **Wildlife Viewing Potential:** Rated **{park['wildlife_score']} / 10**. June offers exceptional viewing as animals descend to low-elevation valley bottoms where lush forage is concentrated.
    * **June Ground Conditions Reality:** {'High-alpine snowpack remains persistent along passes above 8,000–9,000 feet. You can anticipate thunderous waterfall runoff, snow bridges over glacial streams, and spectacular wildflower emergence along lower cirques. Higher routes may require microspikes and hiking poles.' if park['june_viability'] < 8.5 else 'Favorable, early summer conditions predominate. Snowmelt is substantially complete along primary trails, slot canyon water levels are stabilizing, and passes are widely accessible without technical mountaineering equipment.'}
    """)

# 2. WILDLIFE RISK
elif view_choice == "🐻 Wildlife Risk (Bear & Moose)":
    st.markdown(f"### Wildlife Risk: {selected_park}")
    st.markdown("""
    When five regular 39-year-old guys head into the wilderness, wildlife encounters are both a premier attraction and an objective safety hazard.
    In **June**, two biological phenomena peak simultaneously:
    1. **Grizzly and black bear sows** are intensely protective of newborn cubs while foraging heavily in low-elevation valley floors and avalanche chutes.
    2. **Cow moose** give birth in dense riverbank willow thickets and will aggressively charge intruders who stumble into their nursery corridors.
    """)

    st.markdown(f"""
    * **🐻 Bear Conflict Assessment:**
      * Risk Classification: `{park['wildlife_risk']['bear_tier']}`
      * Estimated Attack / Charge Probability: `{park['wildlife_risk']['bear_attack_prob']}`
    * **🫎 Moose Conflict Assessment:**
      * Risk Classification: `{park['wildlife_risk']['moose_tier']}`
      * Estimated Confrontation / Charge Probability: `{park['wildlife_risk']['moose_attack_prob']}`
    """)

    st.info(f"""
    **Mandatory Group Safety Protocols:** {park['wildlife_risk']['risk_mitigation']}
    
    *Crew Rule of Thumb:* Hike in a tight group of five. The presence of five adult men talking and making noise is one of the most effective natural deterrents against surprise wildlife encounters.
    """)

# 3. WEATHER PERILS & CLIMATE
elif view_choice == "⛅ Weather Perils & Climate":
    st.markdown(f"### Weather Perils & Climate: {selected_park}")
    st.markdown("June mountain weather can shift rapidly. Review temperature ranges and convective perils below:")

    st.write(f"**Moderate Temps (60°F–78°F Highs):** `{park['weather_profile']['p_moderate_temp']}`")
    st.write(f"**Clear / Few Clouds (Bluebird Day Odds):** `{park['weather_profile']['p_clear_skies']}`")
    st.write(f"**Convective Thunderstorms & Lightning:** `{park['weather_profile']['peril_thunderstorms']}`")
    st.write(f"**Hypothermia & Sudden Cold Snaps:** `{park['weather_profile']['peril_hypothermia']}`")
    st.write(f"**Excessive Heat Hazard (>95°F):** `{park['weather_profile']['peril_excessive_heat']}`")

# 4. LODGING STRATEGY & PASSES
elif view_choice == "🏕️ Lodging Strategy & Passes":
    st.markdown(f"### Lodging Strategy & Passes: {selected_park}")
    st.write(f"**In-Park Historic Lodge Odds:** `{park['in_park_lodge_prob']}`")
    st.write(f"**Gateway Community Lodges / Condos / Airbnbs:** `{park['gateway_lodge_prob']}`")
    st.write(f"**Est. Nightly Cabin / Lodge (5 Guys):** `${park['lodge_cost_night']} / night`")
    st.write(f"**Est. Nightly Frontcountry Campsite:** `${park['camp_cost_night']} / night`")
    st.write(f"**Park Vehicle Entrance Pass:** {park['passes_entry']}")
    st.write(f"**Timed-Entry / Corridor Mandates:** {park['timed_entry']}")

    st.success(f"""
    **The 50/50 Split Model: Total Spend for 5 Guys = ${lodging_tot:,.0f} (${lodging_tot/5:,.0f}/person)**
    * **Phase 1 (Sat-Tue | 3 Nights Tents):** Frontcountry campground base camp at ${park['camp_cost_night']}/night.
    * **Phase 2 (Wed-Sun | 4 Nights Lodge):** Gateway vacation rental or lodge at ${park['lodge_cost_night']}/night with full beds, hot showers, and laundry.
    """)

# 5. FLIGHTS & SKEWNESS
elif view_choice == "✈️ Cost Distribution & Skewness":
    st.markdown(f"### Flight Costs & Group Equity: {selected_park}")
    st.write(f"**Total Group Spend (All 5 Travelers):** `${tot_cost:,.0f}`")
    st.write(f"**Mean Outlay Per Guy:** `${mean_cost:,.0f}`")
    st.write(f"**Flight Cost Skewness:** `{fl_skew:+.2f}`")

    st.caption("Positive skew (> +0.50) indicates the Columbia, MO traveler carries a higher regional connector airfare burden.")

    fin_table = [
        {"Traveler / Origin": "Seattle, WA #1", "Airfare": f"${park['flights']['SEA']}", "Car + Lodging Share": f"${shared_guy:,.0f}", "Total Net Spend": f"${costs[0]:,.0f}"},
        {"Traveler / Origin": "Seattle, WA #2", "Airfare": f"${park['flights']['SEA']}", "Car + Lodging Share": f"${shared_guy:,.0f}", "Total Net Spend": f"${costs[1]:,.0f}"},
        {"Traveler / Origin": "Chicago, IL #1", "Airfare": f"${park['flights']['ORD']}", "Car + Lodging Share": f"${shared_guy:,.0f}", "Total Net Spend": f"${costs[2]:,.0f}"},
        {"Traveler / Origin": "Chicago, IL #2", "Airfare": f"${park['flights']['ORD']}", "Car + Lodging Share": f"${shared_guy:,.0f}", "Total Net Spend": f"${costs[3]:,.0f}"},
        {"Traveler / Origin": "Columbia, MO #1", "Airfare": f"${park['flights']['COU']}", "Car + Lodging Share": f"${shared_guy:,.0f}", "Total Net Spend": f"${costs[4]:,.0f}"},
    ]
    st.table(pd.DataFrame(fin_table))

# 6. HIKES
elif view_choice == "🥾 Curated 3-Hike Package":
    st.markdown(f"### Curated 3-Hike Package: {selected_park}")
    for i, hike in enumerate(park["hikes"], 1):
        st.markdown(f"#### Hike {i}: {hike['name']}")
        st.image(hike["img"], use_container_width=True)
        st.write(f"**Day:** `{hike['day']}` | **Distance:** `{hike['miles']} miles` | **Gain:** `{hike['gain']} ft`")
        st.write(f"**Vistas & Highlights:** {hike['vistas']}")
        if hike["can_overnight"]:
            st.success(f"⛺ Overnight Available: {hike['backcountry_permit']}")
        else:
            st.info(f"🥾 Format: {hike['backcountry_permit']}")
        st.divider()

# 7. CREW VOTE & COMMENTS (COLLABORATIVE LOGGING & RANKED VOTING)
elif view_choice == "🗳️ Crew Vote & Comments":
    st.markdown("### 🗳️ Group Voting & Discussion Log")
    st.markdown(f"Active User: **{current_user}**")
    
    data_store = load_data()
    all_parks = list(PARK_DATA.keys())

    # SUBSECTION A: SUBMIT A BALLOT
    st.markdown("#### Cast Your Ranked-Choice Ballot")
    st.caption("Points allocated: 1st Place = 3 pts, 2nd Place = 2 pts, 3rd Place = 1 pt.")

    with st.form("voting_form"):
        p1 = st.selectbox("1st Choice (3 Points):", all_parks, index=0)
        p2 = st.selectbox("2nd Choice (2 Points):", all_parks, index=1)
        p3 = st.selectbox("3rd Choice (1 Point):", all_parks, index=2)
        submit_vote = st.form_submit_button("Submit / Update My Ballot")

        if submit_vote:
            if len({p1, p2, p3}) < 3:
                st.error("Please pick 3 distinct parks for your ballot!")
            else:
                data_store["votes"][current_user] = {
                    "first": p1,
                    "second": p2,
                    "third": p3,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                save_data(data_store)
                st.success(f"Ballot recorded for {current_user}!")

    # SUBSECTION B: LIVE STANDINGS
    st.markdown("---")
    st.markdown("#### Live Consensus Standings")
    
    tally = {p: 0 for p in all_parks}
    ballots = data_store.get("votes", {})

    for user, ballot in ballots.items():
        tally[ballot["first"]] += 3
        tally[ballot["second"]] += 2
        tally[ballot["third"]] += 1

    df_tally = pd.DataFrame([
        {"Park": p, "Total Points": pts}
        for p, pts in tally.items()
    ]).sort_values(by="Total Points", ascending=False).reset_index(drop=True)

    if sum(tally.values()) == 0:
        st.info("No votes cast yet. Be the first to cast your ballot above!")
    else:
        st.dataframe(df_tally, use_container_width=True, hide_index=True)

    # Ballots Breakdown expander
    with st.expander("Inspect Individual Ballots Cast:"):
        if not ballots:
            st.write("No ballots on file.")
        for user, b in ballots.items():
            st.write(f"**{user}** ({b.get('timestamp', '')}): 1st: `{b['first']}`, 2nd: `{b['second']}`, 3rd: `{b['third']}`")

    # SUBSECTION C: GROUP DISCUSSION FEED
    st.markdown("---")
    st.markdown("#### Crew Discussion & Notes")
    st.caption("Leave thoughts on gear, reservations, flight bookings, or hiking routes.")

    with st.form("comment_form"):
        new_comment = st.text_area("Add a comment:", placeholder="e.g., Getting mauled by a bear is rough, but I'm down if we split lodging.")
        comment_park = st.selectbox("Tag a Specific Park (Optional):", ["General / All Parks"] + all_parks)
        submit_comment = st.form_submit_button("Post Comment")

        if submit_comment:
            if new_comment.strip():
                data_store["comments"].insert(0, {
                    "author": current_user,
                    "park": comment_park,
                    "text": new_comment.strip(),
                    "timestamp": datetime.now().strftime("%b %d, %Y - %I:%M %p")
                })
                save_data(data_store)
                st.success("Comment posted!")
            else:
                st.warning("Please type a comment before posting.")

    # Render Comments Feed
    st.markdown("##### Recent Messages:")
    comments = data_store.get("comments", [])
    if not comments:
        st.caption("No comments posted yet.")
    else:
        for c in comments:
            st.markdown(f"**{c['author']}** · *{c['timestamp']}* · `Tag: {c.get('park', 'General')}`")
            st.write(f"> {c['text']}")
            st.divider()

# 8. SPANISH INQUISITION
elif view_choice == "⚔️ Spanish Inquisition":
    st.subheader("⚠️ ATTENTION TRAVELERS!")
    st.markdown("""
    <h2 style='color: #B85D19 !important; text-align: center;'>
        NOBODY EXPECTS THE SPANISH INQUISITION!
    </h2>
    """, unsafe_allow_html=True)

    svg_cartoon = """
    <div style="display: flex; justify-content: center; margin-bottom: 16px;">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 450" width="100%" height="auto" style="border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.25); background: #2B1810;">
        <rect width="700" height="450" fill="#2B1810"/>
        <rect x="0" y="320" width="700" height="130" fill="#1C100B"/>
        <g transform="translate(100, 110)">
            <path d="M-50 240 L-20 60 L40 60 L70 240 Z" fill="#B31B1B"/>
            <circle cx="10" cy="20" r="30" fill="#FAD02C"/>
            <path d="M-20 15 Q10 -15 40 15 L42 28 Q10 0 -22 28 Z" fill="#4A2E18"/>
            <circle cx="-3" cy="20" r="10" fill="#333" stroke="#D4AF37" stroke-width="3"/>
            <circle cx="23" cy="20" r="10" fill="#333" stroke="#D4AF37" stroke-width="3"/>
        </g>
        <g transform="translate(500, 110)">
            <path d="M-50 240 L-20 60 L40 60 L70 240 Z" fill="#B31B1B"/>
            <circle cx="10" cy="20" r="30" fill="#F5CBA7"/>
            <ellipse cx="10" cy="0" rx="45" ry="12" fill="#801111"/>
        </g>
        <g transform="translate(300, 70)">
            <path d="M-65 280 L-30 65 L80 65 L115 280 Z" fill="#D32F2F"/>
            <circle cx="25" cy="20" r="35" fill="#FAD02C"/>
            <ellipse cx="25" cy="-8" rx="85" ry="20" fill="#9A0007"/>
            <path d="M-25 90 L-80 50 L-130 50" stroke="#D32F2F" stroke-width="26" stroke-linecap="round"/>
        </g>
        <g transform="rotate(-11 350 225)">
            <rect x="20" y="188" width="650" height="70" fill="#E65100" stroke="#FFD54F" stroke-width="4" rx="8"/>
            <text x="345" y="235" font-family="'Impact', 'Arial Black', sans-serif" font-size="28" fill="#FFFFFF" text-anchor="middle">
                THE ORIGINAL WAS COPYRIGHT PROTECTED
            </text>
        </g>
    </svg>
    </div>
    """
    st.markdown(svg_cartoon, unsafe_allow_html=True)
    st.markdown("""
    > *"Our chief weapon is surprise! Surprise and fear... fear and surprise... our two weapons are fear and surprise... and ruthless efficiency!"*
    """)
    st.caption("Now that the cardinals have audited your itinerary, please return to selecting your national park.")
