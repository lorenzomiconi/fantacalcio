"""
Aggiorna MV, FM, Infortunati e Diffidati di tutti i giocatori in data.json leggendo le statistiche
di Fantapazz: https://www.fantapazz.com/fantacalcio/statistiche
e la pagina probabili formazioni (infortunati, squalificati, diffidati): https://www.fantapazz.com/calcio/fantacalcio/serie-a/probabili-formazioni

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
URL_FORMAZIONI = "https://www.fantapazz.com/calcio/fantacalcio/serie-a/probabili-formazioni"
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

ALIAS = {
    ("RASPADORI", "att"): "Raspadori",   # nel json e' al Napoli, su Fantapazz e' all'Atalanta
    ("HEHHEM", "dif"): "Heggem",         # refuso nel json
}
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


URL_STAT_FC = "https://www.fantacalcio.it/statistiche-serie-a/2026-27/italia/medie"
# alias per i nomi di Fantacalcio.it (nome nel json, ruolo) -> nome sul sito
ALIAS_FC = {
    ("MATINEZ", "por"): "Martinez Jo.",     # refuso nel json: e' il portiere dell'Inter
    ("PIO", "att"): "Esposito F.P.",
    ("RASPADORI", "att"): "Raspadori",     # nel json e' al Napoli, ora e' all'Atalanta
    ("HEHHEM", "dif"): "Heggem",           # refuso nel json
}


def scarica_stat_fantacalcio():
    """Gol, assist, ammonizioni ed espulsioni da Fantacalcio.it (tabella con colonne Gol, Ass, Amm, Esp)."""
    import requests
    r = requests.get(URL_STAT_FC, headers={"User-Agent": "Mozilla/5.0", "Accept-Language": "it-IT,it;q=0.9"}, timeout=30)
    r.raise_for_status()
    for t in pd.read_html(io.StringIO(r.text)):
        cols = {str(c).strip().lower(): c for c in t.columns}
        if all(k in cols for k in ("gol", "ass", "amm", "esp")):
            c_nome = next((c for k, c in cols.items() if "calciator" in k or k in ("nome", "giocatore")), t.columns[0])
            c_sq = cols.get("sq") or cols.get("squadra")
            n = lambda v: int(numero(v) or 0)
            return [{"nome": str(row[c_nome]).strip(), "club": str(row[c_sq]).strip().upper()[:3] if c_sq is not None else None,
                     "ruolo": None, "gol": n(row[cols["gol"]]), "ass": n(row[cols["ass"]]),
                     "amm": n(row[cols["amm"]]), "esp": n(row[cols["esp"]]), "rp": n(row[cols["rp"]]) if "rp" in cols else 0} for _, row in t.iterrows() if not pd.isna(row[c_nome])]
    raise ValueError("tabella con Gol/Ass/Amm/Esp non trovata nella pagina")


def applica_statistiche(data, righe_fc):
    """Scrive gol, assist, gialli, rossi per ogni giocatore. Ritorna i non abbinati."""
    mancanti = []
    for squadra, reparti in data.items():
        if squadra.startswith("_"):
            continue
        for ruolo, giocatori in reparti.items():
            for p in giocatori:
                r, motivo = trova(p, ruolo, righe_fc, ALIAS_FC)
                if r is None:
                    mancanti.append(f"{squadra}: {p['name']} ({p['squadra']}) -> {motivo}")
                    continue
                p["gol"], p["assist"], p["gialli"], p["rossi"] = r["gol"], r["ass"], r["amm"], r["esp"]
                p["rigori_parati"] = r.get("rp", p.get("rigori_parati", 0))
    return mancanti


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


SEZIONI = ["Ballottaggi", "Squalificati", "Infortunati", "In dubbio", "Diffidati", "Ultimo aggiornamento"]
RE_DATA = re.compile(r"^[A-Za-z]{3}, \d{1,2} [A-Za-z]{3}")
RE_BALL = re.compile(r"([^/,]+?)\s*/\s*([^,]+?)\s+(\d+)%\s*-\s*(\d+)%")


def risolvi_nome(testo, noti):
    """Toglie lettera del ruolo (PDCA) attaccata davanti/dietro e ritorna il nome come scritto nelle statistiche."""
    t = re.sub(r"^[-*•]\s*", "", testo.strip())
    t = re.sub(r"\s*\[.*$", "", t).strip()
    cand = [t]
    if len(t) > 2 and t[-1] in "PDCA":
        cand.append(t[:-1].strip())
    if len(t) > 2 and t[0] in "PDCA":
        cand.append(t[1:].strip())
    for c in cand:
        if norm(c) in noti:
            return noti[norm(c)][0]
    return None


def parse_formazioni(testo, righe):
    """testo: pagina in righe di testo. Ritorna {sigla_club: {titolari, panchina, infortunati, ...}}."""
    noti = {}
    for r in righe:
        noti.setdefault(norm(r["nome"]), (r["nome"], r["club"]))
    righe_t = [l.strip() for l in testo.splitlines() if l.strip()]
    out = {}
    for k, l in enumerate(righe_t):
        if l != "Ultime notizie":
            continue
        # nomi prima di "Ultime notizie", fino alla data della partita / fine blocco precedente
        nomi, j = [], k - 1
        while j >= 0 and not RE_DATA.match(righe_t[j]) and righe_t[j] != "Ultimo aggiornamento" and not righe_t[j].startswith("## "):
            n = risolvi_nome(righe_t[j], noti)
            if n:
                nomi.insert(0, n)
            j -= 1
        if len(nomi) < 11:
            continue
        clubs = [noti[norm(n)][1] for n in nomi if noti[norm(n)][1]]
        if not clubs:
            continue
        club = max(set(clubs), key=clubs.count)
        blocco = dict(titolari=nomi[:11], panchina=nomi[11:], infortunati={}, squalificati=[], dubbi={}, diffidati=[], ballottaggi=[])
        # sezioni dopo "Ultime notizie"
        sez, m = None, k + 1
        while m < len(righe_t) and righe_t[m] != "Ultimo aggiornamento":
            riga = righe_t[m]
            if riga in SEZIONI:
                sez = riga
            elif sez == "Ballottaggi":
                for a, b, pa, pb in RE_BALL.findall(riga):
                    na, nb = risolvi_nome(a, noti), risolvi_nome(b, noti)
                    if na and nb:
                        blocco["ballottaggi"].append((na, nb, int(pa), int(pb)))
            elif sez in ("Squalificati", "Infortunati", "In dubbio", "Diffidati"):
                n = risolvi_nome(riga, noti)
                nota = re.search(r"\[(.*?)\]", riga)
                if n and sez == "Squalificati":
                    blocco["squalificati"].append(n)
                elif n and sez == "Infortunati":
                    blocco["infortunati"][n] = nota.group(1) if nota else ""
                elif n and sez == "In dubbio":
                    blocco["dubbi"][n] = ""
                elif n and sez == "Diffidati":
                    blocco["diffidati"].append(n)
                elif sez == "Infortunati" and blocco["infortunati"] and not n:   # nota su riga separata
                    ultimo = list(blocco["infortunati"])[-1]
                    if not blocco["infortunati"][ultimo]:
                        blocco["infortunati"][ultimo] = riga.strip("[] ")
            m += 1
        out[club] = blocco
    return out


def scarica_formazioni(righe):
    import requests
    from bs4 import BeautifulSoup
    r = requests.get(URL_FORMAZIONI, headers={"User-Agent": "Mozilla/5.0", "Accept-Language": "it-IT,it;q=0.9"}, timeout=30)
    r.raise_for_status()
    testo = BeautifulSoup(r.text, "lxml").get_text("\n")
    return parse_formazioni(testo, righe)



def flag_news(p, ruolo, riga, news):
    """Ritorna (infortunato, diffidato, nota, squalificato) usando SEMPRE il club: evita gli omonimi (Kone I. Sassuolo != Kone M. Roma)."""
    club = riga["club"] if riga else sigla_club(p["squadra"])
    nome_sito = riga["nome"] if riga else None
    alias = ALIAS.get((p["name"], ruolo))
    if alias:
        nome_sito = alias
        for c_, b_ in news.items():
            if alias in (list(b_["titolari"]) + list(b_["panchina"]) + list(b_["infortunati"]) + list(b_["squalificati"])):
                club = c_
    b = news.get(club)
    if not b:
        return False, False, "", False
    if nome_sito is None:
        tutti = list(b["titolari"]) + list(b["panchina"]) + list(b["infortunati"]) + list(b["squalificati"]) + list(b["dubbi"]) + list(b["diffidati"])
        sc = sorted(((punteggio(p["name"], n), n) for n in tutti), reverse=True)
        nome_sito = sc[0][1] if sc and sc[0][0] >= SOGLIA else None
    if nome_sito is None:
        return False, False, "", False
    if nome_sito in b["squalificati"]:
        return False, False, "Squalificato", True
    if nome_sito in b["infortunati"]:
        return True, False, b["infortunati"][nome_sito], False
    return False, nome_sito in b["diffidati"], "", False

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
            "pres": None,
        })
    return righe


def trova(p, ruolo, righe, aliases=None):
    club = sigla_club(p["squadra"])
    alias = (ALIAS if aliases is None else aliases).get((p["name"], ruolo))
    if alias:
        for r in righe:
            if r["nome"] == alias:
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

    news = {}
    if not file_locale:
        try:
            news = scarica_formazioni(righe)
            if len(news) < 10:
                raise ValueError(f"trovate solo {len(news)} squadre su 20: la pagina e' cambiata?")
            print(f"📰 Infortunati/diffidati letti per {len(news)} squadre")
        except Exception as e:
            news = {}
            print(f"⚠️ News non aggiornate ({e}). Mantengo i flag esistenti in data.json.")

    with open(FILE_DATI, "r", encoding="utf-8") as f:
        data = json.load(f)

    log = {"ok": [], "fuzzy": [], "senza_voti": [], "problemi": []}
    for squadra, reparti in data.items():
        for ruolo, giocatori in reparti.items():
            for p in giocatori:
                r, motivo = trova(p, ruolo, righe)
                etichetta = f"{squadra}: {p['name']} ({p['squadra']}, {ruolo})"
                nome_sito = r["nome"] if r else None

                if news:
                    p["infortunato"], p["diffidato"], nota, p["squalificato"] = flag_news(p, ruolo, r, news)
                    if nota:
                        p["nota"] = nota
                    else:
                        p.pop("nota", None)
                else:
                    p.setdefault("infortunato", False)
                    p.setdefault("diffidato", False)
                    p.setdefault("squalificato", False)

                if r is None:
                    log["problemi"].append(f"{etichetta} -> {motivo}")
                elif r["mv"] is None or r["fm"] is None:
                    log["senza_voti"].append(f"{etichetta} -> {r['nome']} (ancora nessun voto)")
                else:
                    p["mv"], p["fm"] = r["mv"], r["fm"]
                    (log["ok"] if motivo in ("ok", "alias") else log["fuzzy"]).append(
                        f"{etichetta} -> {r['nome']} | MV {r['mv']} FM {r['fm']}" + ("" if motivo in ("ok", "alias") else f"  [{motivo}]"))

    if not file_locale:
        try:
            stat_fc = scarica_stat_fantacalcio()
            manc = applica_statistiche(data, stat_fc)
            print(f"📈 Gol, assist e cartellini aggiornati da Fantacalcio.it ({len(manc)} giocatori non abbinati)")
            for m in manc:
                print("   ⚠️ ", m)
        except Exception as e:
            print(f"⚠️ Gol/assist/cartellini non aggiornati ({e}). Mantengo i valori esistenti.")

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
