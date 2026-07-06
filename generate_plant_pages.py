from __future__ import annotations
import html
import json
import re
from pathlib import Path

SITE_DIR = Path(__file__).resolve().parent
IMAGE_DIR = SITE_DIR / "images"
PLANT_DIR = SITE_DIR / "plants"
INDEX_FILE = SITE_DIR / "index.html"
SITE_TITLE = "Rasam Family Garden"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

OLD_SAMPLE_PAGES = {
  "pepper.html",
  "tomato.html",
  "basil.html",
  "pothos.html",
  "snake-plant.html",
}

PLANT_DETAILS = {
    "curry-leaf-tree": {
        "category": "Herbs",
        "scientific_name": "Murraya koenigii",
        "plant_type": "Evergreen shrub",
        "hardiness": "USDA 9–12",
        "bloom_time": "Spring to summer",
        "location": "Sunny patio or bright kitchen window",
        "date_planted": "Add your planting date",
        "last_watered": "Check soil weekly",
        "notes": "A fragrant culinary herb that is especially useful in Indian cooking.",
        "sun": "Bright light with some direct sun.",
        "water": "Water when the top 1–2 inches of soil feel dry.",
        "soil": "Fertile, well-draining potting mix.",
        "fertilizer": "Feed lightly with a balanced liquid feed during active growth.",
        "pruning": "Prune lightly to keep the plant compact and productive.",
        "companions": "Pairs well with basil, mint, and ginger in containers.",
    },
    "downtown-miami-magic": {
        "category": "Other",
        "scientific_name": "Unknown cultivar",
        "plant_type": "Ornamental foliage plant",
        "hardiness": "USDA 10–11",
        "bloom_time": "Seasonal foliage interest",
        "location": "Indoor bright spot or sheltered patio",
        "date_planted": "Add your planting date",
        "last_watered": "Water when the top inch dries",
        "notes": "A striking statement plant with rich, patterned foliage.",
        "sun": "Bright filtered light is ideal.",
        "water": "Keep lightly moist but not soggy.",
        "soil": "Fast-draining indoor plant mix.",
        "fertilizer": "Use a diluted houseplant feed every month in spring and summer.",
        "pruning": "Remove damaged leaves as needed.",
        "companions": "Works well with other bold-leaf indoor plants.",
    },
    "english-ivy": {
        "category": "Vines & Climbers",
        "scientific_name": "Hedera helix",
        "plant_type": "Evergreen climber",
        "hardiness": "USDA 4–9",
        "bloom_time": "Late summer to fall",
        "location": "Trellis, shelf, or hanging basket",
        "date_planted": "Add your planting date",
        "last_watered": "Water when the top inch dries",
        "notes": "A classic trailing plant that grows quickly in bright indirect light.",
        "sun": "Bright indirect light; some morning sun is fine.",
        "water": "Water evenly and let the top layer dry slightly.",
        "soil": "Loose, well-drained potting mix.",
        "fertilizer": "Feed monthly in spring and summer.",
        "pruning": "Trim to control growth and refresh foliage.",
        "companions": "Good with pothos, philodendron, and other trailing plants.",
    },
    "fiddleleaf-fig": {
        "category": "Indoor Plants",
        "scientific_name": "Ficus lyrata",
        "plant_type": "Indoor tree",
        "hardiness": "USDA 10–12",
        "bloom_time": "Rarely blooms indoors",
        "location": "Bright indoor corner with room to grow",
        "date_planted": "Add your planting date",
        "last_watered": "Water when the top 2 inches dry",
        "notes": "Needs steady light and a little patience to settle in.",
        "sun": "Bright indirect light to a few hours of gentle sun.",
        "water": "Water thoroughly, then allow the top layer to dry.",
        "soil": "Rich, fast-draining indoor mix.",
        "fertilizer": "Feed monthly during spring and summer.",
        "pruning": "Remove damaged leaves and thin crowded growth.",
        "companions": "Beautiful with snake plant and ZZ plant containers.",
    },
    "giant-bird-of-paradise": {
        "category": "Perennials",
        "scientific_name": "Strelitzia nicolai",
        "plant_type": "Tropical perennial",
        "hardiness": "USDA 10–12",
        "bloom_time": "Late winter to spring",
        "location": "Large patio container or protected garden bed",
        "date_planted": "Add your planting date",
        "last_watered": "Water deeply when the top inch dries",
        "notes": "Bold and architectural, excellent for making a strong focal point.",
        "sun": "Full sun to bright partial shade.",
        "water": "Water deeply and regularly during warm months.",
        "soil": "Loamy, well-draining soil.",
        "fertilizer": "Apply a balanced feed every 4–6 weeks in active growth.",
        "pruning": "Cut old leaves at the base as needed.",
        "companions": "Looks great with palms and broad-leaf tropical plants.",
    },
    "happy-bean": {
        "category": "Other",
        "scientific_name": "Phaseolus vulgaris",
        "plant_type": "Edible annual",
        "hardiness": "USDA 3–10",
        "bloom_time": "Summer",
        "location": "Raised bed or sunny container",
        "date_planted": "Add your planting date",
        "last_watered": "Water when the top inch dries",
        "notes": "A productive bean that can be harvested young or mature.",
        "sun": "At least 6 hours of direct sun.",
        "water": "Keep soil consistently moist once flowering starts.",
        "soil": "Rich, well-draining garden soil.",
        "fertilizer": "Use a light feed at planting and again when flowering begins.",
        "pruning": "No heavy pruning needed; harvest often.",
        "companions": "Thrives near corn, cucumbers, and herbs.",
    },
    "hobbit": {
        "category": "Indoor Plants",
        "scientific_name": "Aeschynanthus radicans",
        "plant_type": "Trailing houseplant",
        "hardiness": "USDA 10–12",
        "bloom_time": "Spring to summer",
        "location": "Hanging basket or shelf edge",
        "date_planted": "Add your planting date",
        "last_watered": "Water when the top inch dries",
        "notes": "A compact, cheerful plant with bright flowers and glossy leaves.",
        "sun": "Bright indirect light.",
        "water": "Water when the potting mix starts to dry slightly.",
        "soil": "Airy, well-draining mix.",
        "fertilizer": "Feed lightly once a month in spring and summer.",
        "pruning": "Pinch back to shape after blooming.",
        "companions": "Great alongside other hanging plants.",
    },
    "jade": {
        "category": "Indoor Plants",
        "scientific_name": "Crassula ovata",
        "plant_type": "Succulent",
        "hardiness": "USDA 10–12",
        "bloom_time": "Winter",
        "location": "Bright windowsill or sunny shelf",
        "date_planted": "Add your planting date",
        "last_watered": "Water deeply, then let soil dry out",
        "notes": "A forgiving succulent with thick, glossy leaves.",
        "sun": "Bright light for most of the day.",
        "water": "Water sparingly and avoid sitting in water.",
        "soil": "Fast-draining cactus or succulent mix.",
        "fertilizer": "Feed very lightly once during active growth.",
        "pruning": "Remove dead stems and reshape lightly.",
        "companions": "Works well with echeveria and other drought-tolerant plants.",
    },
    "jasmine": {
        "category": "Flowers",
        "scientific_name": "Jasminum sambac",
        "plant_type": "Fragrant flowering climber",
        "hardiness": "USDA 8–11",
        "bloom_time": "Late spring to summer",
        "location": "Patio planter or trellis",
        "date_planted": "Add your planting date",
        "last_watered": "Water when the top inch dries",
        "notes": "Known for sweet scent and glossy leaves.",
        "sun": "Full sun to light shade.",
        "water": "Keep lightly moist during active growth.",
        "soil": "Well-drained, slightly fertile soil.",
        "fertilizer": "Feed monthly with a balanced fertilizer in spring and summer.",
        "pruning": "Prune after flowering to maintain shape.",
        "companions": "Lovely with roses and other fragrant bloomers.",
    },
    "japanese-maple": {
        "category": "Perennials",
        "scientific_name": "Acer palmatum",
        "plant_type": "Deciduous ornamental tree",
        "hardiness": "USDA 5–8",
        "bloom_time": "Spring growth flush",
        "location": "Garden border or sheltered patio",
        "date_planted": "Add your planting date",
        "last_watered": "Water regularly in dry weather",
        "notes": "A graceful specimen with dramatic foliage and seasonal color.",
        "sun": "Morning sun with afternoon shade is ideal.",
        "water": "Keep soil evenly moist, especially in summer.",
        "soil": "Moist, well-draining, slightly acidic soil.",
        "fertilizer": "Feed lightly in spring with a slow-release blend.",
        "pruning": "Prune lightly for structure and to remove damaged branches.",
        "companions": "Looks elegant with hostas and ferns.",
    },
    "kong-rose": {
        "category": "Flowers",
        "scientific_name": "Rosa chinensis",
        "plant_type": "Flowering shrub",
        "hardiness": "USDA 7–10",
        "bloom_time": "Spring through fall",
        "location": "Sunny garden bed or container",
        "date_planted": "Add your planting date",
        "last_watered": "Water deeply when the top inch dries",
        "notes": "A long-blooming rose with ornamental value and fragrance.",
        "sun": "At least 6 hours of full sun.",
        "water": "Water deeply and let the top layer dry slightly.",
        "soil": "Rich, loamy, well-draining soil.",
        "fertilizer": "Fertilize regularly during the growing season.",
        "pruning": "Deadhead often and prune in late winter or early spring.",
        "companions": "Pairs well with lavender, salvia, and jasmine.",
    },
    "massangeana": {
        "category": "Other",
        "scientific_name": "Ravenala madagascariensis",
        "plant_type": "Tropical foliage plant",
        "hardiness": "USDA 10–12",
        "bloom_time": "Rarely flowers indoors",
        "location": "Bright indoor room or warm patio",
        "date_planted": "Add your planting date",
        "last_watered": "Water when the top inch dries",
        "notes": "A bold tropical plant with fan-like leaves and strong structure.",
        "sun": "Bright indirect light.",
        "water": "Keep lightly moist and avoid waterlogging.",
        "soil": "Fast-draining tropical mix.",
        "fertilizer": "Feed monthly in spring and summer.",
        "pruning": "Remove damaged leaves; avoid hard cutting.",
        "companions": "Looks striking with large-leaf statements and palms.",
    },
    "money-tree": {
        "category": "Indoor Plants",
        "scientific_name": "Pachira aquatica",
        "plant_type": "Indoor tree",
        "hardiness": "USDA 10–12",
        "bloom_time": "Rarely indoors",
        "location": "Bright living room or office",
        "date_planted": "Add your planting date",
        "last_watered": "Water when the top 1–2 inches dry",
        "notes": "Often grown as a cheerful indoor focal point with braided stems.",
        "sun": "Bright filtered light.",
        "water": "Water thoroughly and let excess drain away.",
        "soil": "Well-draining potting soil.",
        "fertilizer": "Feed lightly once a month in warm months.",
        "pruning": "Trim lightly to maintain shape.",
        "companions": "Pairs well with other sculptural indoor plants.",
    },
    "monstera": {
        "category": "Indoor Plants",
        "scientific_name": "Monstera deliciosa",
        "plant_type": "Tropical climber",
        "hardiness": "USDA 10–12",
        "bloom_time": "Late spring to summer",
        "location": "Bright indoor corner or sheltered patio",
        "date_planted": "Add your planting date",
        "last_watered": "Water when the top 1–2 inches dry",
        "notes": "An iconic plant with dramatic split leaves and easy indoor charm.",
        "sun": "Bright indirect light.",
        "water": "Water until excess drains, then let the top layer dry slightly.",
        "soil": "Loose, airy, well-draining mix.",
        "fertilizer": "Use a balanced houseplant feed monthly in active growth.",
        "pruning": "Trim older leaves and guide growth on a moss pole.",
        "companions": "Great with philodendrons and pothos in one collection.",
    },
    "moss-rose": {
        "category": "Flowers",
        "scientific_name": "Portulaca grandiflora",
        "plant_type": "Succulent annual",
        "hardiness": "USDA 9–11",
        "bloom_time": "Summer",
        "location": "Sunny border or container",
        "date_planted": "Add your planting date",
        "last_watered": "Water when the soil is dry to a finger depth",
        "notes": "A bright, drought-tolerant bloomer that loves heat.",
        "sun": "Full sun is best.",
        "water": "Water sparingly and allow the soil to dry between waterings.",
        "soil": "Sandy, fast-draining soil.",
        "fertilizer": "Feed very lightly or skip if planted in rich soil.",
        "pruning": "Remove spent flowers to encourage more bloom.",
        "companions": "Pairs nicely with other sun-loving annuals.",
    },
    "painted-nettle": {
        "category": "Flowers",
        "scientific_name": "Plectranthus scutellarioides",
        "plant_type": "Ornamental foliage plant",
        "hardiness": "USDA 10–12",
        "bloom_time": "Warm months",
        "location": "Bright porch or indoor spot",
        "date_planted": "Add your planting date",
        "last_watered": "Water when the top inch dries",
        "notes": "Valued for vivid foliage and a compact growth habit.",
        "sun": "Bright indirect light with gentle morning sun.",
        "water": "Keep lightly moist but not soggy.",
        "soil": "Fast-draining, nutrient-rich mix.",
        "fertilizer": "Feed monthly during growth.",
        "pruning": "Pinch back to encourage fullness.",
        "companions": "Works well with coleus and other colorful foliage plants.",
    },
    "pathos": {
        "category": "Other",
        "scientific_name": "Epipremnum aureum",
        "plant_type": "Trailing houseplant",
        "hardiness": "USDA 10–12",
        "bloom_time": "Rarely indoors",
        "location": "Hanging basket or shelf",
        "date_planted": "Add your planting date",
        "last_watered": "Water when the top inch dries",
        "notes": "Easy to grow and great for low-to-medium light rooms.",
        "sun": "Medium to bright indirect light.",
        "water": "Water thoroughly, then let the mix dry slightly.",
        "soil": "Loose indoor mix with decent drainage.",
        "fertilizer": "Feed lightly during spring and summer.",
        "pruning": "Trim long vines and remove yellowing leaves.",
        "companions": "Excellent combined with snake plant and philodendron.",
    },
    "perle-von-nuremburg": {
        "category": "Other",
        "scientific_name": "Rose hybrida",
        "plant_type": "Garden rose",
        "hardiness": "USDA 5–9",
        "bloom_time": "Late spring through fall",
        "location": "Sunny rose bed or large container",
        "date_planted": "Add your planting date",
        "last_watered": "Water deeply when the top inch dries",
        "notes": "A classic rose with a soft blush tone and long flowering habit.",
        "sun": "Full sun for best blooming.",
        "water": "Keep evenly moist, especially in heat.",
        "soil": "Rich, well-draining, slightly acidic soil.",
        "fertilizer": "Feed regularly through the growing season.",
        "pruning": "Deadhead and lightly prune after flushes of bloom.",
        "companions": "Lovely with lavender, salvia, and catmint.",
    },
    "petunia": {
        "category": "Flowers",
        "scientific_name": "Petunia hybrida",
        "plant_type": "Annual flowering plant",
        "hardiness": "USDA 9–11",
        "bloom_time": "Spring through fall",
        "location": "Sunny container or porch box",
        "date_planted": "Add your planting date",
        "last_watered": "Water when the top inch dries",
        "notes": "A cheerful, long-blooming annual in bold colors.",
        "sun": "Full sun for best flowering.",
        "water": "Water regularly and avoid completely drying out.",
        "soil": "Fertile, well-drained soil.",
        "fertilizer": "Feed with a bloom booster every week or two.",
        "pruning": "Deadhead to encourage nonstop bloom.",
        "companions": "Great with marigolds, calibrachoa, and basil.",
    },
    "spider-plant": {
        "category": "Indoor Plants",
        "scientific_name": "Chlorophytum comosum",
        "plant_type": "Trailing houseplant",
        "hardiness": "USDA 9–11",
        "bloom_time": "Spring to summer",
        "location": "Bright shelf or hanging basket",
        "date_planted": "Add your planting date",
        "last_watered": "Water when the top inch dries",
        "notes": "Easy care and excellent for brightening indoor rooms.",
        "sun": "Bright indirect light.",
        "water": "Water thoroughly, then let the mix dry slightly.",
        "soil": "Light, well-draining potting mix.",
        "fertilizer": "Feed monthly during active growth.",
        "pruning": "Trim off brown tips and divide pups when needed.",
        "companions": "Works well with pothos and philodendron.",
    },
    "split-leaf-philodendron": {
        "category": "Indoor Plants",
        "scientific_name": "Philodendron bipinnatifidum",
        "plant_type": "Tropical houseplant",
        "hardiness": "USDA 10–12",
        "bloom_time": "Rarely indoors",
        "location": "Bright indoor corner with support",
        "date_planted": "Add your planting date",
        "last_watered": "Water when the top 1–2 inches dry",
        "notes": "A strong, statement-making plant with deeply cut leaves.",
        "sun": "Bright indirect light.",
        "water": "Water until excess drains away.",
        "soil": "Loose, airy mix with excellent drainage.",
        "fertilizer": "Feed monthly during the growing season.",
        "pruning": "Remove old leaves and guide growth on a pole.",
        "companions": "Excellent with monstera and pothos collections.",
    },
    "stevia": {
        "category": "Herbs",
        "scientific_name": "Stevia rebaudiana",
        "plant_type": "Sweet herb",
        "hardiness": "USDA 8–11",
        "bloom_time": "Summer to fall",
        "location": "Sunny container or garden bed",
        "date_planted": "Add your planting date",
        "last_watered": "Water when the top inch dries",
        "notes": "A sweet-tasting herb often grown as a sugar substitute.",
        "sun": "Full sun for the best flavor.",
        "water": "Keep lightly moist and avoid constant sogginess.",
        "soil": "Well-draining, fertile soil.",
        "fertilizer": "Use a light feed every few weeks in warm weather.",
        "pruning": "Pinch stems to encourage branching.",
        "companions": "Enjoys the company of mint, basil, and thyme.",
    },
    "topsy-turvy": {
        "category": "Other",
        "scientific_name": "Unknown cultivar",
        "plant_type": "Decorative specimen",
        "hardiness": "USDA 8–11",
        "bloom_time": "Seasonal display",
        "location": "Patio or bright indoor space",
        "date_planted": "Add your planting date",
        "last_watered": "Water when the top inch dries",
        "notes": "A sculptural plant that adds playful shape and texture.",
        "sun": "Bright filtered light.",
        "water": "Keep moderate moisture without waterlogging.",
        "soil": "Loose indoor potting soil.",
        "fertilizer": "Feed lightly once a month in active growth.",
        "pruning": "Remove damaged growth and reshape gently.",
        "companions": "Works well with other sculptural, modern plants.",
    },
    "tulasi": {
        "category": "Herbs",
        "scientific_name": "Ocimum tenuiflorum",
        "plant_type": "Sacred basil",
        "hardiness": "USDA 10–11",
        "bloom_time": "Summer",
        "location": "Sunny balcony or bright windowsill",
        "date_planted": "Add your planting date",
        "last_watered": "Water when the top inch dries",
        "notes": "An aromatic herb with culinary and cultural significance.",
        "sun": "Full sun for the best growth.",
        "water": "Water regularly, especially in warm weather.",
        "soil": "Rich, fast-draining potting mix.",
        "fertilizer": "Feed with a diluted organic fertilizer every few weeks.",
        "pruning": "Pinch often to encourage bushiness.",
        "companions": "Great with mint, lemon balm, and curry leaf.",
    },
    "turtle-vine": {
        "category": "Vines & Climbers",
        "scientific_name": "Callisia repens",
        "plant_type": "Trailing vine",
        "hardiness": "USDA 10–12",
        "bloom_time": "Spring to summer",
        "location": "Hanging basket or shelf edge",
        "date_planted": "Add your planting date",
        "last_watered": "Water when the top inch dries",
        "notes": "A soft, trailing plant with a tidy, cascading habit.",
        "sun": "Bright indirect light.",
        "water": "Keep lightly moist but not saturated.",
        "soil": "Loose, well-draining mix.",
        "fertilizer": "Feed lightly once a month during growth.",
        "pruning": "Trim to keep the cascade neat.",
        "companions": "Pairs well with other indoor trailing plants.",
    },
    "wandering-dude": {
        "category": "Vines & Climbers",
        "scientific_name": "Tradescantia zebrina",
        "plant_type": "Trailing vine",
        "hardiness": "USDA 9–11",
        "bloom_time": "Spring to summer",
        "location": "Hanging basket or shelf",
        "date_planted": "Add your planting date",
        "last_watered": "Water when the top inch dries",
        "notes": "A colorful trailing plant that brightens any room quickly.",
        "sun": "Bright indirect light; some gentle morning sun is fine.",
        "water": "Water thoroughly, then let the mix dry slightly.",
        "soil": "Fast-draining houseplant mix.",
        "fertilizer": "Feed monthly during warm months.",
        "pruning": "Trim long stems to encourage bushier growth.",
        "companions": "Beautiful beside pothos and spider plant.",
    },
}


def slugify(name: str) -> str:
    value = name.lower().strip()
    value = re.sub(r"[ _]+", "-", value)
    value = re.sub(r"[^a-z0-9-]+", "", value)
    return value or "plant"


def titleize(name: str) -> str:
    name = name.replace("_", " ").replace("-", " ")
    parts = name.split()
    return " ".join(part.capitalize() for part in parts)


def categorize_plant(title: str) -> str:
    title_lower = title.lower()
    categories = [
        ("Flowers", ["rose", "jasmine", "petunia", "moss", "tulasi", "nettle", "flower", "orchid"]),
        ("Vines & Climbers", ["ivy", "vine", "trailing", "climber", "wandering", "turtle"]),
        ("Vegetables", ["tomato", "pepper", "beans", "corn", "lettuce", "carrot", "peas"]),
        ("Herbs", ["basil", "tulasi", "mint", "sage", "rosemary", "thyme", "oregano", "stevia", "curry"]),
        ("Indoor Plants", ["pothos", "snake", "monstera", "jade", "money", "hobbit", "turtle", "wandering", "english", "fiddleleaf", "spider", "philodendron", "fig"]),
        ("Perennials", ["japanese", "maple", "moss", "rose", "ivy", "money", "garden", "bird", "paradise"]),
    ]
    for category, keywords in categories:
        for keyword in keywords:
            if keyword in title_lower:
                return category
    return "Other"


def get_plant_detail(slug: str, title: str) -> dict[str, str]:
    detail = PLANT_DETAILS.get(slug)
    if detail:
        return detail

    category = categorize_plant(title)
    return {
        "category": category,
        "scientific_name": "Plant species",
        "plant_type": "Garden plant",
        "hardiness": "USDA 8–11",
        "bloom_time": "Seasonal bloom",
        "location": "Sunny bed or bright indoor spot",
        "date_planted": "Add your planting date",
        "last_watered": "Water when the top inch dries",
        "notes": "Add your personal observations and growing notes here.",
        "sun": "Bright light with a little direct sun is ideal.",
        "water": "Water regularly and keep the soil evenly moist.",
        "soil": "Well-draining potting mix or garden soil.",
        "fertilizer": "Feed lightly during the growing season.",
        "pruning": "Prune lightly as needed to keep the plant tidy.",
        "companions": "Pair with similar sun-loving plants.",
    }


def search_data_script(items: list[tuple[str, str, str, dict[str, str]]]) -> str:
    data = [{"title": title, "url": page} for title, page, _image, _details in items]
    json_text = json.dumps(data, ensure_ascii=False)
    return f'<script type="application/json" id="plant-search-data">{json_text}</script>'


def plant_page_html(title: str, slug: str, image_path: str, image_filename: str, details: dict[str, str], search_script: str) -> str:
    storage_key = f"plant-data-{slug}"
    image_src = image_path if image_path.startswith("../") else f"../{image_path.lstrip('/')}"
    template = '''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>%%TITLE%% — %%SITE_TITLE%%</title>
  <link rel="stylesheet" href="../styles.css">
</head>
<body>
  <header class="site-header">
    <div class="top-bar">
      <a class="home-button" href="../index.html">Home</a>
      <div class="search-wrapper">
        <input id="plantSearch" class="search-input" type="search" placeholder="Search plants..." aria-label="Search plant names">
        <button id="searchClear" class="search-clear" type="button" aria-label="Clear search">×</button>
      </div>
    </div>
    <button class="theme-toggle" id="themeToggle" type="button" aria-label="Toggle dark mode">☀️</button>
    <h1>%%TITLE%%</h1>
    <p class="tagline">Plant care and location details for your garden</p>
  </header>
  %%SEARCH_SCRIPT%%
  <main class="container">
    <section class="card">
      <img class="plant-image" src="%%IMAGE_PATH%%" alt="%%TITLE%%">
      <p class="image-caption">Photo: %%IMAGE_FILENAME%%</p>
    </section>

    <section class="card weather-card">
      <h2>Current weather (ZIP 60503)</h2>
      <div class="weather-content"></div>
    </section>

    <section class="card section-grid">
      <div>
        <h2>Plant overview</h2>
        <dl class="meta-list">
          <dt>Scientific name</dt>
          <dd class="editable" data-key="scientific_name">%%SCIENTIFIC%%</dd>
          <dt>Plant type</dt>
          <dd class="editable" data-key="plant_type">%%PLANT_TYPE%%</dd>
          <dt>USDA hardiness</dt>
          <dd class="editable" data-key="hardiness">%%HARDINESS%%</dd>
          <dt>Bloom time</dt>
          <dd class="editable" data-key="bloom_time">%%BLOOM_TIME%%</dd>
        </dl>
      </div>

      <div>
        <h2>Plant status</h2>
        <dl class="meta-list">
          <dt>Location</dt>
          <dd class="editable" data-key="location">%%LOCATION%%</dd>
          <dt>Date planted</dt>
          <dd class="editable" data-key="date_planted">%%DATE_PLANTED%%</dd>
          <dt>Last watered</dt>
          <dd class="editable" data-key="last_watered">%%LAST_WATERED%%</dd>
          <dt>Notes</dt>
          <dd class="editable" data-key="notes">%%NOTES%%</dd>
        </dl>
      </div>
    </section>

    <section class="card">
      <h2>Care guide</h2>
      <div class="section-grid">
        <article>
          <h3>Sun</h3>
          <p>%%SUN%%</p>
        </article>
        <article>
          <h3>Water</h3>
          <p>%%WATER%%</p>
        </article>
        <article>
          <h3>Soil</h3>
          <p>%%SOIL%%</p>
        </article>
        <article>
          <h3>Fertilizer</h3>
          <p>%%FERTILIZER%%</p>
        </article>
        <article>
          <h3>Pruning</h3>
          <p>%%PRUNING%%</p>
        </article>
        <article>
          <h3>Companions</h3>
          <p>%%COMPANIONS%%</p>
        </article>
      </div>
    </section>

    <section class="card">
      <h2>Personal notes</h2>
      <div id="personal-notes" class="editable-block" contenteditable="true">%%PERSONAL_NOTES%%</div>
      <p><a href="../index.html">← Back to home</a></p>
    </section>
  </main>
  <footer class="site-footer">© 2026 %%SITE_TITLE%%</footer>
  <script>
    (function(){
      const key = "__STORAGE_KEY__";
      const saved = localStorage.getItem(key);
      let data = saved ? JSON.parse(saved) : {};
      document.addEventListener('DOMContentLoaded', ()=>{
        document.querySelectorAll('.editable').forEach((el)=>{
          const k = el.dataset.key;
          if (data[k]) el.textContent = data[k];
          el.setAttribute('contenteditable','true');
          el.addEventListener('blur', ()=>{
            data[k] = el.textContent.trim();
            localStorage.setItem(key, JSON.stringify(data));
          });
        });
        const notes = document.getElementById('personal-notes');
        if (notes) {
          if (data['personal_notes']) notes.textContent = data['personal_notes'];
          notes.addEventListener('blur', ()=>{
            data['personal_notes'] = notes.textContent.trim();
            localStorage.setItem(key, JSON.stringify(data));
          });
        }
      });
    })();
  </script>
  <script src="../theme.js"></script>  <script src="../search.js"></script>  <script src="../weather.js"></script>
</body>
</html>'''

    out = template.replace('%%TITLE%%', html.escape(title))
    out = out.replace('%%SITE_TITLE%%', SITE_TITLE)
    out = out.replace('%%SEARCH_SCRIPT%%', search_script)
    out = out.replace('%%IMAGE_PATH%%', html.escape(image_src))
    out = out.replace('%%IMAGE_FILENAME%%', html.escape(image_filename))
    out = out.replace('%%SCIENTIFIC%%', html.escape(details.get('scientific_name','')))
    out = out.replace('%%PLANT_TYPE%%', html.escape(details.get('plant_type','')))
    out = out.replace('%%HARDINESS%%', html.escape(details.get('hardiness','')))
    out = out.replace('%%BLOOM_TIME%%', html.escape(details.get('bloom_time','')))
    out = out.replace('%%LOCATION%%', html.escape(details.get('location','')))
    out = out.replace('%%DATE_PLANTED%%', html.escape(details.get('date_planted','')))
    out = out.replace('%%LAST_WATERED%%', html.escape(details.get('last_watered','')))
    out = out.replace('%%NOTES%%', html.escape(details.get('notes','')))
    out = out.replace('%%SUN%%', html.escape(details.get('sun','')))
    out = out.replace('%%WATER%%', html.escape(details.get('water','')))
    out = out.replace('%%SOIL%%', html.escape(details.get('soil','')))
    out = out.replace('%%FERTILIZER%%', html.escape(details.get('fertilizer','')))
    out = out.replace('%%PRUNING%%', html.escape(details.get('pruning','')))
    out = out.replace('%%COMPANIONS%%', html.escape(details.get('companions','')))
    out = out.replace('%%PERSONAL_NOTES%%', html.escape(details.get('personal_notes','Add your experience, pests, recipes, or harvest details here.')))
    out = out.replace('__STORAGE_KEY__', storage_key)
    return out
