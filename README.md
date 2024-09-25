# renskin-django
Repository for Renaissance Skin django project.

`main` branch contains the static version of the site (converted by GN, Sept 2024)

`master` branch and `pre-gitlab` release contain the latest version of the dynamic, django site, before it was converted to static.

## How was the site converted

Mainly using the [static_site.py tool](https://github.com/kingsdigitallab/kdl-deploy-tools).

```bash
python3 static_site.py copy --url renaissanceskin.ac.uk
python3 static_site.py report

find -iname "*.html" | xargs sed -i 's|http://renaissanceskin.ac.uk/|https://renaissanceskin.ac.uk/|g'

find -iname "*.html" | xargs sed -i "s|32x32.png' %}|32x32.png|g"

find -iname "*.html" | xargs sed -i 's|/search"|/search/"|g'

python3 static_site.py redirect
python3 static_site.py relink
python3 static_site.py tag
python3 static_site.py rename

npx pagefind --site html

# edit /search/index.html to work with pagefind

# copied media files from server
```
