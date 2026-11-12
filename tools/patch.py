"""Step 2: game-logic fixes for Sericum Via (Harlowe 3.1.0).
Edits passage text inside <tw-passagedata>; story text, images and styling stay as they were.
Usage: python3 -I patch.py index.html   (edits in place)
"""
import re, html, sys

path = sys.argv[1]
src = open(path, encoding='utf-8').read()

RESET = ('(set: $saffron to 0)(set: $didC14 to false)(set: $didC15 to false)'
         '(set: $didLook to false)(set: $didNap to 0)')

# (passage name, old text, new text). Each old text must occur exactly once in that passage.
FIXES = [
    # --- Hard (R) path: store bought food just by opening the page; fixed so buying happens on click.
    ('TurkeyHard',
     '(set: $food to 0 ) (set: $coin to 1000 )',
     '(set: $food to 0 ) (set: $coin to 1000 )(set: $health to 100)' + RESET),
    ('StoreHard',
     '(if: $coin > 401 )[[5 packages food = 100 coins|StoreHard]] (set: $coin to $coin - 100)\n'
     '(set: $food to $food + 5)\n'
     '(if: $coin <399 ) [You can\'t shop anymore! you should have at least 400 coins to continue!] \n'
     '\n'
     '(if: $coin <=800 ) [[Checkout and continue|StageTurkeyHard]]\n'
     '\n'
     '\n'
     '(set: $health to 100)',
     '(if: $coin >= 500)[(link: "5 packages food = 100 coins")[(set: $coin to it - 100)(set: $food to it + 5)(goto: "StoreHard")]]\n'
     '(if: $coin < 500)[You can\'t shop anymore! you should have at least 400 coins to continue!]\n'
     '\n'
     '(if: $food >= 5)[[[Checkout and continue|StageTurkeyHard]]]'),
    ('StageTurkeyHard',
     '(set: $coin to $coin + 100) (set: $food to $food -5) ', ''),

    # --- Saffron: buying happened on page load, and revisiting Rajab wiped your saffron.
    ('Trade with local people', '\n(set: $saffron to 0)', ''),
    ('Yes, Sure',
     '(if: $coin > 101 )[[1 package Saffron = 100 coins|Yes, Sure]] (set: $coin to $coin - 100)\n'
     '(set: $saffron to $saffron + 1)\n'
     '\n'
     '(if: $coin <101 ) [you should have at least 100 coins to continue!] \n'
     '\n'
     '(if: $coin <101 ) [[Checkout and continue|Continue on journey]]\n'
     '\n'
     '(if: $coin >101 ) [[Checkout and continue|Continue on journey]]',
     '(if: $coin >= 200)[(link: "1 package Saffron = 100 coins")[(set: $coin to it - 100)(set: $saffron to it + 1)(goto: "Yes, Sure")]]\n'
     '(if: $coin < 200)[you should have at least 100 coins to continue!]\n'
     '\n'
     '[[Checkout and continue|Continue on journey]]'),

    # --- Nap: day counter shown before it was reduced (screen showed one day too many).
    ('You may take a nap!',
     '$coin coins | $food food packages',
     '(set: $gamedayTurkeyHard to $gamedayTurkeyHard - 1 )(set: $didNap to $didNap + 1)$coin coins | $food food packages'),
    ('You may take a nap!',
     '(if: $gamedayTurkeyHard > 63 )[[Continue napping!|You may take a nap!]]\n'
     '(set: $gamedayTurkeyHard to $gamedayTurkeyHard - 1 )',
     '(if: $didNap < 3)[[[Continue napping!|You may take a nap!]]]'),
    ('You may take a nap!',
     '(if: $gamedayTurkeyHard < 63 )\n[You are losing your days]',
     '(if: $didNap > 1)[You are losing your days]'),

    # --- Costs were charged again every time you came back to a page (e.g. Back from the map).
    ('c1.4',
     '(set: $health to $health - 10)',
     '(if: $didC14 is not true)[(set: $health to $health - 10)(set: $didC14 to true)]'),
    ('lookAround1.4',
     '(set: $food to $food - 0.5 )',
     '(if: $didLook is not true)[(set: $food to $food - 1)(set: $didLook to true)]'),
    ('c1.5',
     '(set: $health to $health - 10) (set: $gamedayTurkeyHard to $gamedayTurkeyHard - 1)',
     '(if: $didC15 is not true)[(set: $health to $health - 10)(set: $gamedayTurkeyHard to $gamedayTurkeyHard - 1)(set: $didC15 to true)]'),

    # --- Money could go negative.
    ('str1.5',
     '(set: $coin to $coin - 100 )',
     '(set: $coin to (max: 0, $coin - 100))'),
    ('con1.5',
     '[[Rent a boat for 50 Coins|boat1.5]]',
     '(if: $coin >= 50)[[[Rent a boat for 50 Coins|boat1.5]]]'),

    # --- Muhtasham portrait was squashed into 300x300 (real size 300x402).
    ('Know more about MUHTASHAM KASHANI',
     'width="300" height="300"', 'width="300"'),

    # --- Easy path: same store bug, and the day counter on the road was 0.
    ('Go to store',
     '(if: $coin > 250 )[[Buy 5 packages food|Go to store]] (set: $coin to $coin - 250)\n'
     '(set: $food to $food + 5)\n'
     '(if: $coin <500 ) [Don\'t spend anymore! You should have at least 250 coins to journey.]\n'
     '(if: $coin <260 ) [[Start the journey!]]',
     '(if: $coin >= 500)[(link: "Buy 5 packages food")[(set: $coin to it - 250)(set: $food to it + 5)(goto: "Go to store")]]\n'
     '(if: $coin < 500)[Don\'t spend anymore! You should have at least 250 coins to journey.]\n'
     '(if: $food >= 5)[[[Start the journey!]]]'),
    ('Start the journey!',
     '(set: $health to 100)',
     '(set: $health to 100)(set: $gamedayTurkeyHard to $gameDay)' + RESET),
]

def passage_re(name):
    return re.compile(r'(<tw-passagedata[^>]*\bname="%s"[^>]*>)(.*?)(</tw-passagedata>)'
                      % re.escape(html.escape(name, quote=True)), re.S)

for name, old, new in FIXES:
    rx = passage_re(name)
    m = rx.search(src)
    assert m, 'passage not found: ' + name
    text = html.unescape(m.group(2))
    n = text.count(old)
    assert n == 1, '%s: expected 1 match, found %d for %r' % (name, n, old[:60])
    text = text.replace(old, new)
    src = src[:m.start(2)] + html.escape(text, quote=True) + src[m.end(2):]
    print('fixed:', name)

open(path, 'w', encoding='utf-8').write(src)
