"""Step 3c: About page - remove the dead website address and add a short project description.
Runs after spelling.py.  Usage: python3 -I content.py index.html
"""
import re, html, sys

path = sys.argv[1]
src = open(path, encoding='utf-8').read()

OLD = '''The main duty of the player in this game is to deliver some cargos containing silk from Iran to a neighboring country on the silk road in a limited time. The game lets the player choose the season they want to play in and prepare for the journey by doing the necessary shopping. As a bonus, the player is also provided with the shortest possible routes for the journey, calculated beforehand with GIS for path selection.
You could also visit our website presenting the gathered caravanserais’ data and photos supported by an interactive map.

The game is in Alpha version; So, the game is playable, but it is incomplete.

The //Sericum Via// developed by: Sepehr Vaez Afshar & Sarvin Eshaghi

Drweeb.com/Sericumvia
'''

NEW = '''The main duty of the player in this game is to deliver cargoes of silk from Iran to a neighboring country on the Silk Road within a limited time. The game lets the player choose the season they want to play in and prepare for the journey by doing the necessary shopping. As a bonus, the player is also provided with the shortest possible routes for the journey, calculated beforehand with GIS for path selection.

----
''Paper''
Eshaghi, S., Vaez Afshar, S. & Varinlioğlu, G. (2021). //The Sericum Via: A Serious Game for Preserving Tangible and Intangible Heritage of Iran.// ASCAAD 2021, Cairo (online), pp. 306–316. ''Best Presentation Award.''
<a href="https://papers.cumincad.org/cgi-bin/works/Show?ascaad2021_124" target="_blank" rel="noopener">Read the paper on CumInCAD</a>

''Team''
Game design & development: Sepehr Vaez Afshar & Sarvin Eshaghi
Co-author: Assoc. Prof. Dr. Güzden Varinlioğlu
Made in the Architectural Design Computing PhD program, Istanbul Technical University (2020).
'''

# Main menu note, shortened
NOTE_OLD = '''Note: This is the Alpha version!
We recommend you choose the (R)-tagged choices to play the Alpha version of the game.
We will release the Beta version as soon as possible...
The //Sericum Via// developed by: Sepehr Vaez Afshar & Sarvin Eshaghi</p>'''
NOTE_NEW = '''Note: Alpha version. Choose the (R)-tagged options to play.
Developed by Sepehr Vaez Afshar & Sarvin Eshaghi</p>'''

rx = re.compile(r'(<tw-passagedata[^>]*\bname="Learn1\.1"[^>]*>)(.*?)(</tw-passagedata>)', re.S)
m = rx.search(src)
text = html.unescape(m.group(2))
assert text.count(OLD) == 1, 'Learn1.1 text not found'
src = src[:m.start(2)] + html.escape(text.replace(OLD, NEW), quote=True) + src[m.end(2):]
# Main menu: High scores / Game options were empty placeholder pages
MENU_OLD = "[[Learn about the Sericum Via (R)|Learn about the game theory]]\n\n[[Game options|Option]]\n\n[[High scores]]<br />"
MENU_NEW = "[[Learn about the Sericum Via (R)|Learn about the game theory]]<br />"
rx = re.compile(r'(<tw-passagedata[^>]*\bname="Welcome to Sericum Via"[^>]*>)(.*?)(</tw-passagedata>)', re.S)
m = rx.search(src)
text = html.unescape(m.group(2))
assert text.count(MENU_OLD) == 1, 'menu text not found'
text, n = re.subn(r'Note: This is the Alpha version!.*?Eshaghi</p>', lambda _: NOTE_NEW, text, flags=re.S)
assert n == 1, 'menu note not found'
text = text.replace(MENU_OLD, MENU_NEW)
src = src[:m.start(2)] + html.escape(text, quote=True) + src[m.end(2):]
open(path, 'w', encoding='utf-8').write(src)
print('about page + menu updated')
