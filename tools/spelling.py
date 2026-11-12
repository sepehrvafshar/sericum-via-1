"""Step 3a: spelling / grammar fixes in the visible game text.
Passage names (link targets) are NOT renamed; only what the player reads changes.
Runs after patch.py.  Usage: python3 -I spelling.py index.html
"""
import re, html, sys

path = sys.argv[1]
src = open(path, encoding='utf-8').read()

# Applied to every passage (old text must appear at least once somewhere).
GLOBAL = [
    ('We recommend you to choose (R) tagged choices', 'We recommend you choose the (R)-tagged choices'),
    ('We recommend you choose (R) taged choises', 'We recommend you choose the (R)-tagged choices'),
    ("Hello I'm Akbar. So you're going to travel along the Silk road!", "Hello, I'm Akbar. So you're going to travel along the Silk Road!"),
    ("Well then! you're ready to start. Good Luck!", "Well then! You're ready to start. Good luck!"),
]

# (passage, old, new) - old must occur exactly once in that passage.
FIXES = [
    ('Stage1', 'Which climatic zone do you want to start?', 'In which climatic zone do you want to start?'),
    ('1.Cold and mountainous', 'You must decide which season do you want to start in a cold and mountainous climatic zone?',
     'In which season do you want to start in the cold and mountainous climatic zone?'),
    ('2.Mild and humid', 'You must decide which season do you want to start in a mild and humid climatic zone?',
     'In which season do you want to start in the mild and humid climatic zone?'),
    ('3.Warm and dry', 'You must decide which season do you want to start in a warm and dry climatic zone?',
     'In which season do you want to start in the warm and dry climatic zone?'),
    ('4.Hot and humid', 'You must decide which season do you want to start in a hot and humid climatic zone?',
     'In which season do you want to start in the hot and humid climatic zone?'),

    ('Story', 'At a night, the ruler of Iran had a dream that the year 1000 AH (1591 AD) will be the end of the world. '
              'He feared that his dream come true and he could not continue his reign. Hence, he ordered to build 1000 caravanserais, '
              'if this not happen. Finally, he initiates building them from the year 1009 AH (1600 AD).',
     'One night, the ruler of Iran dreamed that the year 1000 AH (1591 AD) would be the end of the world. '
     'He feared that his dream would come true and that he could not continue his reign. Hence, he ordered 1000 caravanserais '
     'to be built so that it would not happen. Finally, he began building them in the year 1009 AH (1600 AD).'),
    ('Learn about the game theory',
     'The essential goal is to conserve the information related to the Safavid caravanserais of Iran on the Silk Road via conveying them to as much as people possible. '
     'Hence, the intangible heritage of it such as the use of silk road as a commercial transportation way, the circumstances and threats that merchants were facing, '
     'and the purpose of caravanserais had been tried to be transmitted to the player besides the other values of Iran like ceremonies, poems, etc. '
     'The climatic zones of Iran are amongst the other information that the player learns about by being involved in it.',
     'The essential goal is to conserve the information related to the Safavid caravanserais of Iran on the Silk Road by conveying it to as many people as possible. '
     'Hence, we have tried to transmit to the player its intangible heritage, such as the use of the Silk Road as a commercial route, the circumstances and threats '
     'that merchants faced, and the purpose of caravanserais, besides other values of Iran like ceremonies, poems, etc. '
     'The climatic zones of Iran are among the other things the player learns about by playing.'),
    ('Learn1.1',
     'The game lets the player choose the season wants to play and prepare him/herself for the journey by the necessary shopping. '
     'The player has also been provided by the possible shortest routes for the journey as a bonus, calculated previously by GIS for the path selection.',
     'The game lets the player choose the season they want to play in and prepare for the journey by doing the necessary shopping. '
     'As a bonus, the player is also provided with the shortest possible routes for the journey, calculated beforehand with GIS for path selection.'),
    ('Learn1.1', 'The //Sericum Via// developed by: Sepehr Vaez Afshar & Sarvin Eshaghi</p>',
     'The //Sericum Via// developed by: Sepehr Vaez Afshar & Sarvin Eshaghi'),

    ('Select Country', 'Which Country do you want to start?', 'Which country do you want to start from?'),
    ('Select Country2', 'Which Country do you want to trade?', 'Which country do you want to trade with?'),
    ('1.Turkey', "You can't survive without 5 package foods until Turkey!", "You can't survive without 5 food packages until Turkey!"),
    ('2.China', "You can buy food packages from Akbar's Store!", "You can buy food packages from Akbar's store!"),
    ('2.China', "You can't survive without 5 package foods until China!", "You can't survive without 5 food packages until China!"),
    ('Go to store', '(link: "Buy 5 packages food")', '(link: "Buy 5 food packages")'),
    ('Go to store', "Don't spend anymore! You should have at least 250 coins to journey.",
     "Don't spend any more! You should keep at least 250 coins for the journey."),

    ('TurkeyHard', "You have $coin coins. But you don't need to spend it all now. You could also buy foods later from caravanserais on your way.",
     'You have $coin coins.'),
    ('TurkeyHard', 'You could also buy foods later', 'You could also buy food later'),
    ('StoreHard', 'I recommend you to buy at least 10 packages!', 'I recommend buying at least 10 packages!'),
    ('StoreHard', '(link: "5 packages food = 100 coins")', '(link: "5 food packages = 100 coins")'),
    ('StoreHard', "You can't shop anymore! you should have at least 400 coins to continue!",
     "You can't shop any more! You should keep at least 400 coins to continue!"),

    ('Continue on journey', 'Such a cold day and also you are Tired ...', 'Such a cold day, and you are also tired...'),
    ('Talk to People', 'A town residant tells you:', 'A town resident tells you:'),
    ('Talk to People', 'This is some ghazals by our famous poet MUHTASHAM KASHANI.', 'These are ghazals by our famous poet MUHTASHAM KASHANI.'),
    ('Talk to People', '[[Know more about MUHTASHAM KASHANI]]', '[[Learn more about MUHTASHAM KASHANI|Know more about MUHTASHAM KASHANI]]'),
    ('Know more about MUHTASHAM KASHANI', 'One night, he visited Imam al-Mahdi (a) in his dream.', 'One night, he saw Imam al-Mahdi (a) in his dream.'),

    ('Trade with local people', "Hi; I'm Rajab.\nI have some Perfect Iranian Saffron. Do you want to buy?",
     "Hi, I'm Rajab.\nI have some perfect Iranian saffron. Do you want to buy some?"),
    ('Trade with local people', '[[Yes, Sure]]', '[[Yes, sure!|Yes, Sure]]'),
    ('Trade with local people', '[[Know more about Saffron]]', '[[Learn more about saffron|Know more about Saffron]]'),
    ('Trade with local people', '[[No thanks!]]', '[[No, thanks!|No thanks!]]'),
    ('Yes, Sure', "I recommend you to buy at least a package! It's worth as gold; So you can sell it more expensive during your journey.",
     "I recommend buying at least one package! It's worth its weight in gold, so you can sell it for more during your journey."),
    ('Yes, Sure', '(link: "1 package Saffron = 100 coins")', '(link: "1 saffron package = 100 coins")'),
    ('Yes, Sure', '[you should have at least 100 coins to continue!]', '[You should keep at least 100 coins to continue!]'),
    ('Know more about Saffron', "(pronounced /ˈsæfrən/ or /ˈsæfrɒn/)is", "(pronounced /ˈsæfrən/ or /ˈsæfrɒn/) is"),
    ('Know more about Saffron', 'origin,[5] it is', 'origin, it is'),
    ('No thanks!', '[[Thanks Rajab|Continue on journey]]', '[[Thanks, Rajab!|Continue on journey]]'),

    ('c1.3', 'it is 50 km to Fariman River crossing.', 'it is 50 km to the Fariman River crossing.'),
    ('con1.5', 'The river at this point is currently 30 meter across, 1.5 meter deep in the middle. By the way your cammel is so tired!',
     'The river at this point is currently 30 meters across and 1.5 meters deep in the middle. By the way, your camel is very tired!'),
    ('con1.5', '[[Cross the River your self|crossriver1.5]]', '[[Cross the river yourself|crossriver1.5]]'),
    ('lam1.5', 'You have 17 KM ahead to the next caravanserai.', 'You have 17 km ahead to the next caravanserai.'),
    ('str1.5', 'Oops! some of your coins had stolen by robber!', 'Oops! Some of your coins were stolen by a robber!'),
    ('str1.5', 'But your cammel got some energie to continue the road...', 'But your camel got some energy to continue on the road...'),
    ('ttp1.5', 'Have you ever heard Turquoise?', 'Have you ever heard of turquoise?'),
    ('c1.5.1', 'The city of Neyshabur in the northwestern part of Iran', 'The city of Neyshabur in the northeastern part of Iran'),
    ('c1.5.1', 'shaped in to pendants', 'shaped into pendants'),
    ('boat1.5', 'You crossed the route safely.', 'You crossed the river safely.'),
    ('crossriver1.5', 'Oops! You catch a cold.', 'Oops! You caught a cold.'),
    ('c1.6', 'You almost arrive to Virani Ribat Caravanserai.', 'You have almost arrived at Virani Ribat Caravanserai.'),
]

rx_all = re.compile(r'(<tw-passagedata[^>]*>)(.*?)(</tw-passagedata>)', re.S)

for old, new in GLOBAL:
    total = 0
    def sub(m):
        global total
        t = html.unescape(m.group(2)); total += t.count(old)
        return m.group(1) + html.escape(t.replace(old, new), quote=True) + m.group(3)
    src = rx_all.sub(sub, src)
    assert total > 0, 'global not found: ' + old
    print('global x%d: %s' % (total, old[:50]))

for name, old, new in FIXES:
    rx = re.compile(r'(<tw-passagedata[^>]*\bname="%s"[^>]*>)(.*?)(</tw-passagedata>)'
                    % re.escape(html.escape(name, quote=True)), re.S)
    m = rx.search(src)
    assert m, 'passage not found: ' + name
    text = html.unescape(m.group(2))
    n = text.count(old)
    assert n == 1, '%s: expected 1 match, found %d for %r' % (name, n, old[:60])
    src = src[:m.start(2)] + html.escape(text.replace(old, new), quote=True) + src[m.end(2):]
print('passage fixes:', len(FIXES))
open(path, 'w', encoding='utf-8').write(src)
