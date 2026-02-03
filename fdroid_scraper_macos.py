import requests
import json

def scrape_f_droid():
    # URL del database moderno di F-Droid (V2)
    INDEX_URL = "https://f-droid.org/repo/index-v2.json"
    # URL base per le immagini (cartella standard icone 64px)
    ICON_BASE = "https://f-droid.org/repo/icons-64/"
    
    print("Scaricamento dati da F-Droid in corso...")
    try:
        response = requests.get(INDEX_URL)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Errore durante il download: {e}")
        return

    apps_list = []
    packages = data.get('packages', {})

    for pkg_name, pkg_info in packages.items():
        metadata = pkg_info.get('metadata', {})
        
        # Estrazione Nome (IT -> EN -> ID)
        nome = metadata.get('name', {}).get('it') or \
               metadata.get('name', {}).get('en-US') or pkg_name
        
        # Estrazione Riassunto (IT -> EN)
        riassunto = metadata.get('summary', {}).get('it') or \
                    metadata.get('summary', {}).get('en-US') or "Nessuna descrizione disponibile."
        
        # COSTRUZIONE URL ICONA COMPLETO
        icon_data = metadata.get('icon', {})
        icona_url = "https://via.placeholder.com/64"
        
        if icon_data:
            try:
                # Prende il nome del file dell'icona da qualsiasi lingua disponibile
                icon_file = list(icon_data.values())[0].get('name')
                if icon_file:
                    icona_url = f"{ICON_BASE}{icon_file}"
            except:
                pass

        app_entry = {
            "nome": nome,
            "id_pacchetto": pkg_name,
            "riassunto": riassunto,
            "licenza": metadata.get('license', 'FOSS'),
            "icona": icona_url,
            "url_codice_sorgente": metadata.get('sourceCode'),
            "ultimo_aggiornamento": pkg_info.get('lastUpdated')
        }
        
        # Filtro: aggiungi solo se c'è il codice sorgente
        if app_entry["url_codice_sorgente"]:
            apps_list.append(app_entry)

    with open('apps.json', 'w', encoding='utf-8') as f:
        json.dump(apps_list, f, ensure_ascii=False, indent=4)
    
    print(f"Fatto! Generate {len(apps_list)} app con icone aggiornate.")

if __name__ == "__main__":
    scrape_f_droid()
