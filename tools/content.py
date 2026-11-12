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

# About page as small, separated cards (styled by .sv-about / .sv-card in ux.py).
# Kept on few lines on purpose: Harlowe turns every newline into a line break.
NEW = ('<div class="sv-about">'
       '<div class="sv-card"><div class="sv-h">How to play</div>'
       'Deliver cargoes of silk from Iran to a neighboring country on the Silk Road within a limited time. '
       'Choose your season, shop for the journey, and use the shortest routes calculated with GIS as a bonus.'
       '<div class="sv-dim">Alpha version: playable but incomplete.</div></div>'
       '<div class="sv-card"><div class="sv-h">Paper</div>'
       'Eshaghi, S., Vaez Afshar, S. &amp; Varinlioğlu, G. (2021). '
       '<i>The Sericum Via: A Serious Game for Preserving Tangible and Intangible Heritage of Iran.</i> '
       'ASCAAD 2021, Cairo (online), pp. 306–316.'
       '<div class="sv-award">★ Best Presentation Award</div>'
       '<a class="sv-ext" href="https://papers.cumincad.org/cgi-bin/works/Show?ascaad2021_124" target="_blank" rel="noopener">Read the paper on CumInCAD</a></div>'
       '<div class="sv-card"><div class="sv-h">Team</div>'
       '<div class="sv-row"><span class="sv-k">Design &amp; development</span>Sepehr Vaez Afshar &amp; Sarvin Eshaghi</div>'
       '<div class="sv-row"><span class="sv-k">Co-author</span>Assoc. Prof. Dr. Güzden Varinlioğlu</div>'
       '<div class="sv-row"><span class="sv-k">Made at</span>Architectural Design Computing PhD program, Istanbul Technical University, 2020</div>'
       '</div></div>')

# Every page gets a header with a Home button (the script in ux.py adds Back next to it).
HEADER = ('<div class="sv-bar">(unless: (passage:)\'s name is "Welcome to Sericum Via")'
          '[[[⌂ Home->Welcome to Sericum Via]]]</div>')

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

# One Learn page: the "game theory" intro plus How to play / Paper / Team, no Continue step.
ABOUT_CARD = ('<div class="sv-card"><div class="sv-h">About the game</div>'
              'This serious game aims to contribute to the preservation of Iran\'s heritage by bringing information on the '
              'Safavid caravanserais of the Silk Road to as many people as possible. It conveys their intangible heritage too: '
              'the Silk Road as a trade route, the dangers merchants faced, the role of caravanserais, and other values of Iran '
              'such as ceremonies and poems. Players also learn about the climatic zones of Iran along the way.</div>')
assert NEW.startswith('<div class="sv-about">')
LEARN = (NEW.replace('<div class="sv-about">', '<div class="sv-about">' + ABOUT_CARD, 1)
         + '\n[[Start the new game|Stage1]] &nbsp;·&nbsp; [[Back to Main menu|Welcome to Sericum Via]]')
rx = re.compile(r'(<tw-passagedata[^>]*\bname="Learn about the game theory"[^>]*>)(.*?)(</tw-passagedata>)', re.S)
m = rx.search(src)
assert '[[Continue |Learn1.1]]' in html.unescape(m.group(2)), 'learn intro not found'
src = src[:m.start(2)] + html.escape(LEARN, quote=True) + src[m.end(2):]
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

# Header passage (Harlowe shows passages tagged "header" at the top of every passage)
assert 'name="SV Header"' not in src
header_pd = ('<tw-passagedata pid="900" name="SV Header" tags="header" position="100,100" size="100,100">'
             + html.escape(HEADER, quote=True) + '</tw-passagedata>')
i = src.index('</tw-storydata>')
src = src[:i] + header_pd + src[i:]
open(path, 'w', encoding='utf-8').write(src)
print('about page + menu updated')
