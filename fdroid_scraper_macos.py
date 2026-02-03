import requests
import json

def scrape_f_droid():
    # URL del database moderno
    INDEX_URL = "https://f-droid.org/repo/index-v2.json"
    # Cartella dove F-Droid tiene le icone a 64px
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
        
        # LOGICA ICONA: estraiamo il nome del file dall'oggetto complesso di F-Droid
        icon_data = metadata.get('icon', {})
        icona_url = "https://via.placeholder.com/64" # Default se manca
        
        if icon_data:
            try:
                # F-Droid v2 ha le icone divise per lingua. Prendiamo la prima disponibile.
                prime_lingue = list(icon_data.values())
                if prime_lingue:
                    icon_file = prime_lingue[0].get('name')
                    if icon_file:
                        icona_url = f"{ICON_BASE}{icon_file}"
            except Exception:
                pass

        app_entry = {
            "nome": nome,
            "id_pacchetto": pkg_name,
            "riassunto": riassunto,
            "licenza": metadata.get('license', 'FOSS'),
            "icona": icona_url,
            "categorie": metadata.get('categories', ['Generic']), # <--- Aggiungiamo questa riga
            "url_codice_sorgente": metadata.get('sourceCode'),
            "ultimo_aggiornamento": pkg_info.get('lastUpdated')
        }
        
        if app_entry["url_codice_sorgente"]:
            apps_list.append(app_entry)

    with open('apps.json', 'w', encoding='utf-8') as f:
        json.dump(apps_list, f, ensure_ascii=False, indent=4)
    print(f"Fatto! Generate {len(apps_list)} app.")

if __name__ == "__main__":
    scrape_f_droid()
