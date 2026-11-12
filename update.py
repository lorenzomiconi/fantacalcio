import json
import os
import pandas as pd

FILE_DATI = "data.json"
FILE_EXCEL_VOTI = "statistiche_fantapazz.xlsx"
FILE_CSV_VOTI = "statistiche_fantapazz.csv"

def pulisci_nome(nome):
    if not nome:
        return ""
    return str(nome).strip().upper()

def aggiorna_fantamedia_locale():
    # 1. Controlla se esiste il database locale
    if not os.path.exists(FILE_DATI):
        print(f"❌ Errore: Il file {FILE_DATI} non esiste nella cartella.")
        return

    # 2. Cerca il file dei voti locale (Excel o CSV)
    file_voti = None
    if os.path.exists(FILE_EXCEL_VOTI):
        file_voti = FILE_EXCEL_VOTI
    elif os.path.exists(FILE_CSV_VOTI):
        file_voti = FILE_CSV_VOTI
    else:
        print(f"⚠️ Attenzione: Nessun file dei voti trovato ('{FILE_EXCEL_VOTI}' o '{FILE_CSV_VOTI}').")
        print(f"👉 Metti il file scaricato da Fantapazz nella cartella del progetto.")
        return

    print(f"📊 Lettura voti da '{file_voti}' in corso...")

    nuovi_voti = {}

    try:
        if file_voti.endswith(".xlsx") or file_voti.endswith(".xls"):
            df = pd.read_excel(file_voti)
        else:
            df = pd.read_csv(file_voti)

        # Trova le colonne giuste indipendentemente da come le chiama Fantapazz
        col_nome = next((c for c in df.columns if str(c).upper() in ["CALCIATORE", "NOME", "GIOCATORE"]), None)
        col_mv = next((c for c in df.columns if str(c).upper() in ["MV", "MEDIA VOTO"]), None)
        col_fm = next((c for c in df.columns if str(c).upper() in ["FM", "FANTAMEDIA"]), None)

        if not col_nome or not col_mv or not col_fm:
            # Se le intestazioni sono nella prima riga
            df.columns = df.iloc[0]
            df = df.drop(0)
            col_nome = next((c for c in df.columns if str(c).upper() in ["CALCIATORE", "NOME", "GIOCATORE"]), None)
            col_mv = next((c for c in df.columns if str(c).upper() in ["MV", "MEDIA VOTO"]), None)
            col_fm = next((c for c in df.columns if str(c).upper() in ["FM", "FANTAMEDIA"]), None)

        if not col_nome or not col_mv or not col_fm:
            print("❌ Errore: Impossibile trovare le colonne 'Calciatore', 'MV' e 'FM' nel file.")
            return

        for _, row in df.iterrows():
            nome = row[col_nome]
            mv = row[col_mv]
            fm = row[col_fm]

            if pd.notna(nome) and pd.notna(mv) and pd.notna(fm):
                try:
                    c_nome = pulisci_nome(nome)
                    c_mv = float(str(mv).replace(",", "."))
                    c_fm = float(str(fm).replace(",", "."))
                    nuovi_voti[c_nome] = {"mv": c_mv, "fm": c_fm}
                except ValueError:
                    continue

    except Exception as e:
        print(f"❌ Errore durante la lettura del file: {e}")
        return

    # 3. Carica data.json e aggiorna tutte le squadre
    with open(FILE_DATI, "r", encoding="utf-8") as f:
        data = json.load(f)

    aggiornati = 0
    for squadra_nome, reparti in data.items():
        for ruolo, giocatori in reparti.items():
            for p in giocatori:
                nome_p = pulisci_nome(p["name"])
                if nome_p in nuovi_voti:
                    p["mv"] = nuovi_voti[nome_p]["mv"]
                    p["fm"] = nuovi_voti[nome_p]["fm"]
                    aggiornati += 1

    # 4. Salva il file aggiornato
    with open(FILE_DATI, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"✅ Aggiornamento completato con successo!")
    print(f"⚽ Giocatori aggiornati in tutte le rose: {aggiornati}")

if __name__ == "__main__":
    aggiorna_fantamedia_locale()
