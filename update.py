"""
Aggiorna MV, FM, Infortunati e Diffidati di tutti i giocatori in data.json leggendo le statistiche
di Fantapazz: https://www.fantapazz.com/fantacalcio/statistiche
e la pagina indisponibili/squalificati: https://www.fantapazz.com/fantacalcio/indisponibili

Uso:
    python update.py              # scarica dal sito (fonte: Fantapazz)
    python update.py --fonte GDS  # usa le medie Gazzetta (FP, GDS, CDS, STAT)
    python update.py --file statistiche_fantapazz.xlsx   # usa un file scaricato a mano

Dipendenze:  pip install pandas lxml requests openpyxl
"""
import argparse
import difflib
import io
import json
import os
import re
import shutil
import unicodedata

import pandas as pd

URL_STATISTICHE = "https://www.fantapazz.com/fantacalcio/statistiche"
URL_INDISPONIBILI = "https://www.fantapazz.com/fantacalcio/indisponibili"
FILE_DATI = "data.json"
FILE_REPORT = "report_aggiornamento.txt"
FILE_LOCALI = ["statistiche_fantapazz.xlsx", "statistiche_fantapazz.xls", "statistiche_fantapazz.csv"]

FONTI = {"FP": "fp", "GDS": "gds", "CDS": "cds", "STAT": "votostat"}

CLUB = {
    "ATALANTA": "ATA", "BOLOGNA": "BOL", "CAGLIARI": "CAG", "COMO": "COM",
    "FIORENTINA": "FIO", "FROSINONE": "FRO", "GENOA": "GEN", "INTER": "INT",
    "JUVENTUS": "JUV", "LAZIO": "LAZ", "LECCE": "LEC", "MILAN": "MIL",
    "MONZA": "MON", "NAPOLI": "NAP", "PARMA": "PAR", "ROMA": "ROM",
    "SASSUOLO": "SAS", "TORINO": "TOR", "UDINESE": "UDI", "VENEZIA": "VEN",
    "VERONA": "VER",
}
RUOLI = {"1": "por", "2": "dif", "3": "cen", "4": "att", "P": "por", "D": "dif", "C": "cen", "A": "att"}

ALIAS = {}
SOGLIA = 0.82


def norm(s):
    s = unicodedata.normalize("NFKD", str(s or ""))
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.upper().replace("'", "").replace("’", "")
    s = re.sub(r"[^A-Z0-9]+", " ", s)
    return s.strip()


def sigla_club(nome_squadra):
    n = norm(nome_squadra)
    if n == "JUVE":
        n = "JUVENTUS"
    if n in CLUB:
        return CLUB[n]
    m = difflib.get_close_matches(n, list(CLUB), n=1, cutoff=0.75)
    return CLUB[m[0]] if m else None


def cognome_e_token(nome_sito):
    toks = norm(nome_sito).split()
    toks_senza_iniziali = [t for t in toks if len(t) > 1] or toks
    return " ".join(toks_senza_iniziali), toks_senza_iniziali


def punteggio(nome_json, nome_sito):
    a = norm(nome_json)
    cog, toks = cognome_e_token(nome_sito)
    a_ns, cog_ns = a.replace(" ", ""), cog.replace(" ", "")
    if a_ns == cog_ns or a_ns == norm(nome_sito).replace(" ", ""):
        return 1.0
    ta = set(a.split())
    ts = set(toks)
    if ta and ts and (ta <= ts or ts <= ta):
        return 0.95
    return max(
        difflib.SequenceMatcher(None, a_ns, cog_ns).ratio(),
        difflib.SequenceMatcher(None, a, norm(nome_sito)).ratio(),
    )


def numero(v):
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return None
    try:
        return float(str(v).strip().replace(",", "."))
    except ValueError:
        return None


def trova_colonna(colonne, prefisso, fonte_key):
    for c in colonne:
        k = re.sub(r"[^a-z0-9]", "", str(c).lower())
        if k.startswith(prefisso) and k[len(prefisso):] == fonte_key:
            return c
    return None


def tabella_da_html(html):
    for t in pd.read_html(io.StringIO(html)):
        if isinstance(t.columns, pd.MultiIndex):
            t.columns = [" ".join(str(x) for x in col if "Unnamed" not in str(x)).strip() for col in t.columns]
        if any("calciatore" in str(c).lower() for c in t.columns):
            return t
    raise ValueError("Nessuna tabella con la colonna 'Calciatore' trovata nella pagina.")


def carica_tabella(file_locale):
    if file_locale:
        return leggi_file(file_locale)
    import requests
    print(f"🌐 Scarico {URL_STATISTICHE} ...")
    r = requests.get(
        URL_STATISTICHE,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                               "(KHTML, like Gecko) Chrome/124.0 Safari/537.36",
                 "Accept-Language": "it-IT,it;q=0.9"},
        timeout=30,
    )
    r.raise_for_status()
    return tabella_da_html(r.text)


def scarica_indisponibili():
    """Tenta di recuperare infortunati e diffidati dalla pagina dedicata di Fantapazz."""
    infortunati = set()
    diffidati = set()
    try:
        import requests
        print(f"🚑 Scarico infortunati e diffidati da {URL_INDISPONIBILI} ...")
        r = requests.get(
            URL_INDISPONIBILI,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                   "(KHTML, like Gecko) Chrome/124.0 Safari/537.36",
                     "Accept-Language": "it-IT,it;q=0.9"},
            timeout=20,
        )
        r.raise_for_status()
        tables = pd.read_html(io.StringIO(r.text))
        for t in tables:
            cols = [str(c).lower() for c in t.columns]
            c_nome = next((c for c in t.columns if "calciatore" in str(c).lower() or "giocatore" in str(c).lower() or "nome" in str(c).lower()), None)
            c_stato = next((c for c in t.columns if "stato" in str(c).lower() or "motivo" in str(c).lower() or "tipo" in str(c).lower() or "situazione" in str(c).lower()), None)
            if c_nome:
                for _, row in t.iterrows():
                    nome = norm(row[c_nome])
                    if not nome:
                        continue
                    stato_str = " ".join(str(row[c]).lower() for c in t.columns if pd.notna(row[c]))
                    if "diffidat" in stato_str:
                        diffidati.add(nome)
                    elif any(k in stato_str for k in ["infortun", "indisponibil", "lesion", "affatic", "distors", "operat", "stop", "out"]):
                        infortunati.add(nome)
        print(f"✅ Trovati {len(infortunati)} infortunati e {len(diffidati)} diffidati.")
    except Exception as e:
        print(f"⚠️ Impossibile scaricare lista indisponibili automatica ({e}). Mantengo i flag esistenti in data.json.")
    return infortunati, diffidati


def leggi_file(path):
    if path.lower().endswith((".xlsx", ".xls")):
        df = pd.read_excel(path)
    else:
        df = pd.read_csv(path, sep=None, engine="python")
    if not any("calciatore" in str(c).lower() for c in df.columns):
        df.columns = df.iloc[0]
        df = df.drop(df.index[0])
    return df


def estrai_voti(df, fonte):
    key = FONTI[fonte]
    c_nome = next((c for c in df.columns if "calciatore" in str(c).lower()), None)
    c_club = next((c for c in df.columns if str(c).strip().lower() == "club"), None)
    c_ruolo = next((c for c in df.columns if "ruolo" in str(c).lower()), None)
    c_mv = trova_colonna(df.columns, "mv", key)
    c_fm = trova_colonna(df.columns, "fm", key)
    if not (c_nome and c_mv and c_fm):
        raise ValueError(f"Colonne non trovate (nome={c_nome}, mv={c_mv}, fm={c_fm}). "
                         f"Colonne presenti: {list(df.columns)}")
    print(f"📊 Colonne usate: nome='{c_nome}', MV='{c_mv}', FM='{c_fm}'")

    righe = []
    for _, r in df.iterrows():
        nome = r[c_nome]
        if pd.isna(nome):
            continue
        ruolo = None
        if c_ruolo is not None:
            ruolo = RUOLI.get(str(r[c_ruolo]).strip().upper()[:1])
        if ruolo is None:
            for c in df.columns[:2]:
                m = re.match(r"\s*([1-4PDCA])\b", str(r[c]).upper())
                if m:
                    ruolo = RUOLI[m.group(1)]
                    break
        righe.append({
            "nome": str(nome).strip(),
            "club": str(r[c_club]).strip().upper() if c_club is not None and not pd.isna(r[c_club]) else None,
            "ruolo": ruolo,
            "mv": numero(r[c_mv]),
            "fm": numero(r[c_fm]),
        })
    return righe


def trova(p, ruolo, righe):
    club = sigla_club(p["squadra"])
    alias = ALIAS.get((p["name"], ruolo))
    if alias:
        for r in righe:
            if r["nome"] == alias and (club is None or r["club"] == club):
                return r, "alias"

    def migliori(cands, soglia):
        sc = sorted(((punteggio(p["name"], r["nome"]), r) for r in cands), key=lambda x: -(x[0] + (0.05 if x[1]["ruolo"] == ruolo else 0)))
        sc = [(s_, r_) for s_, r_ in sc if s_ >= soglia]
        if not sc:
            return None, "non trovato"
        tot = [s_ + (0.05 if r_["ruolo"] == ruolo else 0) for s_, r_ in sc]
        if len(sc) > 1 and tot[0] - tot[1] < 0.03 and sc[0][1]["nome"] != sc[1][1]["nome"]:
            return None, f"ambiguo ({sc[0][1]['nome']} / {sc[1][1]['nome']})"
        s_, r_ = sc[0]
        return r_, "ok" if s_ >= 0.95 else f"fuzzy ({r_['nome']}, {s_:.2f})"

    in_club = [r for r in righe if r["club"] == club]
    r, motivo = migliori(in_club, SOGLIA)
    if r:
        return r, motivo
    if motivo.startswith("ambiguo"):
        return None, motivo
    altri = [x for x in righe if x["club"] and x["club"] != club]
    r, motivo2 = migliori(altri, 0.93)
    if r:
        return None, f"non trovato nel club; forse e' {r['nome']} ({r['club']}) -> se si', aggiungilo ad ALIAS"
    return None, motivo


def verifica_stato(nome_json, nome_sito, lista_stato):
    if not lista_stato:
        return False
    for item in lista_stato:
        if punteggio(nome_json, item) >= 0.90 or (nome_sito and punteggio(nome_sito, item) >= 0.90):
            return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fonte", default="FP", choices=list(FONTI), type=str.upper,
                    help="FP = Fantapazz (default), GDS, CDS, STAT")
    ap.add_argument("--file", help="file xlsx/csv scaricato a mano da Fantapazz")
    args = ap.parse_args()

    if not os.path.exists(FILE_DATI):
        print(f"❌ {FILE_DATI} non trovato nella cartella corrente.")
        return

    file_locale = args.file
    try:
        df = carica_tabella(file_locale)
    except Exception as e:
        print(f"❌ Download/lettura fallita: {e}")
        loc = next((f for f in FILE_LOCALI if os.path.exists(f)), None)
        if not loc:
            print("👉 Scarica XLS/CSV dalla pagina (pulsante 'Scarica XLS') e rilancia con --file <nomefile>")
            return
        print(f"↪️  Uso il file locale {loc}")
        df = leggi_file(loc)

    righe = estrai_voti(df, args.fonte)
    con_voti = [r for r in righe if r["mv"] is not None and r["fm"] is not None]
    print(f"✅ {len(righe)} calciatori letti, {len(con_voti)} con voti")

    infortunati_set, diffidati_set = scarica_indisponibili() if not file_locale else (set(), set())

    with open(FILE_DATI, "r", encoding="utf-8") as f:
        data = json.load(f)

    log = {"ok": [], "fuzzy": [], "senza_voti": [], "problemi": []}
    for squadra, reparti in data.items():
        for ruolo, giocatori in reparti.items():
            for p in giocatori:
                r, motivo = trova(p, ruolo, righe)
                etichetta = f"{squadra}: {p['name']} ({p['squadra']}, {ruolo})"
                nome_sito = r["nome"] if r else None

                if infortunati_set or diffidati_set:
                    p["infortunato"] = verifica_stato(p["name"], nome_sito, infortunati_set)
                    p["diffidato"] = verifica_stato(p["name"], nome_sito, diffidati_set)
                else:
                    p.setdefault("infortunato", False)
                    p.setdefault("diffidato", False)

                if r is None:
                    log["problemi"].append(f"{etichetta} -> {motivo}")
                elif r["mv"] is None or r["fm"] is None:
                    log["senza_voti"].append(f"{etichetta} -> {r['nome']} (ancora nessun voto)")
                else:
                    p["mv"], p["fm"] = r["mv"], r["fm"]
                    (log["ok"] if motivo in ("ok", "alias") else log["fuzzy"]).append(
                        f"{etichetta} -> {r['nome']} | MV {r['mv']} FM {r['fm']}" + ("" if motivo in ("ok", "alias") else f"  [{motivo}]"))

    shutil.copy(FILE_DATI, FILE_DATI + ".bak")
    with open(FILE_DATI, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    with open(FILE_REPORT, "w", encoding="utf-8") as f:
        for k, titolo in [("problemi", "NON TROVATI / AMBIGUI (aggiungili ad ALIAS)"),
                          ("fuzzy", "ABBINATI APPROSSIMATIVAMENTE (controlla)"),
                          ("senza_voti", "TROVATI MA SENZA VOTI (lasciati invariati)"),
                          ("ok", "ABBINATI")]:
            f.write(f"=== {titolo}: {len(log[k])} ===\n" + "\n".join(log[k]) + "\n\n")

    tot = sum(len(g) for rep in data.values() for g in rep.values())
    print(f"\n⚽ Aggiornati: {len(log['ok']) + len(log['fuzzy'])}/{tot}")
    print(f"   - abbinamenti da controllare: {len(log['fuzzy'])}")
    print(f"   - senza voti (invariati):     {len(log['senza_voti'])}")
    print(f"   - non trovati/ambigui:        {len(log['problemi'])}")
    for riga in log["problemi"]:
        print("   ⚠️ ", riga)
    print(f"\n📝 Dettagli in {FILE_REPORT} (backup: {FILE_DATI}.bak)")


if __name__ == "__main__":
    main()
