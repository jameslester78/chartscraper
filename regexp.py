import re

text_to_search = r'''"james"|"les\nter\n"|"123"
"robert"|"kamada"|"456"
'''

pattern = re.compile(r'(\\n)')
output = pattern.sub(r'',text_to_search)

print (output)