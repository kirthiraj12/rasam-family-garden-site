from __future__ import annotations
import html
import os
import re
from pathlib import Path

SITE_DIR = Path(__file__).resolve().parent
IMAGE_DIR = SITE_DIR / "images"
PLANT_DIR = SITE_DIR / "plants"
INDEX_FILE = SITE_DIR / "index.html"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

OLD_SAMPLE_PAGES = {
    "monstera.html",
    "pepper.html",
    "tomato.html",
    "basil.html",
    "pothos.html",
    "snake-plant.html",
    "spider-plant.html",
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


def plant_page_html(title: str, image_path: str, image_filename: str) -> str:
    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">
  <title>{html.escape(title)} — Family Garden</title>
  <link rel=\"stylesheet\" href=\"../styles.css\">
</head>
<body>
  <header class=\"site-header\">
    <h1>{html.escape(title)}</h1>
    <p class=\"tagline\">Plant care and location details for your garden</p>
  </header>
  <main class=\"container\">
    <section class=\"card\">
      <img class=\"plant-image\" src=\"{html.escape(image_path)}\" alt=\"{html.escape(title)}\">
      <p class=\"image-caption\">Photo: {html.escape(image_filename)}</p>
    </section>

    <section class=\"card weather-card\">
      <h2>Current weather (ZIP 60503)</h2>
      <div class=\"weather-content\"></div>
    </section>

    <section class=\"card section-grid\">
      <div>
        <h2>Plant overview</h2>
        <dl class=\"meta-list\">
          <dt>Scientific name</dt>
          <dd>Update with scientific name</dd>
          <dt>Plant type</dt>
          <dd>Annual / Perennial / Houseplant</dd>
          <dt>USDA hardiness</dt>
          <dd>Update your zone</dd>
          <dt>Bloom time</dt>
          <dd>Update bloom or harvest season</dd>
        </dl>
      </div>

      <div>
        <h2>Plant status</h2>
        <dl class=\"meta-list\">
          <dt>Location</dt>
          <dd>Update with garden zone or room</dd>
          <dt>Date planted</dt>
          <dd>Update when planted</dd>
          <dt>Last watered</dt>
          <dd>Add your last watering date</dd>
          <dt>Notes</dt>
          <dd>Add quick notes on growth, pests, or progress</dd>
        </dl>
      </div>
    </section>

    <section class=\"card\">
      <h2>Care guide</h2>
      <div class=\"section-grid\">
        <article>
          <h3>Sun</h3>
          <p>Update sun requirements for this plant.</p>
        </article>
        <article>
          <h3>Water</h3>
          <p>Update watering frequency and amount.</p>
        </article>
        <article>
          <h3>Soil</h3>
          <p>Update the soil type and mix.</p>
        </article>
        <article>
          <h3>Fertilizer</h3>
          <p>Update your feed schedule and product.</p>
        </article>
        <article>
          <h3>Pruning</h3>
          <p>Update pruning or maintenance notes.</p>
        </article>
        <article>
          <h3>Companions</h3>
          <p>Update companion plants and placement.</p>
        </article>
      </div>
    </section>

    <section class=\"card\">
      <h2>Personal notes</h2>
      <p>Add your experience, pests, recipes, or harvest details here.</p>
      <p><a href=\"../index.html\">← Back to home</a></p>
    </section>
  </main>
  <footer class=\"site-footer\">© 2026 Family Garden</footer>
  <script src=\"../weather.js\"></script>
</body>
</html>"""


def make_index_html(items: list[tuple[str, str, str]]) -> str:
    cards = []
    for title, page, image in items:
        cards.append(
            f"      <article class='plant-card'>\n        <a href='{html.escape(page)}'>\n          <img src='{html.escape(image)}' alt='{html.escape(title)} thumbnail'>\n          <h2>{html.escape(title)}</h2>\n          <p>Tap to view its care page.</p>\n        </a>\n      </article>"
        )

    cards_html = "\n".join(cards)
    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">
  <title>Family Garden</title>
  <link rel=\"stylesheet\" href=\"styles.css\">
  <meta name=\"description\" content=\"Personal plant garden - care notes and photos\">
</head>
<body>
  <header class=\"site-header\">
    <h1>Family Garden</h1>
    <p class=\"tagline\">Plants I care for and their care notes</p>
  </header>

  <main class=\"container\">
    <section class=\"plant-grid\">
{cards_html}
    </section>
  </main>

  <footer class=\"site-footer\">© 2026 Family Garden</footer>
</body>
</html>"""


def main() -> None:
    if not IMAGE_DIR.exists():
        raise SystemExit(f"Image directory not found: {IMAGE_DIR}")

    PLANT_DIR.mkdir(exist_ok=True)
    image_files = [p for p in sorted(IMAGE_DIR.iterdir()) if p.suffix.lower() in IMAGE_EXTENSIONS and p.is_file()]

    if not image_files:
        raise SystemExit("No image files found in the images directory.")

    pages: list[tuple[str, str, str]] = []
    for image_file in image_files:
        stem = image_file.stem
        title = titleize(stem)
        slug = slugify(stem)
        page_name = f"{slug}.html"
        page_path = PLANT_DIR / page_name
        image_path = f"../images/{image_file.name}"
        page_html = plant_page_html(title, image_path, image_file.name)
        page_path.write_text(page_html, encoding="utf-8")
        pages.append((title, f"plants/{page_name}", f"images/{image_file.name}"))

    INDEX_FILE.write_text(make_index_html(pages), encoding="utf-8")

    for old_page in OLD_SAMPLE_PAGES:
        old_path = PLANT_DIR / old_page
        if old_path.exists():
            old_path.unlink()

    print(f"Generated {len(pages)} plant pages and updated {INDEX_FILE}")


if __name__ == "__main__":
    main()
