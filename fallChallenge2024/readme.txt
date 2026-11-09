SELENIA CITY (Fall Challenge 2024) - JOUER EN LOCAL
===================================================

Dossier : fallChallenge2024/
  bot_v1.py     bot de base (tubes sans croisement + un pod aller-retour par tube)
  bot_wait.py   bot qui ne fait que WAIT (score 0, test du dispositif)
  results_v1.txt  scores locaux de bot_v1 sur les 24 tests
  statement.md, puzzle.json   énoncé et métadonnées du puzzle (API CodinGame)
  vendor/referee   referee officiel (git clone de CodinGame/FallChallenge2024-SeleniaCity, ignoré par git)
  run-local.sh, run-view.sh   lanceurs (utilisent ../common/)

Jeu solo (optimisation) : pas d'adversaire, donc aucun agent CodinGame à rejouer.
Le score est celui du referee ("points"). Le comparer d'une version à l'autre sur les mêmes tests.

1) Scores locaux (referee officiel, 24 tests = config/test1..24.json)
   ./run-local.sh                    # bot_v1.py sur les 24 tests
   ./run-local.sh bot_v1.py 1 5 10   # bot et tests choisis
   - sortie : RESULT <test> score={"points":"..."} ; WARN = action refusée par le referee
   - ERR = stderr du bot ; limite du jeu : 500 ms par tour (1000 ms au premier)
   - premier lancement : compile le referee avec le Maven partagé (../.tools, ../common/setup-tools.sh)

2) Visualiseur local
   ./run-view.sh [bot.py] [N] [port]   puis http://localhost:8888/test.html
   - la vue du referee est en TypeScript : au premier lancement le script fait, dans
     vendor/referee/src/main/resources, "npm install" puis "npx tsc" (génère view/graphics/*.js ;
     node_modules/ et vendor/ sont ignorés par git). Node/npm requis. Sans cela : 404 sur ViewModule.js.
   - le script ne rend pas la main (Ctrl+C pour arrêter)

3) Test games sur CodinGame (vrai moteur, vue dans l'IDE) - un test à la fois, 30 par minute max
   API=https://www.codingame.com/api/v1
   jq -n --rawfile code bot_v1.py '{language:"Python3",code:$code,testcase:1}' \
     | curl -s -X POST -H "Authorization: Bearer $(cat ~/.config/codingame/token)" \
       -H 'Content-Type: application/json' --data-binary @- "$API/puzzles/selenia-city/test-games?wait=30"
   - testcase = numéro du test dans puzzle.json ; le token ne doit jamais être affiché ni commité
   - la soumission (POST .../submissions) est faite seulement quand une version s'améliore

4) Mettre à jour l'énoncé / les infos du puzzle
   python3 ../common/cg_api.py puzzle selenia-city --out .

Voir aussi : ../README.md (outils partagés), ../tryangle-catch/readme.txt, ../cellularenaWinterChallenge2024/readme.txt
