import requests
import json

def scrape_f_droid():
    INDEX_URL = "https://f-droid.org/repo/index-v2.json"
    # Cartella specifica dove F-Droid salva le icone a 64px
    ICON_BASE = "https://f-droid.org/repo/icons-64/"
    
    print("Scaricamento dati...")
    try:
        response = requests.get(INDEX_URL)
        data = response.json()
    except Exception as e:
        print(f"Errore: {e}")
        return

    apps_list = []
    packages = data.get('packages', {})

    for pkg_name, pkg_info in packages.items():
        metadata = pkg_info.get('metadata', {})
        
        # Gestione Icona: estrae il nome file dall'oggetto icona
        icon_data = metadata.get('icon', {})
        icon_file = None
        if icon_data:
            # Prende il primo file disponibile tra le lingue
            icon_file = list(icon_data.values())[0].get('name')

        app_entry = {
            "nome": metadata.get('name', {}).get('it') or metadata.get('name', {}).get('en-US') or pkg_name,
            "id_pacchetto": pkg_name,
            "riassunto": metadata.get('summary', {}).get('it') or metadata.get('summary', {}).get('en-US') or "",
            "licenza": metadata.get('license', 'FOSS'),
            "icona": f"{ICON_BASE}{icon_file}" if icon_file else "https://via.placeholder.com/64",
            "url_codice_sorgente": metadata.get('sourceCode'),
        }
        
        if app_entry["url_codice_sorgente"]:
            apps_list.append(app_entry)

    with open('apps.json', 'w', encoding='utf-8') as f:
        json.dump(apps_list, f, ensure_ascii=False, indent=4)
    print(f"Completato: {len(apps_list)} app.")

if __name__ == "__main__":
    scrape_f_droid()
