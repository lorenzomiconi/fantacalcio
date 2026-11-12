import json

# Nome del file JSON dove sono salvate le rose e le medie
FILE_DATI = "data.json"

def aggiorna_fantamedia():
    try:
        with open(FILE_DATI, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Errore: Il file {FILE_DATI} non esiste nella cartella.")
        return

    print("--- AGGIORNAMENTO FANTAMEDIA ---")
     squadra_scelta = input("Nome della squadra (es. CASCINA): ").strip().upper()
    
    if squadra_scelta not in data:
        print(f"Squadra '{squadra_scelta}' non trovata!")
        return

    ruolo = input("Ruolo del giocatore (por, dif, cen, att): ").strip().lower()
    if ruolo not in data[squadra_scelta]:
        print("Ruolo non valido!")
        return

    nome_giocatore = input("Nome del giocatore da aggiornare: ").strip().upper()
    
    # Cerca il giocatore nella rosa
    giocatore_trovato = None
    for p in data[squadra_scelta][ruolo]:
        if p["name"].upper() == nome_giocatore:
            giocatore_trovato = p
            break

    if not giocatore_trovato:
        print(f"Giocatore {nome_giocatore} non trovato in {squadra_scelta} nel ruolo {ruolo}.")
        return

    try:
        nuova_mv = float(input(f"Inserisci nuova Media Voto (attuale {giocatore_trovato['mv']}): ") or giocatore_trovato['mv'])
        nuova_fm = float(input(f"Inserisci nuova Fantamedia (attuale {giocatore_trovato['fm']}): ") or giocatore_trovato['fm'])
    except ValueError:
        print("Valori non validi. Inserisci numeri decimali (es. 6.5).")
        return

    # Aggiorna i dati
    giocatore_trovato['mv'] = nuova_mv
    giocatore_trovato['fm'] = nuova_fm

    # Salva il file JSON aggiornato
    with open(FILE_DATI, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"✅ Successo! {giocatore_giocatore_nome if 'giocatore_giocatore_nome' in locals() else nome_giocatore} aggiornato: MV={nuova_mv}, FM={nuova_fm}")

if __name__ == "__main__":
    aggiorna_fantamedia()
