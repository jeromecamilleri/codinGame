# Passation — agent CodinGame Fall Challenge 2026

Dernière mise à jour : 8 novembre 2026. Ce document permet à un nouvel agent de reprendre le
travail dans `/dataSSD/travailJerome/codingame` sans refaire les vérifications déjà effectuées.

## But du travail

Améliorer un agent pour **Fall Challenge 2026**, jeu **TryAngle Catch**, puis le comparer au
referee et à des bots antérieurs. L'utilisateur veut des changements mesurés :

> Ne créer une nouvelle version permanente de bot que si elle bat les versions précédentes.

Les idées en cours restent des candidats temporaires (par exemple sous `/tmp`). Un candidat ne
devient `bot_vN.py` qu'après une comparaison reproductible contre chaque version de référence.
Comparer les mêmes graines, inverser les sièges et vérifier qu'aucune action n'est rejetée.
Les résultats locaux doivent être présentés comme un échantillon, pas comme une garantie de
classement CodinGame.

L'utilisateur préfère des réponses franches, des faits vérifiés et, quand c'est possible, une
double vérification indépendante. Il échange en français.
Les tokens et le modèle de l'agent IA influent sur l'aide au développement, pas directement sur
le score CodinGame : le juge évalue le programme soumis.

## Jeu et règles utiles

- Les points viennent des triangles contrôlés, à raison d'un point par triangle et par tour.
- Les unités servent à prendre et défendre les maisons et donc les triangles ; leur nombre seul
  ne détermine pas le gagnant.
- Les règles Bronze activent les actions avancées, dont la création de chemins.
- Le referee fixe le maximum à 200 tours et peut mettre fin plus tôt à la partie si un joueur ne
  peut plus marquer ou a perdu ses unités et triangles.
- Le code du referee se trouve dans `vendor/TryAngle-Catch/`. Il est construit localement par
  `scripts/build-local-referee.sh`.

## Fichiers et versions

- `bot.py` : première heuristique, planifie des captures et peut créer des chemins.
- `bot_simple.py` : approche plus directe vers l'adversaire, bot historique déjà comparé.
- `bot_v3_capture_spawn.py` : v3 conservée intacte ; vise les triangles presque capturés et
  recrute avec des triangles en surplus.
- `bot_v4_capture_spawn.py` : version actuelle la plus forte parmi les versions locales testées.
- `bot_v5_no_reversal.py` : v4 sans retour immédiat sur le trajet précédent ; bat v4, v3,
  `bot.py` et `bot_simple.py` en local (voir `BOT_HISTORY.md`). Version la plus forte actuelle.
  `run-head-to-head.sh BOT_A BOT_B [graine] [nombre]` compare deux bots, sièges inversés.
- `bot_v6_cycle_guard.py` : v5 + blocage des cycles de 2-3 maisons + repli `WAIT` en cas d'erreur.
  Pas de gain de force prouvé contre v5 (124 / 114 / 82 sur 320 parties) ; sert de base robuste.
  Les replays 918756754 (timeout) et 918757432 (cycles de 3) l'ont motivée.
- `BOT_HISTORY.md` : historique et résultats déjà validés.

V4 reprend v3 avec quatre différences consignées dans `BOT_HISTORY.md` : priorité plus forte aux
triangles proches de la capture, jusqu'à trois déplacements distincts par tour, recrutement
ajusté au nombre d'unités et mémorisation des chemins calculés pendant le tour.

Lors du dernier contrôle authentifié, le code renvoyé par l'API de la compétition correspondait
exactement au fichier local `bot_v4_capture_spawn.py`. Aucun code n'a été soumis ou modifié en
ligne pendant les derniers essais. Selon l'utilisateur, tous les replays archivés ont été joués le 8 novembre 2026 avec la v4 contre
Baron Bosswell (code inconnu) ; les replays n'ont toutefois pas d'identifiant de soumission pour le prouver.

## Comparaisons locales déjà faites

Les matchs utilisent le referee local Bronze, les conditions standard du concours : une unité
sur chacune des trois maisons de départ (3 unités au total par joueur), zéro triangle bonus.
Chaque duel a été joué sur cinq graines avec les sièges inversés, soit dix parties par adversaire.

| Duel | Victoires / défaites / nulles |
|---|---:|
| v3 contre `bot_simple.py` | 2 / 6 / 2 |
| v3 contre `bot.py` | 4 / 6 / 0 |
| v4 contre `bot_simple.py` | 8 / 1 / 1 |
| v4 contre `bot.py` | 6 / 4 / 0 |

Les 30 matchs de validation finale de v4 n'ont signalé aucune action rejetée. Les résultats
détaillés sont dans `benchmarks/2026-11-08-local-bronze.tsv` et
`benchmarks/2026-11-08-v4-winning-bronze.tsv`. Le test porte sur cinq cartes distinctes ; il
reste utile d'élargir l'échantillon avant de parler de force générale.

## Lancer et comparer

Depuis la racine du workspace :

```sh
# Visualiser v4 contre bot_simple avec le départ standard
./run-local-match.sh 20261108 bot_v4_capture_spawn.py bot_simple.py 1 0

# Refaire le tournoi comparatif
./run-bot-benchmark.sh
```

`run-local-match.sh` démarre par défaut avec 3 unités sur chacune des trois maisons de départ
(9 par joueur) et 3 triangles bonus par joueur. Ces valeurs ne sont pas le départ standard du
concours ; fournir les arguments `1 0` pour 3 unités totales et aucun bonus.

## Replays en ligne archivés

Quatre journaux texte sont stockés sous `replays/raw/` :

- `918739641.log`
- `918740399.log`
- `918740963.log`
- `918741122.log`

`scripts/import_replay_history.py` les transforme en `replays/replay_history.jsonl`. Pour
reconstruire l'index après ajout d'autres `.log` :

```sh
python3 scripts/import_replay_history.py
```

Le replay JSON `replays/raw/918741865.json` (données brutes de l'API) est converti en
`918741865.log` au même format que les autres par `scripts/json_to_log.py`, puis indexé par
`import_replay_history.py` et utilisable par `run-vs-replay.sh`. Pour ajouter un replay JSON :

```sh
python3 scripts/json_to_log.py && python3 scripts/import_replay_history.py
```

Analyse mise à jour dans `replays/ANALYSE.md` : sur les quatre journaux texte, Baron capture en
premier aux frames 3 ou 7 ; `jejecam` ne capture rien dans trois parties et attend la frame 77
dans l'autre. Le replay JSON 918741865 nuance ce constat : les deux joueurs capturent en frame 3,
mais Baron finit tout de même avec 36 triangles et 31 renforts contre 8 triangles et 3 renforts
pour `jejecam`. Sur l'ensemble des cinq parties, le recrutement de `jejecam` reste de zéro à trois
unités, contre 18 à 43 pour Baron. L'indice principal est donc la difficulté à maintenir
l'expansion et les renforts ; la course à la première capture n'explique pas toutes les défaites.

Pour rejouer les commandes historiques du joueur 1 (Baron Bosswell) comme adversaire local :

```sh
./run-vs-replay.sh 918739641 bot_v4_capture_spawn.py
```

`scripts/replay_agent.py` reproduit les commandes enregistrées sans réagir au nouvel état. Ce
n'est pas un replay adaptatif : la partie peut diverger dès que le bot testé change le cours du
jeu. Le test v4 contre les actions du replay `918739641`, avec la même graine et le départ
standard, a reproduit le score final **-1 / 123**.

Les logs n'enregistrent pas l'observation fournie au bot, mais elle se **reconstitue** : le referee
est déterministe, donc rejouer les commandes des deux sièges avec la même graine redonne toutes
les observations. `scripts/reconstruct_states.sh <id>...` les écrit dans
`replays/states/<id>/seat{0,1}.txt` (voir `replays/README.md` pour le format), et
`python3 scripts/analyze_states.py` en tire des statistiques par joueur. Sur 8 des 9 parties le
score rejoué est identique à l'original ; le 918756754 (timeout) n'est valide que jusqu'au
timeout. Constats détaillés : `replays/PROFIL_BARON.md`. Des paires « état → action » complètes
sont donc disponibles pour les deux joueurs, Baron compris.

## Pistes de travail

1. Exploiter `replays/PROFIL_BARON.md` : Baron recrute à chaque tour où il tient un triangle ;
   tester un recrutement plus systématique (voir les pistes de ce fichier).
2. Corriger les détours/oscillations de v4 qui ressortent des journaux, puis mesurer un candidat
   temporaire contre `bot.py`, `bot_simple.py` et les replays fixes.
3. Garder v3/v4 intactes. N'ajouter `bot_v5.py` qu'après qu'un candidat temporaire batte les
   deux versions de référence sur le même protocole et sans erreurs d'action.

## Détails d'environnement

- Challenge public id : `fall-challenge-2026`.
- API de lecture des parties : `GET /api/v1/games/<game_id>` ; les quatre logs texte archivés
  ont été téléchargés à partir de là.
- Le referee local est adapté pour lire `startingUnits` et `startingTriangles`. Le lanceur
  interactif utilise des valeurs par défaut de démonstration (9 unités et 3 triangles bonus
  par joueur) ; les comparaisons normalisées passent explicitement `1 0`.
- Les clés/tokens ne doivent pas être copiés dans ce document, les logs, ni le dépôt.
