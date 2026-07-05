# Plant Images

Organize your plant photos here. Each plant has its own folder.

## Structure

```
images/
└── plants/
    ├── monstera/
    ├── pepper/
    ├── tomato/
    ├── basil/
    ├── pothos/
    ├── snake-plant/
    └── spider-plant/
```

## How to Add Photos

1. Drop `.jpg`, `.png`, or `.webp` files into each plant's folder
2. For year-organized photos, add subfolders: `2024/`, `2025/`, `2026/`, etc.

Example:
```
images/plants/tomato/
├── 2024/
│   ├── planting.jpg
│   └── harvest.jpg
└── 2025/
    ├── seedling.jpg
    └── flower.jpg
```

3. Once added, they'll appear on each plant's web page
4. Commit and push to GitHub: `git add . && git commit -m "Add plant photos" && git push`

Supported formats: JPG, PNG, WebP (optimize images before adding for faster load times)
