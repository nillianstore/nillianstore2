"""Phase 1 surgery: normalize categories, lowercase internal shop links in
product bodies and blog posts. Idempotent — safe to re-run."""
import re
from pathlib import Path

root = Path(__file__).resolve().parent.parent
ASIN_RE = re.compile(r"(/shop/)(B0[A-Z0-9]{8})(?=/|\"|'| )")


def lower_shop_links(text: str) -> str:
    # match trailing-slash and no-slash variants; keep any trailing slash present
    return re.sub(
        r"(/shop/)(B0[A-Z0-9]{8})(/?)",
        lambda m: m.group(1) + m.group(2).lower() + m.group(3),
        text,
    )


# 1. Normalize product `category` to lowercase
changed_cat = 0
for f in (root / "shop").glob("B0*.md"):
    t = f.read_text(encoding="utf-8")
    m = re.search(r"^category:\s*(.+?)\s*$", t, re.M)
    if not m:
        print("NO category:", f.name)
        continue
    val = m.group(1).strip().strip('"').strip("'")
    low = val.lower()
    if low != val:
        f.write_text(t.replace(f"category: {val}", f"category: {low}", 1), encoding="utf-8")
        changed_cat += 1
        print("category:", f.name, val, "->", low)

# 2. Lowercase shop links inside product bodies
changed_body = 0
for f in (root / "shop").glob("B0*.md"):
    t = f.read_text(encoding="utf-8")
    t2 = lower_shop_links(t)
    if t2 != t:
        f.write_text(t2, encoding="utf-8")
        changed_body += 1
        print("body links:", f.name)

# 3. Lowercase shop links inside blog posts
changed_post = 0
for f in (root / "posts").glob("*.md"):
    t = f.read_text(encoding="utf-8")
    t2 = lower_shop_links(t)
    if t2 != t:
        f.write_text(t2, encoding="utf-8")
        changed_post += 1
        print("post links:", f.name)

print(f"DONE: categories={changed_cat} bodies={changed_body} posts={changed_post}")
