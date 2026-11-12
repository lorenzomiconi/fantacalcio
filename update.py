import csv
import json
import os

FILE_DATI = "data.json"
FILE_CSV_VOTI = "statistiche_fantapazz.csv"  # Il file che scarichi da Fantapazz

def aggiorna_fantamedia_da_file():
    # 1. Controlla se esiste il file delle rose (data.json)
    if not os.path.exists(FILE_DATI):
        print(f"❌ Errore: Il file {FILE_DATI} non esiste nella cartella.")
        return

    # 2. Controlla se hai messo il file CSV dei voti nella cartella
    if not os.path.exists(FILE_CSV_VOTI):
        print(f"⚠️ Attenzione: Il file '{FILE_CSV_VOTI}' non è stato trovato nella cartella.")
        print(f"👉 Scarica il file CSV da Fantapazz, rinominalo in '{FILE_CSV_VOTI}' e mettilo qui dentro.")
        return

    # Carica le tue rose attuali
    with open(FILE_DATI, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("📊 Lettura del file dei voti in corso...")
    
    # Dizionario per memorizzare i voti trovati nel file CSV: { "NOME_GIOCATORE": {"mv": X, "fm": Y} }
    nuovi_voti = {}

    try:
        with open(FILE_CSV_VOTI, mode="r", encoding="utf-8-sig") as csv_file:
            # Rileva automaticamente il separatore (virgola o punto e virgola)
            sample = csv_file.read(2048)
            csv_file.seek(0)
            dialect = csv.Sniffer().sniff(sample)
            
            reader = csv.DictReader(csv_file, dialect=dialect)
            
            for row in reader:
                # Cerca i campi del nome e delle medie nel file CSV di Fantapazz
                # (I nomi delle colonne possono variare leggermente a seconda dell'export)
                nome = row.get("Calciatore") or row.get("Nome") or row.get("Giocatore")
                mv = row.get("MV") or row.get("Media Voto")
                fm = row.get("FM") or row.get("Fantamedia")
                
                if nome and mv and fm:
                    try:
                        # Pulisce i valori convertendoli in numeri decimali
                        clean_mv = float(mv.replace(",", "."))
                        clean_fm = float(fm.replace(",", "."))
                        nuovi_voti[nome.strip().upper()] = {"mv": clean_mv, "fm": clean_fm}
                    except ValueError:
                        continue
                        
    except Exception as e:
        print(f"❌ Errore durante la lettura del file CSV: {e}")
        return

    # 3. Aggiorna automaticamente tutte le squadre nel file data.json
    aggiornati_totali = 0
    
    for squadra_nome, reparti in data.items():
        for ruolo, giocatori in reparti.items():
            for p in giocatori:
                nome_giocatore = p["name"].upper()
                if nome_giocatore in nuovi_voti:
                    p["mv"] = nuovi_voti[nome_giocatore]["mv"]
                    p["fm"] = nouveaux_voti_fm = nuovi_voti[nome_giocatore]["fm"] # Corretto
                    p["fm"] = nuovi_voti[nome_giocatore]["fm"]
                    aggiornati_totali += 1

    # 4. Salva il file data.json aggiornato
    with open(FILE_DATI, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"✅ Aggiornamento completato con successo!")
    print(f"⚽ Totale giocatori aggiornati nelle tue rose: {aggiornati_totali}")

if __name__ == "__main__":
    aggiorna_fantamedia_da_file()
