# wordication-legal

Static legal & support site for **Wordication: Word Guess Party**, served by
GitHub Pages at <https://wordication.app> (see `CNAME`).

```
index.html                     landing page (EN) — store links, legal links, contact form
privacy.html  terms.html       current documents, English
<lang>/privacy.html  terms.html    fr, de, es, it, hr, sr
privacy/<version>/...          frozen snapshot of each released version
terms/<version>/...            (EN at index.html, translations at <lang>/index.html)
app-ads.txt                    AdMob + mediation declaration
public/icons/                  store badge icons + wordication-icon.png (favicon,
                               apple-touch-icon and the landing-page header image;
                               copied from ../wordication/assets/images/icon-rounded.png)
_src/                          source of the documents + the generator (not published:
                               GitHub Pages' Jekyll skips paths starting with "_")
```

## Editing the documents

`index.html` is hand-maintained; everything else is generated.
Never edit the generated HTML by hand — the same body is used by 4 pages per
language. Edit `_src/content/<lang>/{privacy,terms}.html` (body only) or
`_src/content/<lang>/strings.json` (page title, "Home" label, version notice),
then regenerate everything:

```sh
python3 _src/build.py
```

All seven languages are required for every change: en, fr, de, es, it, hr, sr.

## Releasing a new version

1. Bump the version and date in the `<p class="meta">` line of every
   `_src/content/<lang>/{privacy,terms}.html` you changed.
2. Set `VERSION` in `_src/build.py` to the new version.
3. Run `python3 _src/build.py`. The current pages are overwritten and a new
   frozen snapshot appears under `privacy/<version>/` and `terms/<version>/`.
   Older snapshots stay untouched, so links handed to the stores keep working.

## TODO before going live

- `index.html` — replace `YOUR_FORM_ID` with the Formspree form id.
- `app-ads.txt` — replace the placeholder AdMob publisher ID, Unity game ids
  and Meta app id (every line marked `# TODO`).
- Point the `wordication.app` DNS at GitHub Pages and enable Pages for this
  repo.
