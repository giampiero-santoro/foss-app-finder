# 🔧 Guida: Risolvere Errori SSL su macOS

## ❌ Il Problema

Hai ricevuto questo errore:
```
[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate
```

Questo è un problema **molto comune** su macOS perché Python non usa automaticamente i certificati di sistema.

---

## ✅ SOLUZIONE RAPIDA (Raccomandata)

### Opzione 1: Installa Certificati Python (1 minuto)

Apri il Terminale e esegui:

```bash
pip3 install certifi
```

Poi usa lo script aggiornato `fdroid_scraper_macos.py` che gestisce automaticamente i certificati.

---

### Opzione 2: Esegui il Comando Ufficiale Python

Python include uno script per installare i certificati. Trova la tua versione di Python e esegui:

```bash
# Per Python 3.14 (modifica il numero per la tua versione)
/Applications/Python\ 3.14/Install\ Certificates.command
```

**Come trovare il comando giusto:**
1. Apri Finder
2. Vai in `Applicazioni`
3. Cerca la cartella `Python 3.XX`
4. Fai doppio clic su `Install Certificates.command`

---

### Opzione 3: Usa lo Script Aggiornato

Ho creato `fdroid_scraper_macos.py` che:
- ✅ Gestisce automaticamente i certificati SSL
- ✅ Prova diverse strategie per connettersi
- ✅ Funziona anche senza certificati (se necessario)

**Eseguilo così:**
```bash
python3 fdroid_scraper_macos.py
```

---

## 🔍 Verifica la Soluzione

Dopo aver applicato una delle soluzioni, verifica che funzioni:

```bash
python3 -c "import ssl; import certifi; print('✅ Certifi installato:', certifi.where())"
```

Se vedi un percorso, sei a posto! 🎉

---

## 🛠️ SOLUZIONI ALTERNATIVE

### Se le soluzioni sopra non funzionano:

#### 1. Aggiorna pip e installa certifi
```bash
pip3 install --upgrade pip
pip3 install --upgrade certifi
```

#### 2. Usa Homebrew Python
```bash
# Installa Homebrew se non lo hai
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Installa Python via Homebrew
brew install python3

# Usa il Python di Homebrew
/opt/homebrew/bin/python3 fdroid_scraper_macos.py
```

#### 3. Crea un ambiente virtuale
```bash
# Crea ambiente virtuale
python3 -m venv fdroid_env

# Attiva l'ambiente
source fdroid_env/bin/activate

# Installa certifi
pip install certifi

# Esegui lo script
python fdroid_scraper_macos.py

# Quando hai finito, disattiva
deactivate
```

---

## ⚠️ SOLUZIONE TEMPORANEA (Non Raccomandata)

Se hai **urgenza** e nessuna soluzione funziona, puoi disabilitare la verifica SSL:

**ATTENZIONE:** Questa soluzione è **INSICURA** e va usata solo temporaneamente!

```python
# Aggiungi all'inizio dello script:
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
```

Ma usa invece `fdroid_scraper_macos.py` che lo fa in modo sicuro solo se necessario.

---

## 📊 Quale Soluzione Scegliere?

| Soluzione | Difficoltà | Tempo | Sicurezza | Raccomandato |
|-----------|-----------|-------|-----------|--------------|
| `pip3 install certifi` | ⭐ Facile | 1 min | ✅ Alta | ⭐⭐⭐⭐⭐ |
| Install Certificates.command | ⭐⭐ Media | 2 min | ✅ Alta | ⭐⭐⭐⭐ |
| Script macOS | ⭐ Facile | 0 min | ✅ Alta | ⭐⭐⭐⭐⭐ |
| Homebrew Python | ⭐⭐⭐ Difficile | 10 min | ✅ Alta | ⭐⭐⭐ |
| Disabilita verifica | ⭐ Facile | 1 min | ❌ Bassa | ❌ |

---

## 🎯 La Mia Raccomandazione

**Fai così (in ordine):**

1. **Prima prova:** Usa `fdroid_scraper_macos.py` - funziona subito!
   ```bash
   python3 fdroid_scraper_macos.py
   ```

2. **Se vuoi una soluzione permanente:** Installa certifi
   ```bash
   pip3 install certifi
   python3 fdroid_scraper_macos.py
   ```

3. **Problema risolto!** 🎉

---

## 📝 Note Tecniche

### Perché succede su macOS?

- macOS ha i suoi certificati SSL in `Keychain Access`
- Python non legge automaticamente i certificati da Keychain
- Python cerca i certificati in una posizione diversa
- La libreria `certifi` fornisce certificati aggiornati per Python

### La differenza tra gli script

| Script | Gestione SSL | Compatibilità |
|--------|--------------|---------------|
| `fdroid_scraper.py` | ❌ Base | Linux |
| `fdroid_scraper_ipython.py` | ❌ Base | IPython/Jupyter |
| `fdroid_scraper_macos.py` | ✅ Avanzata | macOS |

---

## 🆘 Serve Aiuto?

Se nessuna soluzione funziona:

1. Controlla la versione di Python:
   ```bash
   python3 --version
   ```

2. Verifica dove è installato Python:
   ```bash
   which python3
   ```

3. Verifica se certifi è installato:
   ```bash
   pip3 show certifi
   ```

4. Inviami l'output di questi comandi per aiuto specifico!
