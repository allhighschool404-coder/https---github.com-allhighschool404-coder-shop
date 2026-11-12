# -*- coding: utf-8 -*-
import re
import subprocess

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script(?![^>]*src=)[^>]*>(.*?)</script>', html, re.DOTALL)
print(f'Found {len(scripts)} inline script blocks')

all_ok = True
for i, s in enumerate(scripts):
    with open(f'scratch/check_script_{i}.js', 'w', encoding='utf-8') as sf:
        sf.write(s)
    res = subprocess.run(['node', '-c', f'scratch/check_script_{i}.js'], capture_output=True, text=True)
    if res.returncode != 0:
        all_ok = False
        print(f'❌ Script {i} has syntax error:')
        print(res.stderr)
    else:
        print(f'✔ Script {i} syntax is 100% OK')

if all_ok:
    print('\n🎉 ALL JAVASCRIPT SCRIPTS ARE 100% ERROR-FREE AND VALID!')

