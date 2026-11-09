TRYANGLE CATCH - LANCEMENT LOCAL (rapide)
==========================================

Prérequis : Java 9+, Python 3. Maven partagé : ../.tools (installé par ../common/setup-tools.sh).
Le premier lancement compile le referee dans vendor/TryAngle-Catch/target/.
Tout se lance depuis ce dossier (tryangle-catch/).

1) Partie avec visualiseur  (vérifié : http://localhost:8888/test.html s'ouvre)
   ./run-local-match.sh [seed] [bot0] [bot1] [unités] [triangles]
   - défauts : seed 20261108, bot_simple.py (bot0) contre bot.py (bot1), 3 unités et 3 triangles de départ
   - exemple : ./run-local-match.sh 20261108 bot_v6_cycle_guard.py bot_v4_capture_spawn.py 1 0
   - ouvrir ensuite http://localhost:8888/test.html ; le script ne rend pas la main (Ctrl+C pour arrêter)
   - ne pas l'utiliser pour des mesures en série : utiliser run-head-to-head.sh

2) Benchmark rapide contre bot_simple.py  (vérifié)
   ./run-bot-benchmark.sh [fichier_sortie.tsv] [seed ...]
   - bot testé : variable BOT_CANDIDATE (défaut bot_v4_capture_spawn.py)
   - seeds par défaut : 20261108 ... 20261112
   - sortie TSV (benchmarks/...) : seed, bot0, bot1, score0, score1, failure, summary
   - exemple : BOT_CANDIDATE=$PWD/bot_v6_cycle_guard.py ./run-bot-benchmark.sh benchmarks/v6.tsv 1 2 3

3) Comparer deux bots, deux sièges, départ standard du concours (1 unité, 0 triangle)
   ./run-head-to-head.sh BOT_A BOT_B [seed_départ=1000] [nombre=20]
   - affiche : A wins/losses/draws: V / D / N (failures: n)
   - exemple : ./run-head-to-head.sh bot_v6_cycle_guard.py bot_v5_no_reversal.py 1000 40

4) Rejouer un replay CodinGame contre son bot
   ./run-vs-replay.sh <game-id> <bot.py> [index-joueur-enregistré=1]

5) Replays, logs et analyses
   python3 ../common/cg_api.py replay <id> ...     télécharge replays/raw/<id>.json
   python3 scripts/json_to_log.py                  JSON -> .log
   python3 scripts/import_replay_history.py        reconstruit replays/replay_history.jsonl
   ./scripts/reconstruct_states.sh                 observations par tour (replays/states/)
   python3 scripts/analyze_states.py               statistiques (voir replays/PROFIL_BARON.md)

5b) Jouer contre un agent CodinGame (adversaire distant, code non récupérable)
   Puzzle "tryangle-catch" (ligue Wood 4) : BOSS 1 = agent_id 6795836.
   Baron Bosswell (6838062, boss Bronze du challenge) n'est plus jouable : challenge terminé.
   python3 ../common/cg_test_games.py tryangle-catch bot_v6_cycle_guard.py --opp 6795836 --count 5 --out replays/boss
   (une partie à la fois, 10 par minute ; les coups adverses sont dans le "stdout" des logs)

6) Tester un bot à la main
   python3 bot.py < tour.txt     (tour.txt = petit état synthétique de 4 maisons)

Bots : bot_simple.py, bot.py, bot_v3_capture_spawn.py, bot_v4_capture_spawn.py,
       bot_v5_no_reversal.py, bot_v6_cycle_guard.py   (historique : BOT_HISTORY.md)
Voir aussi : LOCAL.md, docs/CONTEXTE_AGENT_CODINGAME.md, ../README.md
