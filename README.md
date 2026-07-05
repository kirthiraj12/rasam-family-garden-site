# Family Garden — site

This folder contains a plain HTML/CSS site for the Family Garden. It can be published on GitHub Pages.

Quick publish options:

1) Push `site/` to a `gh-pages` branch:

```bash
cd FamilyGarden/site
git init
git add .
git commit -m "Initial site"
# add remote: git remote add origin git@github.com:YOUR_USER/YOUR_REPO.git
git branch -M gh-pages
git push -u origin gh-pages
```

2) Or copy the contents of `site/` into a `docs/` folder at the repo root and enable Pages from the `main` branch `/docs` folder in the repo settings.

Next steps I can take for you:
- Initialize a Git repo and create a GitHub repo
- Add more plant pages or a CMS-like JSON data source
- Add images and optimize assets
