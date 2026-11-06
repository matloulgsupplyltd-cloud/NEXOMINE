# Lundana Mining Company website

Static HTML/CSS/JS. No build step is needed to deploy: upload this folder to any static host.

## Important: sample content
Company history (founded 2009, Luanda head office, Lunda Norte operations), projects (Mukanda Ridge, Cacuilo Valley, Dundo, Sol Nascente), statistics, leadership names, news, vacancies, document titles and contact details are **illustrative sample content** written to show the finished site. Replace all of it with approved facts before launch. Do not publish financial figures or listing details unless supplied by the company.
The images in `assets/img` are rendered illustrations, not photographs. Replace each file (same filename) with a licensed or company photo.

## Before going live
1. **Content**: edit `build.py` (company data near the top, page text in `build()`) and run `python3 build.py .` to regenerate every page. Remaining yellow dashed text marks details still to be confirmed. Set `SITE["domain"]`.
2. **Photos**: overwrite files in `assets/img` with real photos using the same names, e.g. `hero-open-pit.jpg` (1920px wide, under 300 KB). If you do, remove the image step from `build.py` so they are not regenerated. Also replace `og-image.jpg` (1200x630).
3. **Contact form**: set `data-endpoint` on `<form id="contact-form">` to a form service URL (Formspree, Netlify Forms, your API). Until then it runs in preview mode.
4. **Map**: the contact page embeds a Google Map for the sample Luanda address. Update the `src` in `build.py` to the real address.
5. **Social links**: replace the `href="#"` in the social icons.
6. **Documents**: replace `href="#"` on document cards with PDF paths.
7. Do not publish financial figures, listings or targets until the company supplies and approves them.
