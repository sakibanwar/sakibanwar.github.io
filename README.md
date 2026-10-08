# sakibanwar.github.io

Personal academic website **and PDF CV** of Sakib Anwar, built from one set of data files.

```
_data/*.yml  ──►  website (Jekyll)        https://sakibanwar.github.io
     │
     └──────────►  PDF CV (LaTeX)          /assets/cv/Sakib_Anwar_CV.pdf
```

Edit something once (a paper's status, a new talk, a new grant) and both the website and the
PDF CV update. Every change to this repository runs `.github/workflows/build.yml`, which
builds the PDF, builds the site with the PDF inside it, and publishes both together. It takes
about 3 minutes. If anything fails, the live site stays as it was and GitHub emails you.

**You never need to edit HTML or LaTeX.**

| What | File | Website | PDF CV |
|---|---|---|---|
| Papers | `_data/research.yml` | Research page | Research Papers |
| Talks and seminars | `_data/talks.yml` | Talks page | Seminars and Conference Presentations |
| Teaching | `_data/teaching.yml` | Teaching page, CV page | Teaching |
| Employment, education, grants, admin… | `_data/cv.yml` | CV page | (same sections) |
| Name, contact details, links | `_data/profile.yml` | Home page | Header |
| Home page bio | `index.md` | Home page | – |
| Co-author websites | `_data/people.yml` | Research page | – |

### Website only / PDF only

Anything can be kept off one of the two:

- `hide_from_website: true` puts it in the PDF only (e.g. Supervision, Personal)
- `hide_from_cv: true` puts it on the website only (e.g. old awards, poster talks)

This works on whole CV sections and on single papers, talks, modules, grants and links.
A few fields are naturally one-sided: abstracts are website only; journal rankings and
the personal email are PDF only.

---

## Editing with forms (recommended)

[Pages CMS](https://pagescms.org) gives you forms for these files (configured in `.pages.yml`).

1. Go to <https://app.pagescms.org> and sign in with GitHub.
2. Install the Pages CMS GitHub app. Choose **Only select repositories** and pick
   `sakibanwar.github.io`.
3. Open the repository. The menu has *Research & papers, Talks & seminars, Teaching, CV
   sections, Profile & contact, Home page bio, Co-author websites*.

Examples:

- **Paper accepted:** *Research & papers* → open it → Status: *Published*, fill in Journal
  and "Volume, pages, year", clear the note → **Save**.
- **New R&R:** change the note to `**Revise and Resubmit** at ***Journal Name***` → **Save**.
- **New talk:** *Talks & seminars* → add an entry → drag it to the top → **Save**.
- **New grant:** *CV sections* → Grants and Awards → add an entry → **Save**.

## Editing on github.com

Open a file (e.g. `_data/research.yml`), click the pencil icon, edit, **Commit changes**.
Copy an existing entry to add a new one and keep the indentation exactly the same (spaces,
not tabs). Put text in "quotes" if it contains a colon followed by a space.

## Previewing on your own computer (optional)

```bash
python CV/build_cv.py
```

writes `CV/build/cv.tex` and, with LaTeX installed, the PDF at `assets/cv/Sakib_Anwar_CV.pdf`.
The PDF layout lives in `CV/cv_template.tex` (your original CV design).

```bash
bundle install
bundle exec jekyll serve
```

previews the website at <http://localhost:4000>.

## Domain (www.sakibanwar.com)

The domain is registered at GoDaddy and set as this repo's custom domain
(**Settings → Pages**). GoDaddy DNS should have:

| Type | Name | Value |
|---|---|---|
| CNAME | www | sakibanwar.github.io |
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |

and no domain forwarding. Once GitHub's DNS check passes, tick **Enforce HTTPS** in
**Settings → Pages**.

## Changing the look

Website colours and fonts: top of `assets/css/style.css`. Menu: `nav:` in `_config.yml`.
PDF layout: `CV/cv_template.tex`.
