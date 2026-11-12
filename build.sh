#!/bin/sh
# Rebuilds site/ (what Cloudflare Pages serves) from the original 2020 Twine file.
# Optional: ./build.sh --single  also writes dist/Sericum_Via_single_file.html (one offline file).
set -e
cd "$(dirname "$0")"
rm -rf site
python3 -I tools/localize.py source/original/Sericum_Via_1N_2020-11-01.html source/assets site
python3 -I tools/patch.py site/index.html       # step 2: game-logic fixes
python3 -I tools/spelling.py site/index.html    # step 3: spelling and grammar
python3 -I tools/content.py site/index.html     # Learn page + main menu
python3 -I tools/ux.py site/index.html source/fonts source/icon.png   # layout, Back button, image sizing
if [ "$1" = "--single" ]; then
  mkdir -p dist
  python3 -I tools/singlefile.py site dist/Sericum_Via_single_file.html
  echo "wrote dist/Sericum_Via_single_file.html"
fi
echo "site/ is ready"
