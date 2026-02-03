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

    print(f"Elaborazione di {len(packages)} pacchetti...")

    for pkg_name, pkg_info in packages.items():
        metadata = pkg_info.get('metadata', {})
        
        # Estrazione Nome (IT, poi EN, poi ID pacchetto)
        nome = metadata.get('name', {}).get('it') or \
               metadata.get('name', {}).get('en-US') or pkg_name
        
        # Estrazione Riassunto
        riassunto = metadata.get('summary', {}).get('it') or \
                    metadata.get('summary', {}).get('en-US') or "Nessuna descrizione disponibile."
        
        # --- ESTRAZIONE CATEGORIE (La parte che mancava!) ---
        categorie = metadata.get('categories', [])
        
        # COSTRUZIONE URL ICONA
        icon_data = metadata.get('icon', {})
        icona_url = "https://via.placeholder.com/64" 
        
        if icon_data:
            try:
                # Prendiamo la prima lingua disponibile nell'oggetto icona
                first_lang_icon = list(icon_data.values())[0]
                icon_file = first_lang_icon.get('name')
                if icon_file:
                    icona_url = f"{REPO_BASE}{icon_file}"
            except:
                pass

        # Creazione del dizionario completo
        app_entry = {
            "nome": nome,
            "id_pacchetto": pkg_name,
            "riassunto": riassunto,
            "categorie": categorie, # Ora le categorie vengono salvate!
            "licenza": metadata.get('license', 'FOSS'),
            "icona": icona_url,
            "url_codice_sorgente": metadata.get('sourceCode'),
            "ultimo_aggiornamento": pkg_info.get('lastUpdated')
        }
        
        # Filtro: aggiungiamo solo se ha il codice sorgente (etica FOSS)
        if app_entry["url_codice_sorgente"]:
            apps_list.append(app_entry)

    print(f"Salvataggio di {len(apps_list)} app in apps.json...")
    
    # Scrittura del file apps.json
    with open('apps.json', 'w', encoding='utf-8') as f:
        json.dump(apps_list, f, ensure_ascii=False, indent=4)
    
    print("Operazione completata con successo!")

if __name__ == "__main__":
    scrape_f_droid()
