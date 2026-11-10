import os, re, json, sys
from html.parser import HTMLParser

ROOT = os.path.expanduser("~/workspace/water-damage-meridian/site")
BASE = "https://waterdamagerepairmeridianid.com"

# collect generated files
gen = set()
for dp, dn, fn in os.walk(ROOT):
    for f in fn:
        p = os.path.join(dp, f)
        rel = os.path.relpath(p, ROOT)
        gen.add(rel)
html_pages = sorted(p for p in gen if p.endswith("index.html") or p == "404.html")
print(f"total files: {len(gen)}  html pages: {len(html_pages)}")

def resolve(link):
    """Return filesystem rel path for an internal link, or None if external/anchor/mail/tel."""
    if not link or link.startswith(("http://", "https://", "mailto:", "tel:", "javascript:", "#")):
        return None
    link = link.split("#")[0].split("?")[0]
    if not link:
        return None
    if link.startswith("/"):
        rel = link.lstrip("/")
    else:
        return None
    if rel == "":
        return "index.html"
    if rel.endswith("/"):
        return rel + "index.html"
    return rel

broken = []
titles = {}
ld_errors = []
ld_counts = {}
leaks = []
LEAK_TOKENS = ["Fishers", "fishers", "Geist", "Hamilton", "clay", "Indiana", "(317)",
               "317-978", "46037", "46038", "46040", "46055", "46060", "Carmel",
               "Noblesville", "Westfield", "McCordsville", "Fortville", "83680",
               "waterdamagerepairfishersin.com"]
for page in html_pages:
    path = os.path.join(ROOT, page)
    txt = open(path, encoding="utf-8").read()
    # links
    for m in re.finditer(r'''(?:href|src)=["']([^"']+)["']''', txt):
        link = m.group(1)
        if link.startswith(("http://", "https://", "mailto:", "tel:", "javascript:", "#", "data:")):
            continue
        r = resolve(link)
        if r is None:
            continue
        if r not in gen:
            broken.append((page, link))
    # title
    tm = re.search(r"<title>(.*?)</title>", txt, re.S)
    title = tm.group(1).strip() if tm else "MISSING TITLE"
    if title in titles:
        print(f"DUP TITLE: {title!r} in {page} and {titles[title]}")
    titles[title] = page
    # JSON-LD
    blocks = re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', txt, re.S)
    ld_counts[page] = len(blocks)
    if not blocks:
        ld_errors.append((page, "no JSON-LD"))
    for b in blocks:
        try:
            json.loads(b)
        except Exception as e:
            ld_errors.append((page, str(e)))
    # leaks
    for tok in LEAK_TOKENS:
        if tok in txt:
            leaks.append((page, tok))
    # phone check: only placeholder allowed
    for m in re.findall(r"\(\d{3}\) \d{3}-\d{4}", txt):
        if m != "(208) 213-9706":
            leaks.append((page, f"phone {m}"))
    for m in re.findall(r"tel:\+\d+", txt):
        if m != "tel:+12082139706":
            leaks.append((page, f"tel {m}"))

print(f"unique titles: {len(titles)} of {len(html_pages)}")
print(f"JSON-LD blocks per page: min={min(ld_counts.values())} max={max(ld_counts.values())}")
print(f"JSON-LD errors: {ld_errors if ld_errors else 'none'}")
print(f"broken internal links: {len(broken)}")
for b in broken[:20]:
    print("  BROKEN:", b)
print(f"leaks: {leaks if leaks else 'none'}")

# sitemap.xml
sm = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
urls = re.findall(r"<loc>(.*?)</loc>", sm)
page_urls = {BASE + ("/" if p == "index.html" else "/" + p[:-len("index.html")]) for p in html_pages if p != "404.html"}
print(f"sitemap urls: {len(urls)}  expected pages (excl 404): {len(page_urls)}")
print(f"sitemap missing: {sorted(page_urls - set(urls))}")
print(f"sitemap extra: {sorted(set(urls) - page_urls)}")
print(f"sitemap wrong-domain: {[u for u in urls if not u.startswith(BASE)]}")
# robots
print("robots.txt:", open(os.path.join(ROOT, "robots.txt")).read().strip().replace("\n", " | "))
