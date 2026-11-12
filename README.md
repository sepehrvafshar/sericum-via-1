# The Sericum Via

*Journey along the Silk Road.* A text-based serious game about the Safavid caravanserais on Iran's Silk Roads, made with Twine (Harlowe 3.1) in 2020.

**Paper:** Eshaghi, S., Vaez Afshar, S. & Varinlioğlu, G. (2021). *The Sericum Via: A Serious Game for Preserving Tangible and Intangible Heritage of Iran.* ASCAAD 2021, Cairo (online), pp. 306–316. **Best Presentation Award.** [CumInCAD](https://papers.cumincad.org/cgi-bin/works/Show?ascaad2021_124)

**Team:** game design and development by Sepehr Vaez Afshar and Sarvin Eshaghi, with Assoc. Prof. Dr. Güzden Varinlioğlu. Made in the Architectural Design Computing PhD program at Istanbul Technical University (2020).

## Preservation edition

This repository preserves the original Alpha version from 1 November 2020, with the same levels, story and artwork. The changes are:

- **Images:** every image and GIF is stored in `site/assets/` instead of being hot-linked from ImgBB.
- **Game logic:** the stores now charge only when you click. Leaving and returning to a page no longer charges twice, and coins can't go negative. The Easy route now shows the right number of days.
- **Text:** spelling and grammar are fixed.
- **Usability:**
  - The game works on mobile and has a Back button.
  - Number keys 1–9 pick a choice.
  - Images are centred and sized to fit the screen.
  - The font is stored locally, so the game works offline.
- **Menu and pages:** the empty "High scores" and "Game options" items are removed, and the Learn page now has the paper and the team.

## Layout

| Path | What it is |
|---|---|
| `site/` | The playable game. Cloudflare Pages serves this folder. |
| `source/original/` | The untouched final Twine export, 1 November 2020. |
| `source/original/earlier/` | Earlier versions: 22 June 2020 and 8 October 2020. |
| `source/assets/`, `source/fonts/`, `source/icon.png` | Images, GIFs, the font and the favicon used by the game. |
| `source/assets-earlier-versions/` | Images used only by the earlier versions. |
| `source/cover.jpg` | Cover artwork. |
| `tools/` | The build steps, applied in order by `build.sh`. |

## Build

```sh
./build.sh            # rebuilds site/ from source/
./build.sh --single   # also writes dist/Sericum_Via_single_file.html (one offline file)
```

This needs only Python 3. There are two ways to change the game:

- Edit the step scripts in `tools/`, then rebuild.
- Edit `site/index.html` directly. A later `./build.sh` overwrites hand edits, so put lasting changes into `tools/`.

## Deploy

The repo is connected to Cloudflare Pages: every push to `main` redeploys the site. Pages settings:

- Framework preset: None
- Build command: none
- Build output directory: `site`
