# -*- coding: utf-8 -*-
import urllib.request

with urllib.request.urlopen('http://127.0.0.1:5000/') as res:
    html = res.read().decode('utf-8')

assert 'const footer = "</div></body></html>";' in html
print('✔ Live server is serving fixed index.html!')
print('✔ switchTab definition in response:', 'function switchTab(tabName)' in html)
print('✔ photoEngineeringTab in response:', 'id="photoEngineeringTab"' in html)

