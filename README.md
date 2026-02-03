# 📱 FOSS App Finder
> Un catalogo moderno e veloce per scoprire le migliori applicazioni Open Source per Android.

FOSS App Finder estrae i dati direttamente dai repository ufficiali di **F-Droid** per offrire un'interfaccia pulita, categorizzata e facile da consultare per chiunque voglia proteggere la propria privacy usando software libero.

## 🔗 Link al Progetto
👉 **[Visualizza il sito live](https://giampiero-santoro.github.io/foss-app-finder/)**

## ✨ Funzionalità principali
- **🔍 Ricerca Istantanea:** Trova app per nome o descrizione in pochi millisecondi.
- **🏷️ Filtri per Categoria:** Naviga tra Internet, Giochi, Multimedia e Sicurezza.
- **🛡️ Schede Tecniche:** Spiegazioni chiare sul perché il software FOSS è sicuro.
- **⚙️ Guide all'installazione:** Istruzioni passo-passo per gli utenti meno esperti.
- **🚀 Aggiornamento Automatico:** Database sincronizzato quotidianamente con F-Droid tramite GitHub Actions.

## 🛠️ Architettura Tecnica
- **Backend (Scraper):** Python (libreria `requests`) per la cattura e pulizia dei dati.
- **Database:** File JSON statico (`apps.json`) per massimizzare la velocità di caricamento.
- **Frontend:** HTML5, JavaScript moderno e **Tailwind CSS** per un design responsive.
- **Storage:** Dati passati tramite `localStorage` per una navigazione istantanea tra le pagine.

## 📂 Struttura del Repository
- `index.html`: La home page con la griglia delle app e i filtri.
- `dettagli.html`: La pagina di approfondimento della singola applicazione.
- `fdroid_scraper_macos.py`: Lo script Python che aggiorna il catalogo.
- `apps.json`: Il database generato dallo script.

---
Progetto creato per promuovere l'etica del software libero e la trasparenza digitale.
