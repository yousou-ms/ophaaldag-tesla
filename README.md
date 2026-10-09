# Ophaaldag Model Y (PWA)

Installeerbare webapp voor de opleveringscontrole van je Tesla Model Y.

## Inhoud

| Bestand | Wat |
|---|---|
| index.html | De app zelf |
| manifest.webmanifest | Naam, icoon en kleuren voor installatie |
| sw.js | Zorgt dat de app offline werkt |
| icons/ | App iconen (Android, iPhone) |

## Online zetten

Upload de **inhoud** van deze map (niet de map zelf, index.html moet in de root staan). Er is HTTPS nodig, maar alle gratis hosts hieronder doen dat automatisch.

* **Netlify Drop:** ga naar app.netlify.com/drop en sleep de map erin.
* **GitHub Pages:** nieuwe repository, bestanden uploaden, Settings > Pages > branch main.
* **Cloudflare Pages / Vercel:** nieuw project, map uploaden, geen build stap nodig.
* **Eigen webhosting:** bestanden via FTP in een submap zetten, bv. /ophaaldag/. Dat werkt ook.

## Installeren op je gsm

* **iPhone:** open de link in **Safari**, tik op Delen en kies **Zet op beginscherm**.
* **Android:** open de link in Chrome en tik op **Installeren** in de app (of menu > App installeren).

Open de app daarna altijd via het icoon. Op iPhone heeft de geïnstalleerde app zijn eigen opslag, los van Safari.

## Goed om te weten

* Alles (vinkjes, notities, foto's) blijft enkel op je gsm. Er gaat niets naar een server.
* Exporteer het rapport voor je vertrekt bij Tesla: delen via WhatsApp of mail, of downloaden.
* Pas je later iets aan in de app, verhoog dan `VERSION` in sw.js (bv. ophaaldag-v2), anders blijft de oude versie in de cache hangen.
* Test thuis één keer: foto maken, rapport exporteren, daarna "Alles wissen".
