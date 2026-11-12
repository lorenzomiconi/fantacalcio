import json
import os
import urllib.request
import urllib.error

FILE_DATI = "data.json"
URL_FANTAPAZZ_STATISTICHE = "https://www.fantapazz.com/fantacalcio/statistiche"

def aggiorna_fantamedia_automatico():
    # 1. Controlla se esiste il file delle rose
    if not os.path.exists(FILE_DATI):
        print(f"❌ Errore: Il file {FILE_DATI} non esiste nella cartella.")
        return

    print("🌐 Connessione a Fantapazz per il download dei voti in corso...")
    
    # Intestazioni per simulare un browser ed evitare blocchi
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    nuovi_voti = {}

    try:
        req = urllib.request.Request(URL_FANTAPAZZ_STATISTICHE, headers=headers)
        with urllib.request.urlopen(req) as response:
            html_content = response.read().decode('utf-8')
            
        # Analizziamo la pagina HTML per estrarre i dati delle tabelle
        # Usiamo BeautifulSoup se disponibile, oppure un parsing leggero con pandas / html standard
        import pandas as pd
        from io import StringIO
        
        tables = pd.read_html(StringIO(html_content))
        if not tables:
            print("❌ Errore: Nessuna tabella trovata sulla pagina.")
            return

        df_voti = None
        for table in tables:
            # Cerchiamo la tabella che contiene le colonne dei voti (Calciatore, MV, FM)
            cols = [str(c).upper() for c in table.columns]
            if any("CALCIATORE" in c or "NOME" in c for c in cols) and any("MV" in c for c in cols):
                df_voti = table
                break
        
        if df_voti is None:
            df_voti = tables[0] # Prende la prima tabella come fallback

        print(f"📊 Elaborazione dei dati estratti...")
        
        # Identifica le colonne corrette
        col_nome = None
        col_mv = None
        col_fm = None
        
        for col in df_voti.columns:
            c_upper = str(col).upper()
            if "CALCIATORE" in c_upper or "NOME" in c_upper or "GIOCATORE" in c_upper:
                col_nome = col
            elif c_upper == "MV" or "MEDIA VOTO" in c_upper:
                col_mv = col
            elif c_upper == "FM" or "FANTAMEDIA" in c_upper:
                col_fm = col

        if not col_nome or not col_mv or not col_fm:
            # Se le intestazioni sono nella prima riga
            df_voti.columns = df_voti.iloc[0]
            df_voti = df_voti.drop(0)
            for col in df_voti.columns:
                c_upper = str(col).upper()
                if "CALCIATORE" in c_upper or "NOME" in c_upper:
                    col_nome = col
                elif c_upper == "MV":
                    col_mv = col
                elif c_upper == "FM":
                    col_fm = col

        if not col_nome or not col_mv or not col_fm:
            print("❌ Errore: Impossibile mappare automaticamente le colonne delle statistiche.")
            return

        for _, row in df_voti.iterrows():
            nome = row[col_nome]
            mv = row[col_mv]
            fm = row[col_fm]
            
            if pd.notna(nome) and pd.notna(mv) and pd.notna(fm):
                try:
                    clean_name = str(nome).strip().upper()
                    clean_mv = float(str(mv).replace(",", "."))
                    clean_fm = float(str(fm).replace(",", "."))
                    nuovi_voti[clean_name] = {"mv": clean_mv, "fm": clean_fm}
                except ValueError:
                    continue

    except Exception as e:
        print(f"❌ Errore durante il recupero dei dati da internet: {e}")
        return

    # 2. Carica il file data.json con tutte le squadre della lega
    with open(FILE_DATI, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 3. Aggiorna i voti di tutti i giocatori in tutte le rose
    aggiornati_totali = 0
    for squadra_nome, reparti in data.items():
        for ruolo, giocatori in reparti.items():
            for p in giocatori:
                nome_giocatore = p["name"].upper().strip()
                if nome_giocatore in nuovi_voti:
                    p["mv"] = nuovi_voti[nome_giocatore]["mv"]
                    p["fm"] = nuovi_voti[nome_giocatore]["fm"]
                    aggiornati_totali += 1

    # 4. Salva il file data.json aggiornato
    with open(FILE_DATI, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"✅ Aggiornamento automatico completato con successo!")
    print(f"⚽ Totale giocatori aggiornati in tutte le rose della lega: {aggiornati_totali}")

if __name__ == "__main__":
    aggiorna_fantamedia_automatico()
