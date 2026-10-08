# sakibanwar.github.io

Personal academic website of Sakib Anwar. Built with Jekyll and hosted free on GitHub Pages.
Every time a change is saved to this repository, GitHub rebuilds the site automatically
(it takes about a minute).

**You never need to edit HTML.** All content lives in a handful of simple text files:

| What you want to change | File |
|---|---|
| Papers (add, edit, change status, abstracts, links) | `_data/research.yml` |
| Co-author websites | `_data/people.yml` |
| Home page bio | `index.md` |
| Name, photo, CV link, email, social links, address | `_data/profile.yml` |
| Teaching | `_data/teaching.yml` |
| Talks | `_data/talks.yml` |
| CV page | `_data/cv.yml` |

---

## Option 1: edit with forms (recommended)

[Pages CMS](https://pagescms.org) is a free editor that gives you proper forms
(dropdowns, text boxes, upload buttons) for this repository. It is already configured
(see `.pages.yml`).

**One-time setup**

1. Go to <https://app.pagescms.org> and sign in with GitHub.
2. When asked, install the Pages CMS GitHub app and give it access to the
   `sakibanwar.github.io` repository.
3. Open the repository. You will see a menu: *Research & papers*, *Co-authors*,
   *Home page bio*, *Profile & contact*, *Teaching*, *Talks*, *CV page*.

**Day to day**

- **Add a paper:** *Research & papers* → *Add an entry* under Papers → fill in the title,
  choose a status, add co-authors and buttons → **Save**.
- **A working paper got accepted:** open it, change *Status* to *Published*, fill in
  *Journal* and *Volume, pages, year*, clear the *Status note* → **Save**.
- **R&R / under review:** just change the *Status note*, e.g.
  `Revise and Resubmit at *Games and Economic Behavior*`.
- **Reorder papers:** drag them in the list. The page shows them in the same order.
- **Upload a PDF** (paper or CV): use the PDF upload field. Files are stored in
  `assets/uploads/`.

Each **Save** is a commit to GitHub; the live site updates about a minute later.

## Option 2: edit directly on GitHub

Open a file on github.com (e.g. `_data/research.yml`), click the pencil icon, edit, and
click **Commit changes**. To add a paper, copy an existing one and change the text:

```yaml
  - title: "My New Paper: An Experiment"
    status: working            # published, working or progress
    coauthors:
      - Konstantinos Georgalos
    url: ""                    # where the title links to (optional)
    journal: ""                # for published papers
    details: ""                # e.g. 27, 820–853 (2024)
    note: Under review         # *stars* make italics
    links:
      - label: arXiv
        url: https://arxiv.org/abs/xxxx.xxxxx
    pdf: ""
    abstract: >-
      Paste the abstract here, indented like this.
```

YAML tips: keep the indentation exactly as in the examples (spaces, not tabs), and put a
title in "quotes" if it contains a colon. If a change breaks the build, GitHub emails you
and the site simply keeps showing the previous version until it's fixed.

## Option 3: preview on your own computer (optional)

Needs Ruby. From this folder:

```bash
bundle install
bundle exec jekyll serve
```

Then open <http://localhost:4000>.

## Using www.sakibanwar.com

The site is published at <https://sakibanwar.github.io>. To move the custom domain
over from Google Sites:

1. In this repo: **Settings → Pages → Custom domain**, enter `www.sakibanwar.com`, save.
2. At your domain registrar, point `www` to `sakibanwar.github.io` with a CNAME record,
   and the bare domain to GitHub's IP addresses (A records `185.199.108.153`,
   `185.199.109.153`, `185.199.110.153`, `185.199.111.153`).
3. Once it works, tick **Enforce HTTPS** and change `url:` in `_config.yml` to
   `https://www.sakibanwar.com`.

## Changing the look

Colours and fonts are at the top of `assets/css/style.css`. The menu order is in
`_config.yml` under `nav:`.
