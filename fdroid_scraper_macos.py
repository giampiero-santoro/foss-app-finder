import requests
import json

def scrape_f_droid():
    # URL del database moderno di F-Droid (V2)
    INDEX_URL = "https://f-droid.org/repo/index-v2.json"
    # URL base per le immagini
    REPO_BASE = "https://f-droid.org/repo/"
    
    print("Scaricamento dati da F-Droid in corso...")
    try:
        response = requests.get(INDEX_URL)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Errore durante il download: {e}")
        return

    apps_list = []
    # Nel formato V2, le app sono sotto la chiave 'packages'
    packages = data.get('packages', {})

    for pkg_name, pkg_info in packages.items():
        metadata = pkg_info.get('metadata', {})
        
        # Estrazione Nome (cerchiamo IT, poi EN, poi l'ID pacchetto)
        nome = metadata.get('name', {}).get('it') or \
               metadata.get('name', {}).get('en-US') or pkg_name
        
        # Estrazione Riassunto
        riassunto = metadata.get('summary', {}).get('it') or \
                    metadata.get('summary', {}).get('en-US') or "Nessuna descrizione disponibile."
        
        # COSTRUZIONE URL ICONA
        icon_data = metadata.get('icon', {})
        icona_url = "https://via.placeholder.com/64" # Default se non c'è icona
        
        if icon_data:
            # Prendiamo la prima lingua disponibile nell'oggetto icona
            try:
                first_lang_icon = list(icon_data.values())[0]
                icon_file = first_lang_icon.get('name')
                if icon_file:
                    icona_url = f"{REPO_BASE}{icon_file}"
            except:
                pass

        # Creazione del dizionario con i nomi che il tuo index.html si aspetta
        app_entry = {
            "nome": nome,
            "id_pacchetto": pkg_name,
            "riassunto": riassunto,
            "licenza": metadata.get('license', 'FOSS'),
            "icona": icona_url,
            "url_codice_sorgente": metadata.get('sourceCode'),
            "ultimo_aggiornamento": pkg_info.get('lastUpdated')
        }
        
        # Aggiungiamo l'app solo se ha un link al codice sorgente (filtro FOSS)
        if app_entry["url_codice_sorgente"]:
            apps_list.append(app_entry)

    # Scrittura del file apps.json
    with open('apps.json', 'w', encoding='utf-8') as f:
        json.dump(apps_list, f, ensure_ascii=False, indent=4)
    
    print(f"Fatto! Salvate {len(apps_list)} app in apps.json")

if __name__ == "__main__":
    scrape_f_droid()
