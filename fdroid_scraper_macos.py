import requests
import json
import os

def scrape_f_droid():
    INDEX_URL = "https://f-droid.org/repo/index-v2.json"
    ICON_BASE = "https://f-droid.org/repo/icons-64/"
    
    print("Inizio scraping...")
    try:
        response = requests.get(INDEX_URL, timeout=30)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"ERRORE CRITICO nel download: {e}")
        exit(1) # Forza l'errore visibile in Actions

    apps_list = []
    packages = data.get('packages', {})

    for pkg_name, pkg_info in packages.items():
        try:
            metadata = pkg_info.get('metadata', {})
            
            icon_data = metadata.get('icon', {})
            icon_file = None
            if icon_data:
                # Prende il primo file disponibile tra le lingue
                lang_icons = list(icon_data.values())
                if lang_icons:
                    icon_file = lang_icons[0].get('name')

            app_entry = {
                "nome": metadata.get('name', {}).get('it') or metadata.get('name', {}).get('en-US') or pkg_name,
                "id_pacchetto": pkg_name,
                "riassunto": metadata.get('summary', {}).get('it') or metadata.get('summary', {}).get('en-US') or "",
                "licenza": metadata.get('license', 'FOSS'),
                "icona": f"{ICON_BASE}{icon_file}" if icon_file else "https://via.placeholder.com/64",
                "categorie": metadata.get('categories', ['Altro']),
                "url_codice_sorgente": metadata.get('sourceCode'),
                "ultimo_aggiornamento": pkg_info.get('lastUpdated'),
                "sistemi": ["Android"]
            }
            
            if app_entry["url_codice_sorgente"]:
                apps_list.append(app_entry)
        except Exception as e:
            print(f"Salto pacchetto {pkg_name} per errore: {e}")
            continue

    with open('apps.json', 'w', encoding='utf-8') as f:
        json.dump(apps_list, f, ensure_ascii=False, indent=4)
    
    print(f"Successo! Generate {len(apps_list)} app.")

if __name__ == "__main__":
    scrape_f_droid()
