"""
Configuration constants, directory paths, mappings, and styling for Strategic HRM Layoffs Project.
"""
from pathlib import Path

# Base Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_PATH = DATA_DIR / "raw" / "layoffs_raw.csv"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
CLEANED_EVENTS_PATH = PROCESSED_DATA_DIR / "layoffs_cleaned_events.csv"
COMPANY_PROFILES_PATH = PROCESSED_DATA_DIR / "layoffs_company_profiles.csv"
FIGURES_DIR = PROJECT_ROOT / "figures"
REPORTS_DIR = PROJECT_ROOT / "reports"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
DASHBOARD_DIR = PROJECT_ROOT / "dashboard"

# Ensure runtime directories exist
for p in [PROCESSED_DATA_DIR, FIGURES_DIR, REPORTS_DIR, NOTEBOOKS_DIR, DASHBOARD_DIR]:
    p.mkdir(parents=True, exist_ok=True)

# Macro-Regime Time Boundaries
MACRO_REGIMES = {
    "COVID_Shock": ("2020-03-01", "2021-12-31", "Phase 1: COVID Shock & Virtualization"),
    "Tech_Boom_Transition": ("2022-01-01", "2022-06-30", "Phase 2: Tech Overhiring & Peak Valuation"),
    "Rate_Hikes_Contraction": ("2022-07-01", "2023-12-31", "Phase 3: Rate Hikes & Tech Contraction"),
    "AI_Structural_Realignment": ("2024-01-01", "2026-12-31", "Phase 4: AI Pivot & Structural Realignment")
}

# Industry Grouping Dictionary (Harmonizing granular niches into coherent sectors)
INDUSTRY_GROUP_MAP = {
    "Retail": "Consumer & Retail",
    "Consumer": "Consumer & Retail",
    "Food": "Consumer & Retail",
    "Travel": "Travel & Transportation",
    "Transportation": "Travel & Transportation",
    "Logistics": "Travel & Transportation",
    "Finance": "Fintech & Financial Services",
    "Crypto": "Fintech & Financial Services",
    "Real Estate": "Real Estate & PropTech",
    "Healthcare": "Healthcare & BioTech",
    "Education": "EdTech & Learning",
    "Marketing": "Marketing & Media",
    "Media": "Marketing & Media",
    "Security": "Enterprise & Infrastructure",
    "Data": "Enterprise & Infrastructure",
    "Infrastructure": "Enterprise & Infrastructure",
    "Support": "Enterprise & Infrastructure",
    "Human Resources": "Enterprise & Infrastructure",
    "Hardware": "Hardware & Manufacturing",
    "Manufacturing": "Hardware & Manufacturing",
    "Aerospace": "Hardware & Manufacturing",
    "Legal": "Professional Services",
    "Recruiting": "Professional Services",
    "Sales": "Professional Services",
    "Other": "Other / Diversified"
}

# Funding Stage Grouping
STAGE_GROUP_MAP = {
    "Seed": "Early Stage (Seed)",
    "Series A": "Early Venture (Series A)",
    "Series B": "Expansion Stage (Series B)",
    "Series C": "Late Stage (Series C-D)",
    "Series D": "Late Stage (Series C-D)",
    "Series E": "Growth Stage (Series E+)",
    "Series F": "Growth Stage (Series E+)",
    "Series G": "Growth Stage (Series E+)",
    "Series H": "Growth Stage (Series E+)",
    "Series I": "Growth Stage (Series E+)",
    "Series J": "Growth Stage (Series E+)",
    "Post-IPO": "Public (Post-IPO)",
    "Acquired": "Acquired / Subsidiary",
    "Private Equity": "Private Equity Owned",
    "Unknown": "Unspecified / Private"
}

# Global Plot Styling Palette (Publication Grade)
COLORS = {
    "primary": "#1f77b4",       # Deep Academic Blue
    "secondary": "#ff7f0e",     # Muted Amber
    "accent": "#2ca02c",        # Forest Green
    "danger": "#d62728",        # Crimson
    "purple": "#9467bd",        # Royal Violet
    "slate": "#7f7f7f",         # Slate Neutral
    "dark_bg": "#1e293b",       # Slate 800
    "card_bg": "#0f172a",       # Slate 900
    "light_bg": "#f8fafc",      # Slate 50
    "grid": "#e2e8f0"           # Slate 200
}
