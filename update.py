import json
import datetime

def main():
    print(f"[{datetime.datetime.now()}] Esecuzione aggiornamento giornaliero Fantacalcio...")
    
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Qui potrai aggiungere logiche di aggiornamento automatico
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print("Aggiornamento completato con successo!")
    except Exception as e:
        print(f"Errore durante l'aggiornamento: {e}")

if __name__ == "__main__":
    main()