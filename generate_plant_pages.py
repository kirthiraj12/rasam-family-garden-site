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
  </header>
  <main class=\"container\">
    <section class=\"card\">
      <img class=\"plant-image\" src=\"{html.escape(image_path)}\" alt=\"{html.escape(title)}\">
      <p class=\"image-caption\">Photo: {html.escape(image_filename)}</p>
    </section>

    <section class=\"card\">
      <h2>Plant overview</h2>
      <ul>
        <li><strong>Plant name:</strong> {html.escape(title)}</li>
        <li><strong>Location:</strong> Update this with your garden location</li>
        <li><strong>Last watered:</strong> Add your date</li>
        <li><strong>Plant type:</strong> Add annual / perennial / houseplant</li>
      </ul>
    </section>

    <section class=\"card\">
      <h2>Care details</h2>
      <ul>
        <li>Sun: Add your sun requirements</li>
        <li>Water: Add your watering schedule</li>
        <li>Soil: Add the soil type</li>
        <li>Fertilizer: Add fertilizer notes</li>
      </ul>
    </section>

    <section class=\"card\">
      <h2>Notes</h2>
      <p>Add your personal experience, pests, harvest months, and recipes here.</p>
      <p><a href=\"../index.html\">← Back to home</a></p>
    </section>
  </main>
  <footer class=\"site-footer\">© 2026 Family Garden</footer>
</body>
</html>"""


def make_index_html(items: list[tuple[str, str]]) -> str:
    cards = []
    for title, page in items:
        cards.append(
            f"      <article class='card'>\n        <h2><a href='{html.escape(page)}'>{html.escape(title)}</a></h2>\n        <p>View the plant photo and care page for {html.escape(title)}.</p>\n      </article>"
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
    <section class=\"grid\">
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

    pages: list[tuple[str, str]] = []
    for image_file in image_files:
        stem = image_file.stem
        title = titleize(stem)
        slug = slugify(stem)
        page_name = f"{slug}.html"
        page_path = PLANT_DIR / page_name
        image_path = f"../images/{image_file.name}"
        page_html = plant_page_html(title, image_path, image_file.name)
        page_path.write_text(page_html, encoding="utf-8")
        pages.append((title, f"plants/{page_name}"))

    INDEX_FILE.write_text(make_index_html(pages), encoding="utf-8")

    for old_page in OLD_SAMPLE_PAGES:
        old_path = PLANT_DIR / old_page
        if old_path.exists():
            old_path.unlink()

    print(f"Generated {len(pages)} plant pages and updated {INDEX_FILE}")


if __name__ == "__main__":
    main()
