"""Configuração central do mounja-carousel-v2."""
from pathlib import Path

# ============ API KEYS ============
GEMINI_API_KEY = "AIzaSyCyIhIK8eAB2-wwtVQHrvEIMN1oME0IKN4"
GEMINI_IMAGE_MODEL = "gemini-2.5-flash-image"
GEMINI_TEXT_MODEL = "gemini-2.5-flash"  # usado pelo generate_copy.py

# ============ BRAND ============
BRAND_HANDLE = "@mounja.app"
BRAND_CTA = "Link na bio"

# Paleta oficial Mounjá (extraída do logo)
COLORS = {
    "brand_pink":    (240, 51, 158),   # #F0339E
    "brand_magenta": (232, 56, 140),   # #E8388C
    "brand_purple":  (123, 44, 191),   # #7B2CBF
    "brand_indigo":  (91, 33, 182),    # #5B21B6
    "bg_cream":      (250, 246, 240),  # #FAF6F0
    "text_dark":     (26, 22, 37),     # #1A1625
    "text_muted":    (107, 91, 122),   # #6B5B7A
    "divider":       (123, 44, 191, 77),  # brand_purple @ 30%
}

# ============ LAYOUT ============
SLIDE_SIZE = (1080, 1350)      # Instagram 4:5 portrait
SAFE_MARGIN = 90               # padding global
ASSET_PADDING = 80             # padding entre asset e borda/texto
TEXT_REGION_RATIO = 0.55       # % do slide ocupado pela área de texto

# Tipografia — tenta achar fontes instaladas, cai em DejaVu como fallback
FONT_CANDIDATES_TITLE = [
    "/usr/share/fonts/truetype/playfair/PlayfairDisplay-Black.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
]
FONT_CANDIDATES_BODY = [
    "/usr/share/fonts/truetype/inter/Inter-Medium.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]
FONT_CANDIDATES_HANDLE = [
    "/usr/share/fonts/truetype/inter/Inter-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]

FONT_SIZE_TITLE = 78
FONT_SIZE_BODY = 38
FONT_SIZE_HANDLE = 26

# ============ PATHS ============
SKILL_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = SKILL_ROOT / "assets"
LOGO_PATH = ASSETS_DIR / "logo.png"
OUTPUTS_BASE = Path("/sessions/adoring-determined-franklin/mnt/Claude/mounja-carousel-v2/outputs")

META_PROMPT_COPY = SKILL_ROOT / "meta_prompt_copy.md"
META_PROMPT_IMAGE = SKILL_ROOT / "meta_prompt_image.md"

# ============ LIMITS ============
MIN_SLIDES = 5
MAX_SLIDES = 15
MAX_ASSET_RETRIES = 2
