<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Lega Fantacalcio</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #0f172a; color: #f8fafc; font-family: system-ui, -apple-system, sans-serif; }
        select { background-color: #1e293b !important; color: #f8fafc !important; }
    </style>
</head>
<body class="p-4 md:p-8">

    <div class="max-w-7xl mx-auto space-y-6">
        <!-- Header -->
        <header class="flex flex-col md:flex-row justify-between items-center bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-lg gap-4">
            <div>
                <h1 class="text-3xl font-extrabold text-emerald-400">LEGA FANTACALCIO ⚽</h1>
                <p class="text-slate-400 text-sm mt-1">Stagione 2026/2027 • Modificatore Difesa (+0.25)</p>
            </div>
            
            <!-- SELETTORE GIORNATA SERIE A -->
            <div class="flex items-center gap-3 bg-slate-900 p-3 rounded-lg border border-slate-700 z-50">
                <label for="giornataSelect" class="text-xs font-bold text-amber-400 uppercase">📅 Giornata:</label>
                <select id="giornataSelect" onchange="updateAll()" class="cursor-pointer bg-slate-800 border border-slate-600 text-white font-bold text-sm py-1.5 px-3 rounded focus:outline-none focus:ring-2 focus:ring-emerald-500">
                </select>
            </div>
        </header>

        <!-- SEZIONE: CREA LA TUA FORMAZIONE CON SCELTA MODULO -->
        <section class="bg-slate-800 p-6 rounded-xl border-2 border-emerald-500/80 shadow-xl space-y-4">
            <div class="flex flex-col md:flex-row justify-between items-center border-b border-slate-700 pb-3 gap-3">
                <div class="flex items-center gap-4">
                    <h2 class="text-xl font-bold text-emerald-400 flex items-center gap-2">
                        <span>📋</span> Schiera la Tua Formazione (Cascina)
                    </h2>
                    <!-- SCELTA MODULO -->
                    <div class="flex items-center gap-2 bg-slate-900 px-3 py-1 rounded-lg border border-slate-700">
                        <label for="moduloSelect" class="text-xs font-bold text-amber-400">Modulo:</label>
                        <select id="moduloSelect" onchange="initCustomLineupSelectors()" class="cursor-pointer bg-slate-800 text-emerald-400 font-bold text-xs py-1 px-2 rounded focus:outline-none">
                            <option value="3-5-2">3-5-2</option>
                            <option value="4-3-3" selected>4-3-3</option>
                            <option value="4-4-2">4-4-2</option>
                            <option value="4-5-1">4-5-1</option>
                            <option value="5-4-1">5-4-1</option>
                        </select>
                    </div>
                </div>
                <div class="text-xs bg-slate-900 px-3 py-1.5 rounded-lg border border-slate-700 font-mono text-amber-400" id="customLineupStats">
                    MV: 0.00 | FM: 0.00
                </div>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-4 lg:grid-cols-5 gap-3" id="customLineupSelectors">
                <!-- I selettori dei ruoli si rigenerano in base al modulo -->
            </div>
        </section>

        <!-- 1. VISUALIZZATORE ROSE COMPLETE -->
        <div class="bg-slate-800 p-6 rounded-xl border border-slate-700">
            <div class="flex justify-between items-center mb-4 border-b border-slate-700 pb-3">
                <h2 id="teamTitle" class="text-xl font-bold text-slate-100">Rosa Squadra</h2>
                <select id="teamSelect" onchange="renderTeam()" class="cursor-pointer bg-slate-900 border border-slate-600 text-emerald-400 font-bold py-1.5 px-3 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"></select>
            </div>
            
            <div class="overflow-x-auto">
                <table class="w-full text-left text-sm">
                    <thead class="bg-slate-900 text-slate-400 text-xs uppercase">
                        <tr>
                            <th class="p-3">Ruolo</th>
                            <th class="p-3">Giocatore</th>
                            <th class="p-3">Squadra & Partita (Casa / Fuori)</th>
                            <th class="p-3 text-center">Media Voto (MV)</th>
                            <th class="p-3 text-center">Fantamedia (FM)</th>
                        </tr>
                    </thead>
                    <tbody id="rosterTable" class="divide-y divide-slate-700"></tbody>
                </table>
            </div>
        </div>

        <!-- SEZIONE SCONTRO & MEDIE -->
        <section class="bg-slate-800 p-6 rounded-xl border-2 border-emerald-500/50 shadow-2xl">
            <div class="flex flex-col md:flex-row justify-between items-center mb-6 pb-4 border-b border-slate-700 gap-4">
                <div class="flex items-center gap-3">
                    <span class="text-2xl">⚔️</span>
                    <h2 class="text-2xl font-black text-amber-400 uppercase tracking-wide">Scontro & Medie per Giornata</h2>
                </div>
                
                <div class="flex items-center gap-4 bg-slate-900 p-3 rounded-lg border border-slate-700">
                    <span class="text-sm font-bold text-emerald-400">CASCINA</span>
                    <span class="text-xs font-black text-slate-500">VS</span>
                    <select id="opponentSelect" onchange="renderMatchup()" class="cursor-pointer bg-slate-800 border border-slate-600 text-amber-400 font-bold text-sm py-1.5 px-3 rounded focus:outline-none focus:ring-2 focus:ring-amber-500">
                    </select>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="bg-slate-900/90 p-5 rounded-lg border border-emerald-500/30 space-y-3">
                    <div class="flex justify-between items-center border-b border-slate-800 pb-2">
                        <h3 class="text-lg font-bold text-emerald-400">🛡️ CASCINA</h3>
                        <div id="cascinaAverages" class="text-xs font-bold text-slate-300">MV: - | FM: -</div>
                    </div>
                    <div id="cascinaMatchupLineup" class="space-y-2"></div>
                </div>

                <div class="bg-slate-900/90 p-5 rounded-lg border border-amber-500/30 space-y-3">
                    <div class="flex justify-between items-center border-b border-slate-800 pb-2">
                        <h3 id="opponentMatchupTitle" class="text-lg font-bold text-amber-400">⚔️ AVVERSARIO</h3>
                        <div id="opponentAverages" class="text-xs font-bold text-slate-300">MV: - | FM: -</div>
                    </div>
                    <div id="opponentMatchupLineup" class="space-y-2"></div>
                </div>
            </div>
        </section>

        <!-- 2. SEZIONE FORMAZIONE CONSIGLIATA -->
        <section class="bg-slate-800 p-6 rounded-xl border border-slate-700 space-y-4">
            <div class="flex justify-between items-center border-b border-slate-700 pb-3">
                <h2 class="text-xl font-bold text-emerald-400 flex items-center gap-2">
                    <span>💡</span> Formazione Ideale Consigliata (Cascina)
                </h2>
                <span class="bg-emerald-500/20 text-emerald-300 text-xs font-bold px-3 py-1 rounded-full border border-emerald-500/30">
                    MODULO 4-3-3
                </span>
            </div>
            <div id="recommendedLineup" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4"></div>
        </section>
    </div>

    <script>
        const leagueData = {
            "CASCINA": {
                "por": [{"name": "OKOYE", "squadra": "UDINESE", "mv": 6.0, "fm": 6.0}, {"name": "PESSINA", "squadra": "BOLOGNA", "mv": 6.0, "fm": 6.0}, {"name": "SKORUPSKI", "squadra": "BOLOGNA", "mv": 6.0, "fm": 6.0}],
                "dif": [{"name": "BRACAGLIA", "squadra": "FROSINONE", "mv": 6.0, "fm": 6.0}, {"name": "DEL PRATO", "squadra": "PARMA", "mv": 6.0, "fm": 6.0}, {"name": "KEMPF", "squadra": "COMO", "mv": 6.0, "fm": 6.0}, {"name": "LUCUMI", "squadra": "JUVENTUS", "mv": 6.0, "fm": 6.0}, {"name": "MANGAS", "squadra": "MONZA", "mv": 6.0, "fm": 6.0}, {"name": "ZORTEA", "squadra": "BOLOGNA", "mv": 6.0, "fm": 6.0}, {"name": "VASQUEZ", "squadra": "GENOA", "mv": 6.0, "fm": 6.0}, {"name": "RAMON", "squadra": "COMO", "mv": 6.0, "fm": 6.0}],
                "cen": [{"name": "COLOMBO", "squadra": "GENOA", "mv": 6.0, "fm": 6.0}, {"name": "BERNARDESCHI", "squadra": "BOLOGNA", "mv": 6.0, "fm": 6.0}, {"name": "CACCIAMANI", "squadra": "TORINO", "mv": 6.0, "fm": 6.0}, {"name": "CALHANOGLU", "squadra": "INTER", "mv": 6.0, "fm": 6.0}, {"name": "DOUGLAS", "squadra": "JUVENTUS", "mv": 6.0, "fm": 6.0}, {"name": "MOREIRA", "squadra": "MILAN", "mv": 6.0, "fm": 6.0}, {"name": "PULISIC", "squadra": "MILAN", "mv": 6.0, "fm": 6.0}, {"name": "WINKS", "squadra": "CAGLIARI", "mv": 6.0, "fm": 6.0}],
                "att": [{"name": "PIO", "squadra": "INTER", "mv": 6.0, "fm": 6.0}, {"name": "COLOMBO", "squadra": "GENOA", "mv": 6.0, "fm": 6.0}, {"name": "MOTA", "squadra": "MONZA", "mv": 6.0, "fm": 6.0}, {"name": "GEUBBELS", "squadra": "LECCE", "mv": 6.0, "fm": 6.0}, {"name": "NOSLIN", "squadra": "LAZIO", "mv": 6.0, "fm": 6.0}, {"name": "SCAMACCA", "squadra": "ATALANTA", "mv": 6.0, "fm": 6.0}]
            },
            "AC PICCHIA": {
                "por": [{"name": "MAIGNAN", "squadra": "MILAN", "mv": 6.0, "fm": 6.0}, {"name": "PERRI", "squadra": "TORINO", "mv": 6.0, "fm": 6.0}, {"name": "TORRIANI", "squadra": "MILAN", "mv": 6.0, "fm": 6.0}],
                "dif": [{"name": "CINQUEGRANO", "squadra": "SASSUOLO", "mv": 6.0, "fm": 6.0}, {"name": "GHILARDI", "squadra": "ROMA", "mv": 6.0, "fm": 6.0}, {"name": "MANCINI", "squadra": "ROMA", "mv": 6.0, "fm": 6.0}, {"name": "MIRANDA", "squadra": "BOLOGNA", "mv": 6.0, "fm": 6.0}, {"name": "PEDRAZA", "squadra": "LAZIO", "mv": 6.0, "fm": 6.0}, {"name": "SCALVINI", "squadra": "ATALANTA", "mv": 6.0, "fm": 6.0}, {"name": "TAVBARES", "squadra": "LAZIO", "mv": 6.0, "fm": 6.0}, {"name": "VALLE", "squadra": "COMO", "mv": 6.0, "fm": 6.0}],
                "cen": [{"name": "ATTA", "squadra": "FIORENTINA", "mv": 6.0, "fm": 6.0}, {"name": "COLPANI", "squadra": "MONZA", "mv": 6.0, "fm": 6.0}, {"name": "JONES", "squadra": "INTER", "mv": 6.0, "fm": 6.0}, {"name": "MBANGULA", "squadra": "BOLOGNA", "mv": 6.0, "fm": 6.0}, {"name": "MCTOMINAY", "squadra": "NAPOLI", "mv": 6.0, "fm": 6.0}, {"name": "RABIOT", "squadra": "MILAN", "mv": 6.0, "fm": 6.0}, {"name": "ROMANO", "squadra": "CAGLIARI", "mv": 6.0, "fm": 6.0}, {"name": "SAMARDZIC", "squadra": "ATALANTA", "mv": 6.0, "fm": 6.0}],
                "att": [{"name": "CAMARDA", "squadra": "MILAN", "mv": 6.0, "fm": 6.0}, {"name": "CASTRO", "squadra": "ROMA", "mv": 6.0, "fm": 6.0}, {"name": "DIAO", "squadra": "COMO", "mv": 6.0, "fm": 6.0}, {"name": "KOLO", "squadra": "JUVENTUS", "mv": 6.0, "fm": 6.0}, {"name": "LAURIENTE'", "squadra": "SASSUOLO", "mv": 6.0, "fm": 6.0}, {"name": "VARELA", "squadra": "MONZA", "mv": 6.0, "fm": 6.0}]
            },
            "AS ORCA": {
                "por": [{"name": "MATINEZ", "squadra": "INTER", "mv": 6.0, "fm": 6.0}, {"name": "PROVEDEL", "squadra": "INTER", "mv": 6.0, "fm": 6.0}, {"name": "STANKOVIC", "squadra": "VENEZIA", "mv": 6.0, "fm": 6.0}],
                "dif": [{"name": "BADIASHILE", "squadra": "NAPOLI", "mv": 6.0, "fm": 6.0}, {"name": "BELLANOVA", "squadra": "ATALANTA", "mv": 6.0, "fm": 6.0}, {"name": "AUGUSTO", "squadra": "INTER", "mv": 6.0, "fm": 6.0}, {"name": "HAINAUT", "squadra": "VENEZIA", "mv": 6.0, "fm": 6.0}, {"name": "JIMENEZ", "squadra": "FIORENTINA", "mv": 6.0, "fm": 6.0}, {"name": "PROVSTGAARD", "squadra": "LAZIO", "mv": 6.0, "fm": 6.0}, {"name": "SPINAZZOLA", "squadra": "NAPOLI", "mv": 6.0, "fm": 6.0}, {"name": "WEALEY", "squadra": "ROMA", "mv": 6.0, "fm": 6.0}],
                "cen": [{"name": "CAMBIAGHI", "squadra": "BOLOGNA", "mv": 6.0, "fm": 6.0}, {"name": "CONCEICAO", "squadra": "JUVENTUS", "mv": 6.0, "fm": 6.0}, {"name": "DIOUF", "squadra": "INTER", "mv": 6.0, "fm": 6.0}, {"name": "FAZZINI", "squadra": "CAGLIARI", "mv": 6.0, "fm": 6.0}, {"name": "MODRIC", "squadra": "MILAN", "mv": 6.0, "fm": 6.0}, {"name": "PISILLI", "squadra": "ROMA", "mv": 6.0, "fm": 6.0}, {"name": "ZACCAGNI", "squadra": "LAZIO", "mv": 6.0, "fm": 6.0}, {"name": "ZHEGROVA", "squadra": "JUVENTUS", "mv": 6.0, "fm": 6.0}],
                "att": [{"name": "BETO", "squadra": "FIORENTINA", "mv": 6.0, "fm": 6.0}, {"name": "BOGA", "squadra": "JUVENTUS", "mv": 6.0, "fm": 6.0}, {"name": "HOJLIND", "squadra": "NAPOLI", "mv": 6.0, "fm": 6.0}, {"name": "LUCCA", "squadra": "NAPOLI", "mv": 6.0, "fm": 6.0}, {"name": "PICCOLI", "squadra": "BOLOGNA", "mv": 6.0, "fm": 6.0}, {"name": "TOURE'", "squadra": "PARMA", "mv": 6.0, "fm": 6.0}]
            },
            "AS TRONZI": {
                "por": [{"name": "NETO", "squadra": "JUVENTUS", "mv": 6.0, "fm": 6.0}, {"name": "VICARIO", "squadra": "JUVENTUS", "mv": 6.0, "fm": 6.0}, {"name": "TORNQVIST", "squadra": "MONZA", "mv": 6.0, "fm": 6.0}],
                "dif": [{"name": "BERNASCONI", "squadra": "ATALANTA", "mv": 6.0, "fm": 6.0}, {"name": "DOEKHI", "squadra": "LAZIO", "mv": 6.0, "fm": 6.0}, {"name": "GALLO", "squadra": "LECCE", "mv": 6.0, "fm": 6.0}, {"name": "GILA", "squadra": "MILAN", "mv": 6.0, "fm": 6.0}, {"name": "KRISTENSEN", "squadra": "ATALANTA", "mv": 6.0, "fm": 6.0}, {"name": "RRAHMANI", "squadra": "NAPOLI", "mv": 6.0, "fm": 6.0}, {"name": "SPENCE", "squadra": "INTER", "mv": 6.0, "fm": 6.0}, {"name": "VALERI", "squadra": "PARMA", "mv": 6.0, "fm": 6.0}],
                "cen": [{"name": "CASADEI", "squadra": "TORINO", "mv": 6.0, "fm": 6.0}, {"name": "CISSE", "squadra": "MILAN", "mv": 6.0, "fm": 6.0}, {"name": "GONCALVES", "squadra": "FIORENTINA", "mv": 6.0, "fm": 6.0}, {"name": "MCKENNIE", "squadra": "JUVENTUS", "mv": 6.0, "fm": 6.0}, {"name": "MILA", "squadra": "COMO", "mv": 6.0, "fm": 6.0}, {"name": "NICO PAZ", "squadra": "COMO", "mv": 6.0, "fm": 6.0}, {"name": "ZANIOLO", "squadra": "UDINESE", "mv": 6.0, "fm": 6.0}, {"name": "THORSTVEDT", "squadra": "SASSUOLO", "mv": 6.0, "fm": 6.0}],
                "att": [{"name": "BOBCEK", "squadra": "FROSINONE", "mv": 6.0, "fm": 6.0}, {"name": "CARLOS", "squadra": "CAGLIARI", "mv": 6.0, "fm": 6.0}, {"name": "KRSTOVIC", "squadra": "ATALANTA", "mv": 6.0, "fm": 6.0}, {"name": "PELLEGRINO", "squadra": "FIORENTINA", "mv": 6.0, "fm": 6.0}, {"name": "RAMOS", "squadra": "MILAN", "mv": 6.0, "fm": 6.0}, {"name": "YEBOAH", "squadra": "VENEZIA", "mv": 6.0, "fm": 6.0}]
            },
            "LUCREZIA": {
                "por": [{"name": "FALCONE", "squadra": "LECCE", "mv": 6.0, "fm": 6.0}, {"name": "GOLLINI", "squadra": "ROMA", "mv": 6.0, "fm": 6.0}, {"name": "SVILAR", "squadra": "ROMA", "mv": 6.0, "fm": 6.0}],
                "dif": [{"name": "ALABA", "squadra": "UDINESE", "mv": 6.0, "fm": 6.0}, {"name": "BELGHALI", "squadra": "TORINO", "mv": 6.0, "fm": 6.0}, {"name": "COUTO", "squadra": "COMO", "mv": 6.0, "fm": 6.0}, {"name": "DI MARCO", "squadra": "INTER", "mv": 6.0, "fm": 6.0}, {"name": "MARIN", "squadra": "NAPOLI", "mv": 6.0, "fm": 6.0}, {"name": "N'DIKA", "squadra": "ROMA", "mv": 6.0, "fm": 6.0}, {"name": "SUTALO", "squadra": "LAZIO", "mv": 6.0, "fm": 6.0}, {"name": "THEATE", "squadra": "BOLOGNA", "mv": 6.0, "fm": 6.0}],
                "cen": [{"name": "BAKOLA", "squadra": "SASSUOLO", "mv": 6.0, "fm": 6.0}, {"name": "FABBIAN", "squadra": "PARMA", "mv": 6.0, "fm": 6.0}, {"name": "FRATTESI", "squadra": "LAZIO", "mv": 6.0, "fm": 6.0}, {"name": "RODRIGUEZ", "squadra": "COMO", "mv": 6.0, "fm": 6.0}, {"name": "ROWE", "squadra": "ATALANTA", "mv": 6.0, "fm": 6.0}, {"name": "SAELEMAEKERS", "squadra": "MILAN", "mv": 6.0, "fm": 6.0}, {"name": "VERGARA", "squadra": "NAPOLI", "mv": 6.0, "fm": 6.0}, {"name": "VLASIC", "squadra": "TORINO", "mv": 6.0, "fm": 6.0}],
                "att": [{"name": "BONNY", "squadra": "INTER", "mv": 6.0, "fm": 6.0}, {"name": "DAVIS", "squadra": "UDINESE", "mv": 6.0, "fm": 6.0}, {"name": "DE KATELAERE", "squadra": "ATALANTA", "mv": 6.0, "fm": 6.0}, {"name": "ESPOSITO", "squadra": "SASSUOLO", "mv": 6.0, "fm": 6.0}, {"name": "SOULE'", "squadra": "ROMA", "mv": 6.0, "fm": 6.0}, {"name": "WOLTEMADE", "squadra": "JUVENTUS", "mv": 6.0, "fm": 6.0}]
            },
            "SBLOCCUSELLI": {
                "por": [{"name": "BIJLOW", "squadra": "GENOA", "mv": 6.0, "fm": 6.0}, {"name": "CHRISTENSEN", "squadra": "FIORENTINA", "mv": 6.0, "fm": 6.0}, {"name": "DE GEA", "squadra": "FIORENTINA", "mv": 6.0, "fm": 6.0}],
                "dif": [{"name": "AKANJI", "squadra": "INTER", "mv": 6.0, "fm": 6.0}, {"name": "CALVANI", "squadra": "FROSINONE", "mv": 6.0, "fm": 6.0}, {"name": "HERMOSO", "squadra": "ROMA", "mv": 6.0, "fm": 6.0}, {"name": "KAMARA", "squadra": "UDINESE", "mv": 6.0, "fm": 6.0}, {"name": "MOLINA", "squadra": "ROMA", "mv": 6.0, "fm": 6.0}, {"name": "OYONO", "squadra": "FROSINONE", "mv": 6.0, "fm": 6.0}, {"name": "RODRIGUEZ", "squadra": "CAGLIARI", "mv": 6.0, "fm": 6.0}, {"name": "BISSEK", "squadra": "INTER", "mv": 6.0, "fm": 6.0}],
                "cen": [{"name": "BATURINA", "squadra": "COMO", "mv": 6.0, "fm": 6.0}, {"name": "CALò", "squadra": "FROSINONE", "mv": 6.0, "fm": 6.0}, {"name": "FAGIOLI", "squadra": "FIORENTINA", "mv": 6.0, "fm": 6.0}, {"name": "CHUKWUEZE", "squadra": "MILAN", "mv": 6.0, "fm": 6.0}, {"name": "MATIC", "squadra": "SASSUOLO", "mv": 6.0, "fm": 6.0}, {"name": "ORSOLINI", "squadra": "BOLOGNA", "mv": 6.0, "fm": 6.0}, {"name": "SCHMID", "squadra": "FROSINONE", "mv": 6.0, "fm": 6.0}, {"name": "TAYLOR", "squadra": "LAZIO", "mv": 6.0, "fm": 6.0}],
                "att": [{"name": "ADAMS", "squadra": "TORINO", "mv": 6.0, "fm": 6.0}, {"name": "BERARDI", "squadra": "SASSUOLO", "mv": 6.0, "fm": 6.0}, {"name": "CUTRONE", "squadra": "MONZA", "mv": 6.0, "fm": 6.0}, {"name": "DOUVIKAS", "squadra": "COMO", "mv": 6.0, "fm": 6.0}, {"name": "ZEBALLOS", "squadra": "MONZA", "mv": 6.0, "fm": 6.0}, {"name": "KVERNADZE", "squadra": "FROSINONE", "mv": 6.0, "fm": 6.0}]
            },
            "BENEVENGO": {
                "por": [{"name": "CAPRILE", "squadra": "CAGLIARI", "mv": 6.0, "fm": 6.0}, {"name": "CORVI", "squadra": "PARMA", "mv": 6.0, "fm": 6.0}, {"name": "MILINKOVIC", "squadra": "NAPOLI", "mv": 6.0, "fm": 6.0}],
                "dif": [{"name": "BREMER", "squadra": "JUVENTUS", "mv": 6.0, "fm": 6.0}, {"name": "CELIK", "squadra": "JUVENTUS", "mv": 6.0, "fm": 6.0}, {"name": "GRAGUSIN", "squadra": "FIORENTINA", "mv": 6.0, "fm": 6.0}, {"name": "FORTINI", "squadra": "TORINO", "mv": 6.0, "fm": 6.0}, {"name": "GATTI", "squadra": "JUVENTUS", "mv": 6.0, "fm": 6.0}, {"name": "LULLI", "squadra": "ROMA", "mv": 6.0, "fm": 6.0}, {"name": "SOLET", "squadra": "UDINESE", "mv": 6.0, "fm": 6.0}, {"name": "STONES", "squadra": "INTER", "mv": 6.0, "fm": 6.0}],
                "cen": [{"name": "ADZIC", "squadra": "SASSUOLO", "mv": 6.0, "fm": 6.0}, {"name": "BARELLA", "squadra": "INTER", "mv": 6.0, "fm": 6.0}, {"name": "GONZALEZ", "squadra": "JUVENTUS", "mv": 6.0, "fm": 6.0}, {"name": "MANDRAGORA", "squadra": "TORINO", "mv": 6.0, "fm": 6.0}, {"name": "MORA", "squadra": "ROMA", "mv": 6.0, "fm": 6.0}, {"name": "PELLEGRINI", "squadra": "ROMA", "mv": 6.0, "fm": 6.0}, {"name": "SUCIC", "squadra": "INTER", "mv": 6.0, "fm": 6.0}, {"name": "ANGUISSA", "squadra": "NAPOLI", "mv": 6.0, "fm": 6.0}],
                "att": [{"name": "LONTANI", "squadra": "PARMA", "mv": 6.0, "fm": 6.0}, {"name": "MARTINEZ", "squadra": "INTER", "mv": 6.0, "fm": 6.0}, {"name": "OSMAJIC", "squadra": "GENOA", "mv": 6.0, "fm": 6.0}, {"name": "RASPADORI", "squadra": "NAPOLI", "mv": 6.0, "fm": 6.0}, {"name": "ROBINSON", "squadra": "MONZA", "mv": 6.0, "fm": 6.0}, {"name": "SANTOS", "squadra": "NAPOLI", "mv": 6.0, "fm": 6.0}]
            },
            "SILVIO": {
                "por": [{"name": "CARNESECCHI", "squadra": "ATALANTA", "mv": 6.0, "fm": 6.0}, {"name": "MURIC", "squadra": "SASSUOLO", "mv": 6.0, "fm": 6.0}, {"name": "SPORTIELLO", "squadra": "ATALANTA", "mv": 6.0, "fm": 6.0}],
                "dif": [{"name": "CHALOBAH", "squadra": "COMO", "mv": 6.0, "fm": 6.0}, {"name": "COMUZZO", "squadra": "TORINO", "mv": 6.0, "fm": 6.0}, {"name": "DE WINTER", "squadra": "MILAN", "mv": 6.0, "fm": 6.0}, {"name": "DOIG", "squadra": "SASSUOLO", "mv": 6.0, "fm": 6.0}, {"name": "KALULU", "squadra": "JUVENTUS", "mv": 6.0, "fm": 6.0}, {"name": "GABRIEL", "squadra": "LECCE", "mv": 6.0, "fm": 6.0}, {"name": "VOJVODA", "squadra": "UDINESE", "mv": 6.0, "fm": 6.0}, {"name": "ZE PEDRP", "squadra": "CAGLIARI", "mv": 6.0, "fm": 6.0}],
                "cen": [{"name": "BALDANZI", "squadra": "GENOA", "mv": 6.0, "fm": 6.0}, {"name": "BUSIO", "squadra": "VENEZIA", "mv": 6.0, "fm": 6.0}, {"name": "DA CUNHA", "squadra": "COMO", "mv": 6.0, "fm": 6.0}, {"name": "EKKELENKAMP", "squadra": "UDINESE", "mv": 6.0, "fm": 6.0}, {"name": "FITZ-JIM", "squadra": "TORINO", "mv": 6.0, "fm": 6.0}, {"name": "GAETANO", "squadra": "ATALANTA", "mv": 6.0, "fm": 6.0}, {"name": "LOBOTKA", "squadra": "NAPOLI", "mv": 6.0, "fm": 6.0}, {"name": "MASTANTUONO", "squadra": "FIORENTINA", "mv": 6.0, "fm": 6.0}],
                "att": [{"name": "EKHATOR", "squadra": "JUVENTUS", "mv": 6.0, "fm": 6.0}, {"name": "NERES", "squadra": "NAPOLI", "mv": 6.0, "fm": 6.0}, {"name": "PINAMONTI", "squadra": "LAZIO", "mv": 6.0, "fm": 6.0}, {"name": "ROMERO", "squadra": "PARMA", "mv": 6.0, "fm": 6.0}, {"name": "SIMEONE", "squadra": "TORINO", "mv": 6.0, "fm": 6.0}, {"name": "THURAM", "squadra": "INTER", "mv": 6.0, "fm": 6.0}]
            },
            "LISBONA": {
                "por": [{"name": "BUTEZ", "squadra": "COMO", "mv": 6.0, "fm": 6.0}, {"name": "MERET", "squadra": "NAPOLI", "mv": 6.0, "fm": 6.0}, {"name": "SANCHEZ", "squadra": "COMO", "mv": 6.0, "fm": 6.0}],
                "dif": [{"name": "BASTONI", "squadra": "INTER", "mv": 6.0, "fm": 6.0}, {"name": "COCO", "squadra": "TORINO", "mv": 6.0, "fm": 6.0}, {"name": "DI LORENZO", "squadra": "NAPOLI", "mv": 6.0, "fm": 6.0}, {"name": "FAVASULI", "squadra": "NAPOLI", "mv": 6.0, "fm": 6.0}, {"name": "FLORIANI", "squadra": "LAZIO", "mv": 6.0, "fm": 6.0}, {"name": "HEHHEM", "squadra": "BOLOGNA", "mv": 6.0, "fm": 6.0}, {"name": "MINA", "squadra": "CAGLIARI", "mv": 6.0, "fm": 6.0}, {"name": "OSTIGARD", "squadra": "GENOA", "mv": 6.0, "fm": 6.0}],
                "cen": [{"name": "ALAJBEGOVIC", "squadra": "JUVENTUS", "mv": 6.0, "fm": 6.0}, {"name": "CANCELLIERI", "squadra": "LAZIO", "mv": 6.0, "fm": 6.0}, {"name": "DE BRUYNE", "squadra": "NAPOLI", "mv": 6.0, "fm": 6.0}, {"name": "KARLSTROM", "squadra": "UDINESE", "mv": 6.0, "fm": 6.0}, {"name": "KESSIE", "squadra": "ATALANTA", "mv": 6.0, "fm": 6.0}, {"name": "NJIE", "squadra": "FIORENTINA", "mv": 6.0, "fm": 6.0}, {"name": "PERRONE", "squadra": "COMO", "mv": 6.0, "fm": 6.0}, {"name": "POLITANO", "squadra": "NAPOLI", "mv": 6.0, "fm": 6.0}],
                "att": [{"name": "ADAMAS", "squadra": "VENEZIA", "mv": 6.0, "fm": 6.0}, {"name": "BOWIE", "squadra": "SASSUOLO", "mv": 6.0, "fm": 6.0}, {"name": "DOVBYK", "squadra": "BOLOGNA", "mv": 6.0, "fm": 6.0}, {"name": "GHEDJEMIS", "squadra": "FROSINONE", "mv": 6.0, "fm": 6.0}, {"name": "MALEN", "squadra": "ROMA", "mv": 6.0, "fm": 6.0}, {"name": "MENDY", "squadra": "CAGLIARI", "mv": 6.0, "fm": 6.0}]
            },
            "EMOIVECI": {
                "por": [{"name": "MANDAS", "squadra": "LAZIO", "mv": 6.0, "fm": 6.0}, {"name": "MOTTA", "squadra": "LAZIO", "mv": 6.0, "fm": 6.0}, {"name": "PALMISANI", "squadra": "FROSINONE", "mv": 6.0, "fm": 6.0}],
                "dif": [{"name": "BALERDI", "squadra": "ROMA", "mv": 6.0, "fm": 6.0}, {"name": "BARTESAGHI", "squadra": "MILAN", "mv": 6.0, "fm": 6.0}, {"name": "CAMBIASO", "squadra": "JUVENTUS", "mv": 6.0, "fm": 6.0}, {"name": "KAIKI", "squadra": "COMO", "mv": 6.0, "fm": 6.0}, {"name": "OBRADOR", "squadra": "SASSUOLO", "mv": 6.0, "fm": 6.0}, {"name": "PAVLOVIC", "squadra": "MILAN", "mv": 6.0, "fm": 6.0}, {"name": "VALDEPENAS", "squadra": "FIORENTINA", "mv": 6.0, "fm": 6.0}, {"name": "ZAPPACOSTA", "squadra": "ATALANTA", "mv": 6.0, "fm": 6.0}],
                "cen": [{"name": "BERNABè", "squadra": "PARMA", "mv": 6.0, "fm": 6.0}, {"name": "CRISTANTE", "squadra": "ROMA", "mv": 6.0, "fm": 6.0}, {"name": "EDERSON", "squadra": "ATALANTA", "mv": 6.0, "fm": 6.0}, {"name": "GUDMUNSSON", "squadra": "LAZIO", "mv": 6.0, "fm": 6.0}, {"name": "KONè", "squadra": "ROMA", "mv": 6.0, "fm": 6.0}, {"name": "PESSINA", "squadra": "MONZA", "mv": 6.0, "fm": 6.0}, {"name": "POBEGA", "squadra": "BOLOGNA", "mv": 6.0, "fm": 6.0}, {"name": "ZIELISKI", "squadra": "INTER", "mv": 6.0, "fm": 6.0}],
                "att": [{"name": "DYBALA", "squadra": "ROMA", "mv": 6.0, "fm": 6.0}, {"name": "KEAN", "squadra": "COMO", "mv": 6.0, "fm": 6.0}, {"name": "RAIMONDO", "squadra": "FROSINONE", "mv": 6.0, "fm": 6.0}, {"name": "VITINHA", "squadra": "GENOA", "mv": 6.0, "fm": 6.0}, {"name": "YILDIZ", "squadra": "JUVENTUS", "mv": 6.0, "fm": 6.0}, {"name": "MALDINI", "squadra": "CAGLIARI", "mv": 6.0, "fm": 6.0}]
            }
        };

        const calendarioUfficiale = {
            1: [
                {home: "INTER", away: "MONZA"}, {home: "UDINESE", away: "COMO"}, {home: "GENOA", away: "NAPOLI"},
                {home: "PARMA", away: "CAGLIARI"}, {home: "FROSINONE", away: "JUVENTUS"}, {home: "MILAN", away: "TORINO"},
                {home: "BOLOGNA", away: "LAZIO"}, {home: "ROMA", away: "FIORENTINA"}, {home: "ATALANTA", away: "SASSUOLO"}, {home: "LECCE", away: "VENEZIA"}
            ],
            2: [
                {home: "NAPOLI", away: "COMO"}, {home: "CAGLIARI", away: "INTER"}, {home: "LAZIO", away: "GENOA"},
                {home: "LECCE", away: "ROMA"}, {home: "TORINO", away: "ATALANTA"}, {home: "BOLOGNA", away: "JUVENTUS"},
                {home: "MILAN", away: "PARMA"}, {home: "MONZA", away: "FROSINONE"}, {home: "UDINESE", away: "VERONA"}, {home: "SASSUOLO", away: "VENEZIA"}
            ],
            3: [
                {home: "INTER", away: "NAPOLI"}, {home: "ROMA", away: "ATALANTA"}, {home: "FROSINONE", away: "VENEZIA"},
                {home: "PARMA", away: "MONZA"}, {home: "JUVENTUS", away: "MILAN"}, {home: "TORINO", away: "LAZIO"},
                {home: "BOLOGNA", away: "CAGLIARI"}, {home: "UDINESE", away: "LECCE"}, {home: "FIORENTINA", away: "SASSUOLO"}, {home: "VERONA", away: "COMO"}
            ],
            4: [
                {home: "LAZIO", away: "MILAN"}, {home: "ATALANTA", away: "CAGLIARI"}, {home: "LECCE", away: "MONZA"},
                {home: "NAPOLI", away: "BOLOGNA"}, {home: "INTER", away: "TORINO"}, {home: "ROMA", away: "VERONA"},
                {home: "FIORENTINA", away: "UDINESE"}, {home: "FROSINONE", away: "SASSUOLO"}, {home: "VENEZIA", away: "COMO"}, {home: "JUVENTUS", away: "PARMA"}
            ],
            5: [
                {home: "UDINESE", away: "CAGLIARI"}, {home: "ROMA", away: "INTER"}, {home: "VENEZIA", away: "LAZIO"},
                {home: "FIORENTINA", away: "NAPOLI"}, {home: "ATALANTA", away: "JUVENTUS"}, {home: "BOLOGNA", away: "TORINO"},
                {home: "MILAN", away: "MONZA"}, {home: "PARMA", away: "SASSUOLO"}, {home: "FROSINONE", away: "COMO"}, {home: "VERONA", away: "LECCE"}
            ],
            6: [
                {home: "INTER", away: "PARMA"}, {home: "NAPOLI", away: "FROSINONE"}, {home: "COMO", away: "ROMA"},
                {home: "LAZIO", away: "MONZA"}, {home: "JUVENTUS", away: "VENEZIA"}, {home: "MILAN", away: "UDINESE"},
                {home: "ATALANTA", away: "BOLOGNA"}, {home: "CAGLIARI", away: "FIORENTINA"}, {home: "TORINO", away: "SASSUOLO"}, {home: "LECCE", away: "VERONA"}
            ],
            7: [
                {home: "FIORENTINA", away: "COMO"}, {home: "MILAN", away: "ATALANTA"}, {home: "JUVENTUS", away: "LAZIO"},
                {home: "PARMA", away: "TORINO"}, {home: "INTER", away: "LECCE"}, {home: "ROMA", away: "GENOA"},
                {home: "NAPOLI", away: "VERONA"}, {home: "BOLOGNA", away: "VENEZIA"}, {home: "CAGLIARI", away: "SASSUOLO"}, {home: "FROSINONE", away: "MONZA"}
            ],
            8: [
                {home: "ATALANTA", away: "FROSINONE"}, {home: "GENOA", away: "VENEZIA"}, {home: "LECCE", away: "JUVENTUS"},
                {home: "UDINESE", away: "MILAN"}, {home: "INTER", away: "FIORENTINA"}, {home: "ROMA", away: "CAGLIARI"},
                {home: "LAZIO", away: "PARMA"}, {home: "NAPOLI", away: "TORINO"}, {home: "MONZA", away: "VERONA"}, {home: "SASSUOLO", away: "BOLOGNA"}
            ],
            9: [
                {home: "TORINO", away: "COMO"}, {home: "MILAN", away: "BOLOGNA"}, {home: "PARMA", away: "UDINESE"},
                {home: "VENEZIA", away: "INTER"}, {home: "MONZA", away: "NAPOLI"}, {home: "GENOA", away: "JUVENTUS"},
                {home: "FROSINONE", away: "LECCE"}, {home: "FIORENTINA", away: "ATALANTA"}, {home: "CAGLIARI", away: "VERONA"}, {home: "ROMA", away: "LAZIO"}
            ],
            10: [
                {home: "UDINESE", away: "ROMA"}, {home: "MILAN", away: "INTER"}, {home: "COMO", away: "VENEZIA"},
                {home: "FROSINONE", away: "TORINO"}, {home: "LAZIO", away: "CAGLIARI"}, {home: "LECCE", away: "GENOA"},
                {home: "JUVENTUS", away: "NAPOLI"}, {home: "SASSUOLO", away: "FIORENTINA"}, {home: "ATALANTA", away: "PARMA"}, {home: "BOLOGNA", away: "MONZA"}
            ],
            11: [
                {home: "ROMA", away: "SASSUOLO"}, {home: "NAPOLI", away: "LAZIO"}, {home: "GENOA", away: "MILAN"},
                {home: "MONZA", away: "ATALANTA"}, {home: "VENEZIA", away: "UDINESE"}, {home: "TORINO", away: "LECCE"},
                {home: "CAGLIARI", away: "FROSINONE"}, {home: "PARMA", away: "BOLOGNA"}, {home: "INTER", away: "COMO"}, {home: "FIORENTINA", away: "JUVENTUS"}
            ],
            12: [
                {home: "JUVENTUS", away: "VENEZIA"}, {home: "BOLOGNA", away: "UDINESE"}, {home: "SASSUOLO", away: "GENOA"},
                {home: "MILAN", away: "FROSINONE"}, {home: "ATALANTA", away: "INTER"}, {home: "COMO", away: "CAGLIARI"},
                {home: "LAZIO", away: "LECCE"}, {home: "PARMA", away: "ROMA"}, {home: "NAPOLI", away: "TORINO"}, {home: "MONZA", away: "FIORENTINA"}
            ],
            13: [
                {home: "INTER", away: "GENOA"}, {home: "UDINESE", away: "FIORENTINA"}, {home: "SASSUOLO", away: "NAPOLI"},
                {home: "ROMA", away: "MONZA"}, {home: "VENEZIA", away: "BOLOGNA"}, {home: "FROSINONE", away: "PARMA"},
                {home: "CAGLIARI", away: "MILAN"}, {home: "ATALANTA", away: "LECCE"}, {home: "COMO", away: "JUVENTUS"}, {home: "TORINO", away: "LAZIO"}
            ],
            14: [
                {home: "JUVENTUS", away: "UDINESE"}, {home: "MILAN", away: "PARMA"}, {home: "VENEZIA", away: "SASSUOLO"},
                {home: "FIORENTINA", away: "CAGLIARI"}, {home: "BOLOGNA", away: "ROMA"}, {home: "MONZA", away: "COMO"},
                {home: "NAPOLI", away: "LECCE"}, {home: "GENOA", away: "TORINO"}, {home: "LAZIO", away: "ATALANTA"}, {home: "FROSINONE", away: "INTER"}
            ],
            15: [
                {home: "COMO", away: "BOLOGNA"}, {home: "LAZIO", away: "ROMA"}, {home: "INTER", away: "TORINO"},
                {home: "PARMA", away: "FIORENTINA"}, {home: "NAPOLI", away: "MILAN"}, {home: "ATALANTA", away: "GENOA"},
                {home: "CAGLIARI", away: "MONZA"}, {home: "LECCE", away: "SASSUOLO"}, {home: "JUVENTUS", away: "FROSINONE"}, {home: "UDINESE", away: "VENEZIA"}
            ],
            16: [
                {home: "ROMA", away: "JUVENTUS"}, {home: "FIORENTINA", away: "BOLOGNA"}, {home: "TORINO", away: "CAGLIARI"},
                {home: "VENEZIA", away: "MONZA"}, {home: "SASSUOLO", away: "PARMA"}, {home: "MILAN", away: "COMO"},
                {home: "GENOA", away: "UDINESE"}, {home: "ATALANTA", away: "NAPOLI"}, {home: "LECCE", away: "INTER"}, {home: "FROSINONE", away: "LAZIO"}
            ],
            17: [
                {home: "TORINO", away: "VENEZIA"}, {home: "ROMA", away: "FROSINONE"}, {home: "MONZA", away: "MILAN"},
                {home: "INTER", away: "SASSUOLO"}, {home: "BOLOGNA", away: "JUVENTUS"}, {home: "COMO", away: "LECCE"},
                {home: "FIORENTINA", away: "LAZIO"}, {home: "NAPOLI", away: "PARMA"}, {home: "ATALANTA", away: "UDINESE"}, {home: "CAGLIARI", away: "GENOA"}
            ],
            18: [
                {home: "VENEZIA", away: "ROMA"}, {home: "MILAN", away: "FIORENTINA"}, {home: "JUVENTUS", away: "TORINO"},
                {home: "FROSINONE", away: "BOLOGNA"}, {home: "LAZIO", away: "INTER"}, {home: "SASSUOLO", away: "UDINESE"},
                {home: "MONZA", away: "CAGLIARI"}, {home: "PARMA", away: "ATALANTA"}, {home: "NAPOLI", away: "GENOA"}, {home: "LECCE", away: "COMO"}
            ],
            19: [
                {home: "TORINO", away: "ATALANTA"}, {home: "INTER", away: "JUVENTUS"}, {home: "CAGLIARI", away: "SASSUOLO"},
                {home: "UDINESE", away: "NAPOLI"}, {home: "MONZA", away: "FROSINONE"}, {home: "ROMA", away: "MILAN"},
                {home: "BOLOGNA", away: "GENOA"}, {home: "COMO", away: "LAZIO"}, {home: "PARMA", away: "VENEZIA"}, {home: "LECCE", away: "FIORENTINA"}
            ],
            20: [
                {home: "ATALANTA", away: "ROMA"}, {home: "CAGLIARI", away: "COMO"}, {home: "JUVENTUS", away: "GENOA"},
                {home: "LAZIO", away: "TORINO"}, {home: "LECCE", away: "BOLOGNA"}, {home: "MILAN", away: "VERONA"},
                {home: "NAPOLI", away: "INTER"}, {home: "PARMA", away: "VENEZIA"}, {home: "SASSUOLO", away: "MONZA"}, {home: "FROSINONE", away: "UDINESE"}
            ],
            21: [
                {home: "BOLOGNA", away: "MILAN"}, {home: "COMO", away: "ATALANTA"}, {home: "GENOA", away: "ROMA"},
                {home: "INTER", away: "CAGLIARI"}, {home: "JUVENTUS", away: "LECCE"}, {home: "LAZIO", away: "PARMA"},
                {home: "NAPOLI", away: "VENEZIA"}, {home: "MONZA", away: "TORINO"}, {home: "UDINESE", away: "SASSUOLO"}, {home: "VERONA", away: "FROSINONE"}
            ],
            22: [
                {home: "ATALANTA", away: "LAZIO"}, {home: "CAGLIARI", away: "JUVENTUS"}, {home: "FROSINONE", away: "NAPOLI"},
                {home: "LECCE", away: "INTER"}, {home: "MILAN", away: "GENOA"}, {home: "PARMA", away: "COMO"},
                {home: "ROMA", away: "BOLOGNA"}, {home: "SASSUOLO", away: "VERONA"}, {home: "TORINO", away: "UDINESE"}, {home: "VENEZIA", away: "MONZA"}
            ],
            23: [
                {home: "BOLOGNA", away: "FROSINONE"}, {home: "COMO", away: "MILAN"}, {home: "GENOA", away: "ATALANTA"},
                {home: "INTER", away: "ROMA"}, {home: "JUVENTUS", away: "PARMA"}, {home: "LAZIO", away: "SASSUOLO"},
                {home: "NAPOLI", away: "CAGLIARI"}, {home: "MONZA", away: "LECCE"}, {home: "UDINESE", away: "VENEZIA"}, {home: "VERONA", away: "TORINO"}
            ],
            24: [
                {home: "ATALANTA", away: "BOLOGNA"}, {home: "CAGLIARI", away: "LAZIO"}, {home: "FROSINONE", away: "GENOA"},
                {home: "LECCE", away: "NAPOLI"}, {home: "MILAN", away: "JUVENTUS"}, {home: "PARMA", away: "INTER"},
                {home: "ROMA", away: "COMO"}, {home: "SASSUOLO", away: "TORINO"}, {home: "VERONA", away: "UDINESE"}, {home: "VENEZIA", away: "MONZA"}
            ],
            25: [
                {home: "BOLOGNA", away: "VERONA"}, {home: "COMO", away: "PARMA"}, {home: "GENOA", away: "CAGLIARI"},
                {home: "INTER", away: "MILAN"}, {home: "JUVENTUS", away: "ATALANTA"}, {home: "LAZIO", away: "FROSINONE"},
                {home: "NAPOLI", away: "ROMA"}, {home: "MONZA", away: "LECCE"}, {home: "UDINESE", away: "TORINO"}, {home: "VENEZIA", away: "SASSUOLO"}
            ],
            26: [
                {home: "ATALANTA", away: "INTER"}, {home: "CAGLIARI", away: "BOLOGNA"}, {home: "FROSINONE", away: "MILAN"},
                {home: "LECCE", away: "ROMA"}, {home: "PARMA", away: "GENOA"}, {home: "SASSUOLO", away: "NAPOLI"},
                {home: "TORINO", away: "JUVENTUS"}, {home: "VERONA", away: "LAZIO"}, {home: "VENEZIA", away: "COMO"}, {home: "MONZA", away: "UDINESE"}
            ],
            27: [
                {home: "BOLOGNA", away: "PARMA"}, {home: "COMO", away: "TORINO"}, {home: "GENOA", away: "MONZA"},
                {home: "INTER", away: "VENEZIA"}, {home: "JUVENTUS", away: "VERONA"}, {home: "LAZIO", away: "NAPOLI"},
                {home: "MILAN", away: "LECCE"}, {home: "ROMA", away: "ATALANTA"}, {home: "SASSUOLO", away: "CAGLIARI"}, {home: "FROSINONE", away: "UDINESE"}
            ],
            28: [
                {home: "ATALANTA", away: "MILAN"}, {home: "CAGLIARI", away: "ROMA"}, {home: "FROSINONE", away: "PARMA"},
                {home: "LECCE", away: "BOLOGNA"}, {home: "NAPOLI", away: "JUVENTUS"}, {home: "TORINO", away: "INTER"},
                {home: "UDINESE", away: "LAZIO"}, {home: "VERONA", away: "GENOA"}, {home: "VENEZIA", away: "SASSUOLO"}, {home: "MONZA", away: "COMO"}
            ],
            29: [
                {home: "BOLOGNA", away: "INTER"}, {home: "COMO", away: "FROSINONE"}, {home: "GENOA", away: "LECCE"},
                {home: "JUVENTUS", away: "CAGLIARI"}, {home: "LAZIO", away: "VERONA"}, {home: "MILAN", away: "ROMA"},
                {home: "PARMA", away: "NAPOLI"}, {home: "SASSUOLO", away: "ATALANTA"}, {home: "TORINO", away: "MONZA"}, {home: "VENEZIA", away: "UDINESE"}
            ],
            30: [
                {home: "ATALANTA", away: "TORINO"}, {home: "CAGLIARI", away: "VENEZIA"}, {home: "FROSINONE", away: "MONZA"},
                {home: "INTER", away: "UDINESE"}, {home: "LAZIO", away: "MILAN"}, {home: "NAPOLI", away: "BOLOGNA"},
                {home: "ROMA", away: "PARMA"}, {home: "SASSUOLO", away: "JUVENTUS"}, {home: "VERONA", away: "LECCE"}, {home: "COMO", away: "GENOA"}
            ],
            31: [
                {home: "BOLOGNA", away: "ATALANTA"}, {home: "GENOA", away: "SASSUOLO"}, {home: "JUVENTUS", away: "INTER"},
                {home: "LECCE", away: "CAGLIARI"}, {home: "MILAN", away: "NAPOLI"}, {home: "PARMA", away: "VERONA"},
                {home: "ROMA", away: "TORINO"}, {home: "UDINESE", away: "FROSINONE"}, {home: "VENEZIA", away: "LAZIO"}, {home: "MONZA", away: "COMO"}
            ],
            32: [
                {home: "ATALANTA", away: "MONZA"}, {home: "CAGLIARI", away: "PARMA"}, {home: "COMO", away: "VERONA"},
                {home: "FROSINONE", away: "ROMA"}, {home: "INTER", away: "LAZIO"}, {home: "JUVENTUS", away: "BOLOGNA"},
                {home: "NAPOLI", away: "GENOA"}, {home: "SASSUOLO", away: "MILAN"}, {home: "TORINO", away: "LECCE"}, {home: "VENEZIA", away: "UDINESE"}
            ],
            33: [
                {home: "BOLOGNA", away: "TORINO"}, {home: "GENOA", away: "INTER"}, {home: "LAZIO", away: "JUVENTUS"},
                {home: "LECCE", away: "COMO"}, {home: "MILAN", away: "CAGLIARI"}, {home: "PARMA", away: "FROSINONE"},
                {home: "ROMA", away: "NAPOLI"}, {home: "UDINESE", away: "ATALANTA"}, {home: "VERONA", away: "VENEZIA"}, {home: "MONZA", away: "SASSUOLO"}
            ],
            34: [
                {home: "ATALANTA", away: "VENEZIA"}, {home: "CAGLIARI", away: "UDINESE"}, {home: "COMO", away: "INTER"},
                {home: "FROSINONE", away: "VERONA"}, {home: "JUVENTUS", away: "ROMA"}, {home: "LAZIO", away: "BOLOGNA"},
                {home: "NAPOLI", away: "MONZA"}, {home: "PARMA", away: "MILAN"}, {home: "SASSUOLO", away: "LECCE"}, {home: "TORINO", away: "GENOA"}
            ],
            35: [
                {home: "BOLOGNA", away: "PARMA"}, {home: "GENOA", away: "FROSINONE"}, {home: "INTER", away: "ATALANTA"},
                {home: "LECCE", away: "TORINO"}, {home: "MILAN", away: "VENEZIA"}, {home: "ROMA", away: "LAZIO"},
                {home: "UDINESE", away: "JUVENTUS"}, {home: "VERONA", away: "SASSUOLO"}, {home: "MONZA", away: "CAGLIARI"}, {home: "COMO", away: "NAPOLI"}
            ],
            36: [
                {home: "ATALANTA", away: "MILAN"}, {home: "CAGLIARI", away: "NAPOLI"}, {home: "FROSINONE", away: "INTER"},
                {home: "JUVENTUS", away: "MONZA"}, {home: "LAZIO", away: "FIORENTINA"}, {home: "PARMA", away: "ROMA"},
                {home: "SASSUOLO", away: "BOLOGNA"}, {home: "TORINO", away: "VERONA"}, {home: "UDINESE", away: "GENOA"}, {home: "VENEZIA", away: "LECCE"}
            ],
            37: [
                {home: "BOLOGNA", away: "UDINESE"}, {home: "COMO", away: "ATALANTA"}, {home: "GENOA", away: "TORINO"},
                {home: "INTER", away: "VERONA"}, {home: "LECCE", away: "FROSINONE"}, {home: "MILAN", away: "MONZA"},
                {home: "NAPOLI", away: "JUVENTUS"}, {home: "ROMA", away: "CAGLIARI"}, {home: "SASSUOLO", away: "LAZIO"}, {home: "VENEZIA", away: "PARMA"}
            ],
            38: [
                {home: "ATALANTA", away: "COMO"}, {home: "CAGLIARI", away: "MILAN"}, {home: "FROSINONE", away: "LECCE"},
                {home: "JUVENTUS", away: "INTER"}, {home: "LAZIO", away: "ROMA"}, {home: "PARMA", away: "BOLOGNA"},
                {home: "SASSUOLO", away: "GENOA"}, {home: "TORINO", away: "NAPOLI"}, {home: "UDINESE", away: "MONZA"}, {home: "VERONA", away: "VENEZIA"}
            ]
        };

        function initDashboard() {
            const giornataSelect = document.getElementById('giornataSelect');
            if (giornataSelect && giornataSelect.options.length === 0) {
                for (let i = 1; i <= 38; i++) {
                    const opt = document.createElement('option');
                    opt.value = i;
                    opt.textContent = `${i}ª Giornata`;
                    if (i === 12) opt.selected = true;
                    giornataSelect.appendChild(opt);
                }
            }

            const teamSelect = document.getElementById('teamSelect');
            const opponentSelect = document.getElementById('opponentSelect');
            
            if (teamSelect && teamSelect.options.length === 0) {
                Object.keys(leagueData).forEach(team => {
                    const opt1 = document.createElement('option');
                    opt1.value = team; opt1.textContent = team;
                    teamSelect.appendChild(opt1);
                });
            }

            if (opponentSelect && opponentSelect.options.length === 0) {
                Object.keys(leagueData).forEach(team => {
                    if (team !== "CASCINA") {
                        const opt2 = document.createElement('option');
                        opt2.value = team; opt2.textContent = team;
                        opponentSelect.appendChild(opt2);
                    }
                });
            }

            initCustomLineupSelectors();
            updateAll();
        }

        function updateAll() {
            renderTeam();
            renderMatchup();
            renderRecommendedLineup();
            updateCustomLineupStats();
        }

        function getMatchDetails(p, giornata) {
            if (!p || !p.squadra) return { avversario: "-", isHome: false };
            let squadraKey = p.squadra.toUpperCase().trim();
            if (squadraKey === "JUVE") squadraKey = "JUVENTUS";
            if (squadraKey === "SASSLUOLO") squadraKey = "SASSUOLO";
            if (squadraKey === "FROSINORE") squadraKey = "FROSINONE";
            
            const partiteGiornata = calendarioUfficiale[giornata] || [];
            for (let match of partiteGiornata) {
                if (match.home === squadraKey) return { avversario: match.away, isHome: true };
                if (match.away === squadraKey) return { avversario: match.home, isHome: false };
            }
            return { avversario: "-", isHome: false };
        }

        // Generazione dinamica dei menu in base al modulo selezionato (3-5-2, 4-3-3, ecc.)
        function initCustomLineupSelectors() {
            const container = document.getElementById('customLineupSelectors');
            const moduloVal = document.getElementById('moduloSelect').value;
            if (!container) return;
            container.innerHTML = '';

            const parts = moduloVal.split('-');
            const difCount = parseInt(parts[0]);
            const cenCount = parseInt(parts[1]);
            const attCount = parseInt(parts[2]);

            const cascina = leagueData["CASCINA"];
            
            let slots = [
                {type: 'POR', count: 1, list: cascina.por},
                {type: 'DIF', count: difCount, list: cascina.dif},
                {type: 'CEN', count: cenCount, list: cascina.cen},
                {type: 'ATT', count: attCount, list: cascina.att}
            ];

            slots.forEach(slot => {
                for (let i = 1; i <= slot.count; i++) {
                    const div = document.createElement('div');
                    div.className = "bg-slate-900 p-2 rounded border border-slate-700 space-y-1";
                    
                    const label = document.createElement('label');
                    label.className = "text-[11px] font-bold text-slate-400 block uppercase";
                    label.textContent = `${slot.type} #${i}`;
                    
                    const select = document.createElement('select');
                    select.className = "custom-player-select w-full bg-slate-800 text-white text-xs p-1.5 rounded border border-slate-600 focus:outline-none focus:ring-1 focus:ring-emerald-500";
                    select.dataset.role = slot.type;
                    select.onchange = updateCustomLineupStats;

                    const emptyOpt = document.createElement('option');
                    emptyOpt.value = "";
                    emptyOpt.textContent = "-- Seleziona --";
                    select.appendChild(emptyOpt);

                    slot.list.forEach((p, idx) => {
                        const opt = document.createElement('option');
                        opt.value = p.name;
                        opt.textContent = `${p.name} (${p.squadra})`;
                        // Seleziona i primi disponibili per default fino a riempire il modulo
                        if (idx < slot.count && i === idx + 1) opt.selected = true;
                        select.appendChild(opt);
                    });

                    div.appendChild(label);
                    div.appendChild(select);
                    container.appendChild(div);
                }
            });

            updateCustomLineupStats();
        }

        function updateCustomLineupStats() {
            const selects = document.querySelectorAll('.custom-player-select');
            const giornata = document.getElementById('giornataSelect').value || 12;
            const cascina = leagueData["CASCINA"];
            
            let selectedPlayers = [];
            
            selects.forEach(sel => {
                const name = sel.value;
                const role = sel.dataset.role;
                if (!name) return;
                
                let roleKey = role.toLowerCase() === 'por' ? 'por' : role.toLowerCase() === 'dif' ? 'dif' : role.toLowerCase() === 'cen' ? 'cen' : 'att';
                let playerObj = (cascina[roleKey] || []).find(p => p.name === name);
                
                if (playerObj) {
                    const match = getMatchDetails(playerObj, giornata);
                    selectedPlayers.push({
                        role,
                        name: playerObj.name,
                        squadra: playerObj.squadra,
                        mv: playerObj.mv,
                        fm: playerObj.fm,
                        avversario: match.avversario,
                        isHome: match.isHome
                    });
                }
            });

            const stats = calculateAverages(selectedPlayers);
            const statsEl = document.getElementById('customLineupStats');
            if (statsEl) {
                statsEl.textContent = `Titolari schierati: ${selectedPlayers.length}/11 | Media Voto: ${stats.mv} | Fantamedia: ${stats.fm}`;
            }
        }

        function getBest11(teamKey, giornata) {
            const team = leagueData[teamKey];
            if (!team) return [];
            
            const normalize = (p, role) => {
                const match = getMatchDetails(p, giornata);
                return {
                    role, name: p.name, squadra: p.squadra || "N/D", mv: p.mv || 6.0, fm: p.fm || 6.0, avversario: match.avversario, isHome: match.isHome
                };
            };

            const porList = (team.por || []).map(p => normalize(p, 'POR'));
            const difList = (team.dif || []).map(p => normalize(p, 'DIF')).sort((a,b) => b.fm - a.fm).slice(0, 4);
            const cenList = (team.cen || []).map(p => normalize(p, 'CEN')).sort((a,b) => b.fm - a.fm).slice(0, 3);
            const attList = (team.att || []).map(p => normalize(p, 'ATT')).sort((a,b) => b.fm - a.fm).slice(0, 3);

            return [porList[0], ...difList, ...cenList, ...attList].filter(Boolean);
        }

        function calculateAverages(lineup) {
            if (lineup.length === 0) return { mv: "0.00", fm: "0.00" };
            let totalMv = lineup.reduce((acc, p) => acc + Number(p.mv), 0);
            let totalFm = lineup.reduce((acc, p) => acc + Number(p.fm), 0);
            return {
                mv: (totalMv / lineup.length).toFixed(2),
                fm: (totalFm / lineup.length).toFixed(2)
            };
        }

        function renderTeam() {
            const giornataEl = document.getElementById('giornataSelect');
            const teamEl = document.getElementById('teamSelect');
            if (!giornataEl || !teamEl) return;

            const giornata = giornataEl.value || 12;
            const teamName = teamEl.value || "CASCINA";
            const team = leagueData[teamName];
            if (!team) return;
            
            const teamTitleEl = document.getElementById('teamTitle');
            if (teamTitleEl) teamTitleEl.textContent = `Rosa Completa: ${teamName}`;

            const tbody = document.getElementById('rosterTable');
            if (!tbody) return;
            tbody.innerHTML = '';

            const categories = [
                { role: 'POR', list: team.por || [], color: 'text-amber-400 font-bold' },
                { role: 'DIF', list: team.dif || [], color: 'text-blue-400 font-bold' },
                { role: 'CEN', list: team.cen || [], color: 'text-emerald-400 font-bold' },
                { role: 'ATT', list: team.att || [], color: 'text-rose-400 font-bold' }
            ];

            categories.forEach(cat => {
                cat.list.forEach(p => {
                    const squadra = p.squadra || "N/D";
                    const match = getMatchDetails(p, giornata);
                    const homeAwayBadge = match.isHome ? '<span class="text-emerald-400 font-bold" title="In Casa">🏠 Casa</span>' : '<span class="text-amber-400 font-bold" title="Fuori Casa">✈️ Fuori</span>';
                    
                    const tr = document.createElement('tr');
                    tr.className = "hover:bg-slate-700/50 transition";
                    tr.innerHTML = `
                        <td class="p-3 ${cat.color}">${cat.role}</td>
                        <td class="p-3 font-semibold text-slate-200">${p.name}</td>
                        <td class="p-3 text-xs"><span class="text-slate-300 font-medium">${squadra}</span> <span class="text-slate-500 mx-1">→</span> ${homeAwayBadge} vs <span class="text-amber-300 font-semibold">${match.avversario}</span></td>
                        <td class="p-3 text-center text-slate-300 font-mono">${Number(p.mv).toFixed(2)}</td>
                        <td class="p-3 text-center text-emerald-400 font-mono font-bold">${Number(p.fm).toFixed(2)}</td>
                    `;
                    tbody.appendChild(tr);
                });
            });
        }

        function renderMatchup() {
            const giornataEl = document.getElementById('giornataSelect');
            const oppEl = document.getElementById('opponentSelect');
            if (!giornataEl || !oppEl) return;

            const giornata = giornataEl.value || 12;
            const oppName = oppEl.value || Object.keys(leagueData).find(t => t !== "CASCINA");
            
            const oppTitleEl = document.getElementById('opponentMatchupTitle');
            if (oppTitleEl) oppTitleEl.textContent = `⚔️ ${oppName}`;

            const cascinaLineup = getBest11("CASCINA", giornata);
            const opponentLineup = getBest11(oppName, giornata);

            const cAvg = calculateAverages(cascinaLineup);
            const oAvg = calculateAverages(opponentLineup);

            const cAvgEl = document.getElementById('cascinaAverages');
            const oAvgEl = document.getElementById('opponentAverages');
            if (cAvgEl) cAvgEl.textContent = `Media Voto: ${cAvg.mv} | Fantamedia: ${cAvg.fm}`;
            if (oAvgEl) oAvgEl.textContent = `Media Voto: ${oAvg.mv} | Fantamedia: ${oAvg.fm}`;

            const renderLineupList = (containerId, lineup) => {
                const container = document.getElementById(containerId);
                if (!container) return;
                container.innerHTML = '';
                lineup.forEach(p => {
                    const homeAwayText = p.isHome ? '🏠 Casa' : '✈️ Fuori';
                    const div = document.createElement('div');
                    div.className = "flex justify-between items-center bg-slate-800 p-2 rounded border border-slate-700 text-xs gap-2";
                    div.innerHTML = `
                        <div class="flex items-center gap-2 overflow-hidden flex-wrap">
                            <span class="font-bold px-1.5 py-0.5 rounded bg-slate-900 shrink-0 ${
                                p.role === 'POR' ? 'text-amber-400' : p.role === 'DIF' ? 'text-blue-400' : p.role === 'CEN' ? 'text-emerald-400' : 'text-rose-400'
                            }">${p.role}</span>
                            <span class="font-semibold text-slate-200">${p.name}</span>
                            <span class="text-slate-400 text-[10px]">(${p.squadra})</span>
                            <span class="text-amber-300 text-[10px] bg-amber-500/10 px-1.5 py-0.5 rounded border border-amber-500/20">${homeAwayText} vs ${p.avversario}</span>
                        </div>
                        <div class="flex gap-2 font-mono text-[11px] shrink-0">
                            <span class="text-slate-300">MV: <b>${Number(p.mv).toFixed(2)}</b></span>
                            <span class="text-emerald-400">FM: <b>${Number(p.fm).toFixed(2)}</b></span>
                        </div>
                    `;
                    container.appendChild(div);
                });
            };

            renderLineupList('cascinaMatchupLineup', cascinaLineup);
            renderLineupList('opponentMatchupLineup', opponentLineup);
        }

        function renderRecommendedLineup() {
            const giornataEl = document.getElementById('giornataSelect');
            if (!giornataEl) return;
            const giornata = giornataEl.value || 12;
            const best11 = getBest11("CASCINA", giornata);
            const container = document.getElementById('recommendedLineup');
            if (!container) return;
            container.innerHTML = '';

            best11.forEach(p => {
                const homeAwayText = p.isHome ? '🏠 Casa' : '✈️ Fuori';
                const card = document.createElement('div');
                card.className = "bg-slate-900 p-3 rounded-lg border border-slate-700 space-y-1";
                card.innerHTML = `
                    <div class="flex justify-between items-center">
                        <span class="text-xs font-bold px-2 py-0.5 rounded bg-slate-800 ${
                            p.role === 'POR' ? 'text-amber-400' : p.role === 'DIF' ? 'text-blue-400' : p.role === 'CEN' ? 'text-emerald-400' : 'text-rose-400'
                        }">${p.role}</span>
                        <span class="text-[11px] text-amber-300">${homeAwayText} vs <b>${p.avversario}</b></span>
                    </div>
                    <div class="font-bold text-slate-100 text-sm pt-1">${p.name} <span class="text-xs text-slate-400 font-normal">(${p.squadra})</span></div>
                    <div class="flex justify-between text-xs pt-1 border-t border-slate-800">
                        <span class="text-slate-400">MV: ${Number(p.mv).toFixed(2)}</span>
                        <span class="text-emerald-400 font-bold">FM: ${Number(p.fm).toFixed(2)}</span>
                    </div>
                `;
                container.appendChild(card);
            });
        }

        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initDashboard);
        } else {
            initDashboard();
        }
    </script>
</body>
</html>
