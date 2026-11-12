import csv
import json
import os

FILE_DATI = "data.json"
# Cerca sia il file CSV che l'Excel scaricato da Fantapazz
FILE_CSV_VOTI = "statistiche_fantapazz.csv"
FILE_EXCEL_VOTI = "statistiche_fantapazz.xlsx"

def pulisci_nome(nome):
    """Pulisce il nome del giocatore per un matching perfetto"""
    if not nome:
        return ""
    return str(nome).strip().upper()

def aggiorna_fantamedia_da_file():
    # 1. Controlla se esiste il file delle rose (data.json)
    if not os.path.exists(FILE_DATI):
        print(f"❌ Errore: Il file {FILE_DATI} non esiste nella cartella.")
        return

    # Trova quale file dei voti è presente nella cartella (CSV o Excel)
    file_voti_trovato = None
    if os.path.exists(FILE_CSV_VOTI):
        file_voti_trovato = FILE_CSV_VOTI
    elif os.path.exists(FILE_EXCEL_VOTI):
        file_voti_trovato = FILE_EXCEL_VOTI
    else:
        print(f"⚠️ Attenzione: Non è stato trovato alcun file dei voti ('{FILE_CSV_VOTI}' o '{FILE_EXCEL_VOTI}').")
        print(f"👉 Scarica il file delle statistiche da Fantapazz e mettilo nella cartella.")
        return

    # Carica le rose attuali di tutte le squadre della lega
    with open(FILE_DATI, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"📊 Lettura dei voti da '{file_voti_trovato}' in corso...")
    
    nuovi_voti = {}

    try:
        # Se è un file Excel (.xlsx), usiamo pandas
        if file_voti_trovato.endswith(".xlsx"):
            import pandas as pd
            df = pd.read_excel(file_voti_trovato)
            
            # Cerca le colonne corrispondenti nel DataFrame
            col_nome = next((c for c in df.columns if c in ["Calciatore", "Nome", "Giocatore"]), None)
            col_mv = next((c for c in df.columns if c in ["MV", "Media Voto"]), None)
            col_fm = next((c for c in df.columns if c in ["FM", "Fantamedia"]), None)
            
            if not col_nome or not col_mv or not col_fm:
                print(f"❌ Errore: Impossibile trovare le colonne necessarie nel file Excel (Calciatore, MV, FM).")
                return
                
            for _, row in df.iterrows():
                nome = row[col_nome]
                mv = row[col_mv]
                fm = row[col_fm]
                if pd.notna(nome) and pd.notna(mv) and pd.notna(fm):
                    try:
                        clean_mv = float(str(mv).replace(",", "."))
                        clean_fm = float(str(fm).replace(",", "."))
                        nuovi_voti[pulisci_nome(nome)] = {"mv": clean_mv, "fm": clean_fm}
                    except ValueError:
                        continue
                        
        # Altrimenti leggiamo il file CSV
        else:
            with open(file_voti_trovato, mode="r", encoding="utf-8-sig") as csv_file:
                sample = csv_file.read(2048)
                csv_file.seek(0)
                dialect = csv.Sniffer().sniff(sample)
                
                reader = csv.DictReader(csv_file, dialect=dialect)
                
                for row in reader:
                    nome = row.get("Calciatore") or row.get("Nome") or row.get("Giocatore")
                    mv = row.get("MV") or row.get("Media Voto")
                    fm = row.get("FM") or row.get("Fantamedia")
                    
                    if nome and mv and fm:
                        try:
                            clean_mv = float(mv.replace(",", "."))
                            clean_fm = float(fm.replace(",", "."))
                            nuovi_voti[pulisci_nome(nome)] = {"mv": clean_mv, "fm": clean_fm}
                        except ValueError:
                            continue
                            
    except Exception as e:
        print(f"❌ Errore durante la lettura del file dei voti: {e}")
        return

    # 3. Aggiorna automaticamente tutte le squadre e i giocatori nel file data.json
    aggiornati_totali = 0
    
    for squadra_nome, reparti in data.items():
        for ruolo, giocatori in reparti.items():
            for p in giocatori:
                nome_giocatore = pulisci_nome(p["name"])
                if nome_giocatore in nuovi_voti:
                    p["mv"] = nuovi_voti[nome_giocatore]["mv"]
                    p["fm"] = nuovi_voti[nome_giocatore]["fm"]
                    aggiornati_totali += 1

    # 4. Salva il file data.json aggiornato con le nuove medie
    with open(FILE_DATI, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"✅ Aggiornamento completato con successo!")
    print(f"⚽ Totale giocatori aggiornati in tutte le rose della lega: {aggiornati_totali}")

if __name__ == "__main__":
    aggiorna_fantamedia_da_file()
