# Sakib Anwar — Jekyll Site (GitHub Pages)

This repo is configured for a **user site** at <https://sakibanwar.github.io>. If you prefer a project site, rename the repo and set `baseurl` in `_config.yml` accordingly.

## Local preview
```bash
bundle install
bundle exec jekyll serve
# open http://localhost:4000/
```

## Deploy (GitHub Pages)
- Default branch: `main`.
- Deployment: GitHub Actions workflow in `.github/workflows/pages.yml`.
- After pushing, visit the repo’s **Settings → Pages** to see the published URL.

## Custom domain (later)
When you’re ready to use `sakibanwar.com`:
1. Add the domain under **Settings → Pages → Custom domain**.
2. Add a `CNAME` file in the repo root containing only:
   ```
   sakibanwar.com
   ```
3. Create DNS records at your registrar per GitHub’s docs (A/AAAA to GitHub Pages).
