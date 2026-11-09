CELLULARENA (Winter Challenge 2024) - JOUER EN LOCAL
=====================================================

Dossier : cellularenaWinterChallenge2024/
  bot.py        ton bot (Python 3, règles Wood : ROOT, BASIC, HARVESTER)
  bot_concours.py  ton agent du concours (version envoyée, ajoutée telle quelle)
  run-referee.sh  referee officiel + visualiseur (voir 0)
  sim.py        simulateur maison, SANS referee officiel (approximation des règles Wood)
  statement.md, stub.txt   énoncé et squelette d'entrée
  replays/boss/ parties jouées contre les agents CodinGame (voir 3)

0) Referee OFFICIEL + visualiseur graphique (vendor/referee = CodinGame/WinterChallenge2024-Cellularena)
   ./run-referee.sh view  [bot0.py] [bot1.py] [seed=1] [niveau=5] [port=8888]   -> http://localhost:8888/test.html
   ./run-referee.sh batch [bot0.py] [bot1.py] [seed] [niveau]                   -> RESULT seed=.. scores={0=..,1=..}
   - niveau de ligue 1..5 (5 = règles complètes ; les niveaux bas = règles Wood) ; défaut bot.py contre bot.py
   - le 1er lancement compile le referee (Maven partagé) et la vue TypeScript (npm install + npx tsc)
   - le boss de config/Boss.py est "redacted" dans le dépôt officiel : pas de code adverse, il faut deux de tes bots
   - dans la fenêtre : "Standard Output"/"Standard Error" de chaque joueur affichent ses coups tour par tour

1) Simulateur local maison (bot contre bot, sans interface graphique)
   python3 sim.py [--seed N] [--games N] [--turns 100] [--p0 "python3 bot.py"] [--p1 "python3 bot.py"] [-v]
   - défaut : bot.py contre bot.py, seed 1, 1 partie ; -v affiche les coups de chaque tour
   - score = nombre d'organes à la fin ; affiche "p0 wins / p1 wins / draws"
   - exemple : python3 sim.py --games 20 --p0 "python3 bot.py" --p1 "python3 autre_bot.py"
   - stderr des bots masqué (visible avec -v)
   - limite : ce n'est pas le vrai referee, les résultats ne valent pas ceux de CodinGame

2) Tester une entrée à la main
   Le protocole est celui de stub.txt : largeur/hauteur, puis à chaque tour la liste des entités.
   python3 bot.py < entree.txt

3) Jouer contre les agents CodinGame (adversaires distants, code non récupérable)
   Les agents ne sont jouables que par l'API (puzzle "winter-challenge-2024", ligue Wood 3) :
     BOSS 2  agent_id 5736695      B4R0N  agent_id 6047938
   python3 ../common/cg_test_games.py winter-challenge-2024 bot.py --opp 5736695 --opp 6047938 --count 5 --out replays/boss
   - token : ~/.config/codingame/token (jamais commité) ; une partie à la fois, 10 par minute max
   - archive replays/boss/<agent>_<partie>.json et .log (coups de l'adversaire dans "stdout")
   - le JSON se convertit au format log commun : python3 ../common/json_to_log.py replays/boss/*.json
   - liste actuelle des adversaires : curl avec le token sur /api/v1/puzzles/winter-challenge-2024/opponents
   - archivé : 5736695_919124769 (défaite 16-17), 6047938_919124815 (victoire 16-9)

Voir aussi : ../README.md (outils partagés), ../tryangle-catch/readme.txt
