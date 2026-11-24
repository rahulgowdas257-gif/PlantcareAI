"""
PlantCare AI - Botanical Theme Styles
Custom CSS styling using Forest Green, Sage Light Green, and Soft Cream/White.
"""

def get_custom_css():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Playfair+Display:ital,wght@0,600;0,700;1,600&display=swap');

    :root {
        --forest-dark: #1b4332;
        --forest-mid: #2d6a4f;
        --forest-emerald: #40916c;
        --sage-light: #74c69d;
        --sage-pale: #b7e4c7;
        --botanical-bg: #d8f3dc;
        --soft-white: #f8faf8;
        --pure-white: #ffffff;
        --earth-amber: #e76f51;
        --warning-yellow: #f4a261;
        --text-charcoal: #1f2937;
        --text-muted: #4b5563;
        --border-light: #e5e7eb;
    }

    /* Streamlit Main Container Font */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Headings */
    h1, h2, h3 {
        color: #1b4332 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }

    /* Main App Header Banner */
    .botanical-hero {
        background: linear-gradient(135deg, #1b4332 0%, #2d6a4f 60%, #40916c 100%);
        color: #ffffff;
        padding: 2.2rem 2.4rem;
        border-radius: 18px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(27, 67, 50, 0.25);
        position: relative;
        overflow: hidden;
    }

    .botanical-hero::after {
        content: "🌿";
        position: absolute;
        right: 25px;
        bottom: 10px;
        font-size: 5.5rem;
        opacity: 0.25;
        transform: rotate(15deg);
        pointer-events: none;
    }

    .botanical-hero h1 {
        color: #ffffff !important;
        margin-bottom: 0.4rem;
        font-size: 2.3rem !important;
        font-weight: 800 !important;
    }

    .botanical-hero p {
        color: #d8f3dc;
        font-size: 1.05rem;
        margin: 0;
        max-width: 80%;
    }

    /* Metric Cards */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
        gap: 1rem;
        margin-bottom: 1.8rem;
    }

    .metric-card {
        background: #ffffff;
        border: 1px solid #d8f3dc;
        border-radius: 14px;
        padding: 1.25rem 1.4rem;
        box-shadow: 0 2px 8px rgba(27, 67, 50, 0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        position: relative;
    }

    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 14px rgba(27, 67, 50, 0.1);
        border-color: #74c69d;
    }

    .metric-title {
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #52796f;
        margin-bottom: 0.35rem;
    }

    .metric-value {
        font-size: 1.9rem;
        font-weight: 800;
        color: #1b4332;
        line-height: 1.1;
    }

    .metric-subtitle {
        font-size: 0.8rem;
        color: #6c757d;
        margin-top: 0.35rem;
    }

    /* Plant Card */
    .plant-card-box {
        background: #ffffff;
        border: 1px solid #e1efe6;
        border-radius: 16px;
        padding: 1.4rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 12px rgba(27, 67, 50, 0.06);
        transition: all 0.25s ease-in-out;
    }

    .plant-card-box:hover {
        border-color: #52b788;
        box-shadow: 0 8px 20px rgba(27, 67, 50, 0.12);
    }

    /* Badges & Tags */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.65rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.02em;
    }

    .badge-urgent {
        background-color: #ffe3e3;
        color: #c92a2a;
        border: 1px solid #ffa8a8;
    }

    .badge-today {
        background-color: #fff3bf;
        color: #e67700;
        border: 1px solid #ffd43b;
    }

    .badge-good {
        background-color: #d8f3dc;
        color: #2d6a4f;
        border: 1px solid #b7e4c7;
    }

    .badge-neutral {
        background-color: #e9ecef;
        color: #495057;
        border: 1px solid #dee2e6;
    }

    .badge-stage {
        background-color: #e8f5e9;
        color: #1b4332;
        border: 1px solid #a3cfbb;
        font-weight: 600;
    }

    /* Botanical Callouts */
    .disclaimer-box {
        background: #fff9db;
        border-left: 4px solid #fcc419;
        padding: 0.85rem 1.1rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-size: 0.9rem;
        color: #664d03;
    }

    .demo-ribbon {
        display: inline-block;
        background: #fff3bf;
        color: #d9480f;
        font-weight: 800;
        font-size: 0.72rem;
        padding: 0.2rem 0.55rem;
        border-radius: 6px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        border: 1px solid #ffd43b;
        margin-right: 0.5rem;
    }

    .info-card {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        color: #166534;
        margin-bottom: 1rem;
    }

    .tip-box {
        background: #eef7f2;
        border-left: 4px solid #40916c;
        padding: 0.8rem 1rem;
        border-radius: 6px;
        font-size: 0.88rem;
        color: #1b4332;
        margin: 0.6rem 0;
    }

    /* Buttons Enhancement */
    div.stButton > button:first-child {
        background-color: #2d6a4f;
        color: #ffffff !important;
        border-radius: 10px;
        font-weight: 600;
        border: none;
        padding: 0.5rem 1.1rem;
        transition: all 0.2s ease;
    }

    div.stButton > button:first-child:hover {
        background-color: #1b4332;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(27, 67, 50, 0.25);
        transform: translateY(-1px);
    }

    /* Secondary / outline buttons */
    div[data-testid="stFormSubmitButton"] > button {
        background-color: #2d6a4f !important;
        color: white !important;
        font-weight: 700 !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #f7faf7;
        border-right: 1px solid #e1efe6;
    }

    /* Smooth Input Fields */
    input, textarea, select {
        border-radius: 8px !important;
    }

    /* Progress bar custom color */
    .stProgress > div > div > div > div {
        background-color: #40916c;
    }

    /* Clean spacing for tab content */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 8px 16px;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        background-color: #e8f5e9 !important;
        color: #1b4332 !important;
    }
    </style>
    """
