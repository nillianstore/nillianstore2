import re, html
from pathlib import Path
from collections import defaultdict

root = Path("C:/Users/learn/Documents/Nillianstore/nillianstore2")
SKIP = ('all','nav','post','posts','shop','shops')

def parse_tags(text):
    m = re.match(r'^---\r?\n(.*?)\r?\n---', text, re.S)
    if not m: return []
    tags, in_t = [], False
    for line in m.group(1).split('\n'):
        if line.startswith('tags:'):
            rest = line[5:].strip()
            if rest:
                tags = [t.strip().strip('"').strip("'") for t in rest.strip('[]').split(',') if t.strip()]
            else:
                in_t = True
            continue
        if in_t:
            if line.startswith('  - '):
                tags.append(line[4:].strip().strip('"').strip("'"))
            else:
                in_t = False
    return tags

def safe_slug(s):
    s = html.unescape(str(s)).lower()
    s = re.sub(r"[^a-z0-9-]", '-', s)
    return re.sub(r'-+', '-', s).strip('-')

prod_by_tag, post_by_tag = defaultdict(list), defaultdict(list)
for f in sorted(root.glob('shop/B0*.md')):
    for t in parse_tags(f.read_text(encoding='utf-8')):
        if t in SKIP: continue
        prod_by_tag[safe_slug(t)].append(f.stem)
for f in sorted(root.glob('posts/*.md')):
    for t in parse_tags(f.read_text(encoding='utf-8')):
        if t in SKIP: continue
        post_by_tag[safe_slug(t)].append(f.stem)

all_tags = set(prod_by_tag) | set(post_by_tag)
qual = {s: v for s, v in prod_by_tag.items() if len(v) >= 2}
print("products:", len(list(root.glob('shop/B0*.md'))), "posts:", len(list(root.glob('posts/*.md'))))
print("distinct tag slugs:", len(all_tags))
print("\nQUALIFYING (>=2 products):", len(qual))
for s in sorted(qual):
    print(f"  /tags/{s}/ -> {len(qual[s])} products (+{len(post_by_tag.get(s,[]))} posts)")
thin = [s for s in all_tags if len(prod_by_tag.get(s, [])) < 2]
print(f"\nthin tags (<2 products): {len(thin)}")
print("categories:", {f.name: f for f in []})
cats = defaultdict(list)
for f in sorted(root.glob('shop/B0*.md')):
    m = re.search(r'^category:\s*(.+)$', f.read_text(encoding='utf-8'), re.M)
    if m: cats[m.group(1).strip()].append(f.stem)
print("\nproduct categories:")
for c, v in sorted(cats.items()):
    print(f"  '{c}': {len(v)}")
