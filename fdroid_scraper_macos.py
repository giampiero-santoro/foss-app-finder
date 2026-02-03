import requests
import json

def scrape_f_droid():
    INDEX_URL = "https://f-droid.org/repo/index-v2.json"
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
        
        # Gestione Icona
        icon_data = metadata.get('icon', {})
        icona_url = "https://via.placeholder.com/64"
        if icon_data:
            try:
                icon_file = list(icon_data.values())[0].get('name')
                if icon_file: icona_url = f"{ICON_BASE}{icon_file}"
            except: pass
                
        app_entry = {
            "nome": nome,
            "id_pacchetto": pkg_name,
            "riassunto": riassunto,
            "licenza": metadata.get('license', 'FOSS'),
            "icona": icona_url,
            "categorie": metadata.get('categories', ['Altro']),
            "url_codice_sorgente": metadata.get('sourceCode'),
            "ultimo_aggiornamento": pkg_info.get('lastUpdated'),
            # Aggiungiamo i sistemi operativi (default Android per F-Droid)
            "sistemi": ["Android"], 
            "url_fdroid": f"https://f-droid.org/packages/{pkg_name}/"
        }
        
        if app_entry["url_codice_sorgente"]:
            apps_list.append(app_entry)

    with open('apps.json', 'w', encoding='utf-8') as f:
        json.dump(apps_list, f, ensure_ascii=False, indent=4)
    print(f"Completato: {len(apps_list)} app.")

if __name__ == "__main__":
    scrape_f_droid()
