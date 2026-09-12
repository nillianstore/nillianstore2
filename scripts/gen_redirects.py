"""Generate old->new URL redirects for the lowercase permalink migration.

Output: netlify_redirects_old_urls.txt  (one old URL per line, /shop/<UPPER-ASIN>/)
        These 301 -> /shop/<lowercase-asin>/ (exact same path, lowercase).
Idempotent: always regenerates from committed (HEAD) vs working-tree shop files.
"""
import re, subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[1]

def slugs(files):
    slugs = set()
    for line in files.splitlines():
        line = line.strip().replace('\r', '')
        m = re.match(r'^permalink:\s*(/\S+)', line)
        if m:
            slugs.add(m.group(1))
    return slugs

committed = slugs(subprocess.check_output(
    ['git', 'show', 'HEAD'], cwd=root, stderr=subprocess.DEVNULL
).decode('utf-8', 'replace') if False else
    '\n'.join(subprocess.run(
        ['git', 'grep', '-h', 'permalink:', 'HEAD', '--', 'shop/'],
        cwd=root, capture_output=True, text=True
    ).stdout.splitlines()))

worktree = set()
for f in (root / 'shop').glob('B0*.md'):
    for line in f.read_text(encoding='utf-8').splitlines():
        m = re.match(r'^permalink:\s*(/\S+)', line.strip().replace('\r', ''))
        if m:
            worktree.add(m.group(1))

old = {p for p in committed if p != p.lower()}  # committed with uppercase -> need 301
new_upper = {p.lower() for p in old}
missing = new_upper - worktree

lines = sorted(old)
out = root / 'netlify_redirects_old_urls.txt'
out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
print(f'old uppercase permalinks: {len(lines)}')
for l in lines:
    print(' ', l)
print(f'new lowercase permalinks present: {len(new_upper & worktree)}')
if missing:
    print('WARNING missing new permalinks:', sorted(missing))
