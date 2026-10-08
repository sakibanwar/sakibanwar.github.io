#!/usr/bin/env python3
"""Build the PDF CV from the same data files that drive the website.

    python CV/build_cv.py            writes CV/build/cv.tex and, if LaTeX is
                                     installed, compiles it and copies the PDF
                                     to the path set as cv_pdf in _config.yml
    python CV/build_cv.py --tex-only only writes CV/build/cv.tex

Needs: pip install pyyaml jinja2
"""
import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "_data"
BUILD = ROOT / "CV" / "build"

SECTION_TITLES = {
    "published": "Publications",
    "working": "Working Papers",
    "progress": "Work in Progress",
}
TALK_TITLES = {"seminar": "Seminars", "conference": "Conference Presentations"}


# --------------------------------------------------------------------------
# Text -> LaTeX
# --------------------------------------------------------------------------
SPECIAL = {
    "\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#",
    "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
}
LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")


def tex(value):
    """Escape plain text for LaTeX and tidy up typography."""
    if value is None:
        return ""
    s = "".join(SPECIAL.get(c, c) for c in str(value).strip())
    s = re.sub(r'"([^"]*)"', r"“\1”", s)                       # "quotes" -> curly quotes
    s = re.sub(r"\b(Prof|Dr|Mr|Mrs|Ms|St|vs)\. ", r"\1.\\ ", s)  # no sentence gap after "Dr."
    s = re.sub(r"(?<![A-Za-z])([A-Z])\. (?=[A-Z])", r"\1.\\ ", s)  # or after initials "K. Georgalos"
    s = s.replace("LaTeX", r"\LaTeX{}")
    s = re.sub(r"\b(Stata|Mathematica)\b", r"\\textsc{\1}", s)
    return s


def emphasis(s):
    s = re.sub(r"\*\*\*(.+?)\*\*\*", r"\\textbf{\\textit{\1}}", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", s)
    return re.sub(r"\*(.+?)\*", r"\\textit{\1}", s)


def url(value):
    return str(value).strip().replace("\\", "/").replace("%", r"\%").replace("#", r"\#")


def md(value):
    """A small Markdown subset (**bold**, *italic*, [text](url)) to LaTeX."""
    if value is None:
        return ""
    links = []

    def stash(m):
        links.append((m.group(1), m.group(2)))
        return f"\x00{len(links) - 1}\x00"

    s = emphasis(tex(LINK.sub(stash, str(value).strip())))
    return re.sub(
        "\x00(\\d+)\x00",
        lambda m: rf"\href{{{url(links[int(m.group(1))][1])}}}{{{emphasis(tex(links[int(m.group(1))][0]))}}}",
        s,
    )


def md_lines(value):
    lines = [line for line in str(value or "").splitlines() if line.strip()]
    return " \\\\\n    ".join(md(line) for line in lines)


def initials(name):
    parts = str(name).split()
    if len(parts) < 2 or re.fullmatch(r"[A-Z]\.", parts[0]):
        return str(name)
    return f"{parts[0][0]}. {parts[-1]}"


def coauthors(names):
    short = [initials(n) for n in names or []]
    text = short[0] if len(short) == 1 else ", ".join(short[:-1]) + " and " + short[-1]
    return tex(text)


def mon(month):
    return str(month or "")[:3]


def compact_modules(place):
    mods = [m for g in place.get("groups") or [] for m in g.get("modules") or []]
    return ", ".join(md(m["name"]) + (f" ({tex(m['dates'])})" if m.get("dates") else "") for m in mods)


# --------------------------------------------------------------------------
# Data
# --------------------------------------------------------------------------
def load(name):
    with open(DATA / f"{name}.yml", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def on_cv(items):
    return [i for i in items or [] if not i.get("hide_from_cv")]


def header_rows(p):
    def item(icon, text, link=None):
        body = rf"\href{{{url(link)}}}{{{tex(text)}}}" if link else tex(text)
        return rf"{icon}\;{body}"

    row1, row2 = [], []
    if p.get("phone"):
        phone = str(p["phone"]).strip()
        if phone.startswith("0"):
            phone = "+44 (0)" + phone[1:]
        digits = re.sub(r"[^\d+]", "", phone.replace("(0)", ""))
        row1.append(item(r"\faPhone", phone, f"tel:{digits}"))
    for key in ("email_personal", "email"):
        if p.get(key):
            row1.append(item(r"\faEnvelope", p[key], f"mailto:{p[key]}"))
    if p.get("website"):
        row2.append(item(r"\faGlobe", re.sub(r"^https?://", "", p["website"]).rstrip("/"), p["website"]))
    if p.get("github"):
        row2.append(item(r"\faGithub", re.sub(r"^https?://(www\.)?", "", p["github"]).rstrip("/"), p["github"]))
    if p.get("google_scholar") and p.get("google_scholar_on_cv"):
        row2.append(item(r"\aiGoogleScholar", "Google Scholar", p["google_scholar"]))
    if p.get("orcid") and p.get("orcid_on_cv"):
        row2.append(item(r"\aiOrcid", re.sub(r"^https?://(www\.)?orcid\.org/", "", p["orcid"]), p["orcid"]))
    if p.get("cv_location"):
        row2.append(item(r"\faMapMarker*", p["cv_location"]))
    return [r for r in (row1, row2) if r]


def build_context():
    profile = load("profile")
    research = load("research")
    teaching = load("teaching")
    talks = load("talks")
    cv = load("cv")

    papers = on_cv(research.get("papers"))
    research_groups = [
        {"status": s, "title": t, "papers": [p for p in papers if p.get("status") == s]}
        for s, t in SECTION_TITLES.items()
    ]
    research_section = next((s for s in cv.get("sections") or [] if s.get("type") == "research"), {})
    if research_section.get("publications_oldest_first"):
        research_groups[0]["papers"].reverse()
    talk_list = on_cv(talks.get("talks"))
    talk_groups = [
        {"title": t, "talks": [x for x in talk_list if x.get("type", "conference") == k]}
        for k, t in TALK_TITLES.items()
    ]
    teaching["qualifications"] = on_cv(teaching.get("qualifications"))
    teaching["textbooks"] = on_cv(teaching.get("textbooks"))
    teaching["places"] = [
        {**place, "groups": [{**g, "modules": on_cv(g.get("modules"))} for g in place.get("groups") or []]}
        for place in on_cv(teaching.get("places"))
    ]

    sections = []
    for s in on_cv(cv.get("sections")):
        s = dict(s)
        s["entries"] = on_cv(s.get("entries"))
        s["lines"] = on_cv(s.get("lines"))
        sections.append(s)

    return {
        "profile": profile,
        "header_rows": header_rows(profile),
        "sections": sections,
        "research": [g for g in research_groups if g["papers"]],
        "teaching": teaching,
        "talks": [g for g in talk_groups if g["talks"]],
    }


# --------------------------------------------------------------------------
def render():
    env = Environment(
        loader=FileSystemLoader(str(ROOT / "CV")),
        block_start_string="((*", block_end_string="*))",
        variable_start_string="(((", variable_end_string=")))",
        comment_start_string="((=", comment_end_string="=))",
        trim_blocks=True, lstrip_blocks=True, keep_trailing_newline=True,
    )
    env.filters.update(tex=tex, md=md, md_lines=md_lines, url=url, coauthors=coauthors,
                       mon=mon, compact_modules=compact_modules)
    out = env.get_template("cv_template.tex").render(**build_context())
    out = re.sub(r"\n{3,}", "\n\n", out)
    BUILD.mkdir(parents=True, exist_ok=True)
    (BUILD / "cv.tex").write_text(out, encoding="utf-8")
    return BUILD / "cv.tex"


def compile_pdf(tex_file):
    if not shutil.which("latexmk"):
        print("LaTeX not found, so only the .tex file was written.")
        return None
    cmd = ["latexmk", "-lualatex", "-interaction=nonstopmode", "-halt-on-error", tex_file.name]
    result = subprocess.run(cmd, cwd=tex_file.parent, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stdout[-3000:])
        sys.exit("LaTeX failed; see CV/build/cv.log")
    with open(ROOT / "_config.yml", encoding="utf-8") as f:
        dest = ROOT / yaml.safe_load(f)["cv_pdf"].lstrip("/")
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(tex_file.with_suffix(".pdf"), dest)
    return dest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--tex-only", action="store_true", help="write the .tex file but don't compile it")
    args = parser.parse_args()
    tex_file = render()
    print(f"Wrote {tex_file.relative_to(ROOT)}")
    if not args.tex_only:
        pdf = compile_pdf(tex_file)
        if pdf:
            print(f"Wrote {pdf.relative_to(ROOT)}")
