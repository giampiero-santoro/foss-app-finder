#!/usr/bin/env python3
"""
Script per scaricare e processare i metadati delle app di F-Droid.
Versione con gestione certificati SSL per macOS
"""

import json
import sys
import ssl
import certifi
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from typing import Dict, List, Optional

# URL del file di metadati ufficiale di F-Droid
FDROID_INDEX_URL = "https://f-droid.org/repo/index-v2.json"

# Nome del file di output
OUTPUT_FILE = "apps.json"


def crea_ssl_context():
    """
    Crea un contesto SSL che funziona su macOS.
    Prova diverse strategie per gestire i certificati.
    
    Returns:
        Contesto SSL configurato, oppure None per disabilitare la verifica
    """
    try:
        # Strategia 1: Usa certifi (libreria dedicata ai certificati)
        import certifi
        context = ssl.create_default_context(cafile=certifi.where())
        print("✅ Usando certificati da certifi")
        return context
    except ImportError:
        pass
    
    try:
        # Strategia 2: Usa il contesto SSL di default
        context = ssl.create_default_context()
        print("✅ Usando contesto SSL di default")
        return context
    except Exception:
        pass
    
    # Strategia 3: Disabilita la verifica SSL (NON RACCOMANDATO ma funziona)
    print("⚠️  Attenzione: Verifica SSL disabilitata per motivi di compatibilità")
    return ssl._create_unverified_context()


def scarica_metadati(url: str, timeout: int = 30) -> Optional[Dict]:
    """
    Scarica i metadati di F-Droid dall'URL specificato.
    Gestisce problemi di certificati SSL su macOS.
    
    Args:
        url: URL del file index-v2.json di F-Droid
        timeout: Timeout in secondi per la richiesta HTTP
    
    Returns:
        Dizionario contenente i metadati JSON, oppure None in caso di errore
    """
    print(f"📥 Scaricamento metadati da: {url}")
    
    # Crea il contesto SSL appropriato
    ssl_context = crea_ssl_context()
    
    try:
        # Crea una richiesta con User-Agent per evitare blocchi
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        request = Request(url, headers=headers)
        
        # Esegue la richiesta HTTP con il contesto SSL
        with urlopen(request, timeout=timeout, context=ssl_context) as response:
            # Legge e decodifica il contenuto JSON
            print("⏳ Download in corso (il file è grande, circa 50-100 MB)...")
            data = json.loads(response.read().decode('utf-8'))
            print(f"✅ Download completato con successo!")
            return data
            
    except HTTPError as e:
        print(f"❌ Errore HTTP {e.code}: {e.reason}", file=sys.stderr)
        print(f"   Il server ha restituito un errore. Riprova più tardi.", file=sys.stderr)
        return None
        
    except URLError as e:
        print(f"❌ Errore di connessione: {e.reason}", file=sys.stderr)
        
        # Messaggio specifico per errori SSL su macOS
        if "CERTIFICATE_VERIFY_FAILED" in str(e.reason):
            print("\n" + "="*60, file=sys.stderr)
            print("🔧 SOLUZIONE PER macOS:", file=sys.stderr)
            print("="*60, file=sys.stderr)
            print("\nPer risolvere il problema dei certificati SSL, esegui UNO di questi comandi:\n", file=sys.stderr)
            print("1️⃣  Installa certifi:", file=sys.stderr)
            print("   pip3 install certifi", file=sys.stderr)
            print("\n2️⃣  Esegui il comando di installazione certificati Python:", file=sys.stderr)
            print("   /Applications/Python\\ 3.*/Install\\ Certificates.command", file=sys.stderr)
            print("\n3️⃣  Oppure installa certificati manualmente:", file=sys.stderr)
            print("   pip3 install --upgrade certifi", file=sys.stderr)
            print("="*60 + "\n", file=sys.stderr)
        
        return None
        
    except json.JSONDecodeError as e:
        print(f"❌ Errore nel parsing JSON: {e}", file=sys.stderr)
        print(f"   Il file scaricato potrebbe essere corrotto.", file=sys.stderr)
        return None
        
    except Exception as e:
        print(f"❌ Errore inaspettato: {type(e).__name__}: {e}", file=sys.stderr)
        return None


def estrai_informazioni_essenziali(metadati: Dict) -> List[Dict]:
    """
    Estrae solo le informazioni essenziali da ogni app per risparmiare memoria.
    
    Args:
        metadati: Dizionario completo dei metadati di F-Droid
    
    Returns:
        Lista di dizionari contenenti solo le informazioni essenziali per ogni app
    """
    print(f"🔍 Estrazione informazioni essenziali...")
    
    apps_filtrate = []
    
    # Il formato index-v2.json ha una struttura con "packages" come chiave principale
    packages = metadati.get('packages', {})
    
    if not packages:
        print(f"⚠️  Nessun pacchetto trovato nei metadati", file=sys.stderr)
        return []
    
    total_packages = len(packages)
    print(f"📦 Trovati {total_packages} pacchetti totali")
    
    # Itera attraverso ogni pacchetto
    processed = 0
    for package_id, package_data in packages.items():
        processed += 1
        
        # Mostra progresso ogni 500 app
        if processed % 500 == 0:
            print(f"⏳ Processate {processed}/{total_packages} app...")
        
        try:
            # Estrae i metadati di base
            metadata = package_data.get('metadata', {})
            
            # Estrae l'URL del codice sorgente
            source_code_url = metadata.get('sourceCode', '')
            
            # Filtra le app senza URL del codice sorgente valido
            if not source_code_url or source_code_url.strip() == '':
                continue
            
            # Estrae la data dell'ultimo aggiornamento dalle versioni disponibili
            versions = package_data.get('versions', {})
            ultimo_aggiornamento = None
            
            if versions:
                # Prende la prima versione (la più recente) e la sua data
                first_version = next(iter(versions.values()), {})
                manifest = first_version.get('manifest', {})
                ultimo_aggiornamento = manifest.get('versionCode')
                
                # Cerca un timestamp più leggibile se disponibile
                added_timestamp = first_version.get('added')
                if added_timestamp:
                    ultimo_aggiornamento = added_timestamp
            
            # Estrae l'URL dell'icona
            icon = metadata.get('icon')
            icon_url = None
            if icon:
                # L'icona è relativa, costruisce l'URL completo
                icon_url = f"https://f-droid.org/repo/{icon.get('name', '')}"
            
            # Crea il dizionario con le informazioni essenziali
            app_info = {
                'nome': metadata.get('name', {}).get('en-US', package_id),
                'id_pacchetto': package_id,
                'riassunto': metadata.get('summary', {}).get('en-US', ''),
                'licenza': metadata.get('license', 'Sconosciuta'),
                'icona': icon_url,
                'url_codice_sorgente': source_code_url,
                'ultimo_aggiornamento': ultimo_aggiornamento
            }
            
            apps_filtrate.append(app_info)
            
        except Exception as e:
            # In caso di errore con una singola app, continua con le altre
            print(f"⚠️  Errore nell'elaborazione del pacchetto {package_id}: {e}", 
                  file=sys.stderr)
            continue
    
    print(f"✅ Estratte {len(apps_filtrate)} app con URL del codice sorgente valido")
    return apps_filtrate


def salva_risultati(apps: List[Dict], nome_file: str) -> bool:
    """
    Salva i risultati in un file JSON in formato compatto.
    
    Args:
        apps: Lista delle app da salvare
        nome_file: Nome del file di output
    
    Returns:
        True se il salvataggio è riuscito, False altrimenti
    """
    print(f"💾 Salvataggio risultati in '{nome_file}'...")
    
    try:
        with open(nome_file, 'w', encoding='utf-8') as f:
            # Salva in formato compatto (senza indentazione) per risparmiare spazio
            # ensure_ascii=False mantiene i caratteri Unicode originali
            json.dump(apps, f, ensure_ascii=False, separators=(',', ':'))
        
        print(f"✅ File salvato con successo!")
        
        # Calcola e mostra statistiche
        import os
        file_size = os.path.getsize(nome_file)
        print(f"📊 Dimensione file: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
        
        return True
        
    except IOError as e:
        print(f"❌ Errore nella scrittura del file: {e}", file=sys.stderr)
        return False
        
    except Exception as e:
        print(f"❌ Errore inaspettato durante il salvataggio: {e}", file=sys.stderr)
        return False


def esegui_scraping():
    """
    Funzione principale che orchestra l'intero processo.
    
    Returns:
        Tuple (success: bool, num_apps: int)
    """
    print("=" * 60)
    print("🤖 F-Droid Metadata Scraper (macOS Edition)")
    print("=" * 60)
    print()
    
    # Passo 1: Scarica i metadati
    metadati = scarica_metadati(FDROID_INDEX_URL)
    
    if metadati is None:
        print("\n❌ Impossibile scaricare i metadati. Operazione terminata.")
        return False, 0
    
    print()
    
    # Passo 2 e 3: Estrai informazioni essenziali e filtra le app
    apps_filtrate = estrai_informazioni_essenziali(metadati)
    
    if not apps_filtrate:
        print("\n❌ Nessuna app trovata con i criteri specificati.")
        return False, 0
    
    print()
    
    # Passo 4: Salva i risultati
    successo = salva_risultati(apps_filtrate, OUTPUT_FILE)
    
    if not successo:
        print("\n❌ Impossibile salvare i risultati. Operazione terminata.")
        return False, len(apps_filtrate)
    
    print()
    print("=" * 60)
    print(f"✨ Operazione completata con successo!")
    print(f"📁 File generato: {OUTPUT_FILE}")
    print(f"📱 Numero totale di app: {len(apps_filtrate)}")
    print("=" * 60)
    
    return True, len(apps_filtrate)


def main():
    """
    Funzione main per esecuzione come script.
    """
    success, num_apps = esegui_scraping()
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
