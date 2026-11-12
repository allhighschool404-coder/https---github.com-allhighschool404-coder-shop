# -*- coding: utf-8 -*-
with open('templates/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Extract the modal block that got mistakenly placed inside const footer
start_marker = '    <!-- Photo Engineering: 4R/A4 Print Sheet Modal -->'
end_marker = '    </div>\n\n</body>'

p1 = text.find(start_marker)
p2 = text.find(end_marker, p1) + len('    </div>\n')

modals_block = text[p1:p2].strip()
print('Modals block found, length:', len(modals_block))

# Find the exact bad footer region
s_footer = text.find('const footer = "</div>')
e_footer = text.find('</html>";\n            const fileContent', s_footer) + len('</html>";')

bad_footer = text[s_footer:e_footer]
print('Bad footer length:', len(bad_footer))

fixed_text = text.replace(bad_footer, 'const footer = "</div></body></html>";')

# Place modals before real </body> at the end of the file
real_body = '</body>\n\n</html>'
if real_body in fixed_text:
    fixed_text = fixed_text.replace(real_body, f'{modals_block}\n</body>\n\n</html>')
    print('Placed modals before real </body>')
else:
    real_body2 = '</body>\n</html>'
    if real_body2 in fixed_text:
        fixed_text = fixed_text.replace(real_body2, f'{modals_block}\n</body>\n</html>')
        print('Placed modals before real </body> (variant 2)')
    else:
        print('Warning: real_body not found!')

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(fixed_text)

print('Updated index.html successfully!')

