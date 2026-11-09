# TryAngle Catch en local

Le referee officiel et les scripts de lancement sont dans ce workspace. Le premier
lancement compile le referee et copie ses dépendances dans `vendor/TryAngle-Catch/target/`.
Maven est fourni dans `.tools/`; Python 3 et Java 9+ doivent être présents sur la machine.
Le lanceur ajoute l’ouverture de module requise par le Guice ancien du referee sur Java 17.

## Faire traiter l’exemple d’un tour

Depuis la racine du workspace :

```sh
python3 bot.py < tour.txt
```

`tour.txt` est un petit état synthétique de quatre maisons, destiné à illustrer le protocole
et le format d’une action. `tout.txt` est également fourni avec l’orthographe de la demande.
Ce sont des exemples d’entrée, pas des cartes complètes générées par le referee.

## Lancer une vraie partie locale

```sh
./run-local-match.sh
```

Le match utilise les règles Bronze, une carte déterministe et `bot_simple.py` contre `bot.py`
par défaut. Le premier avance prudemment vers l'adversaire ; le second cherche surtout à
capturer des triangles et à créer des chemins. Le lanceur interactif donne par défaut 3 unités
sur chacune des 3 maisons de départ (9 unités au total) et 3 triangles bonus à chaque joueur.
Pour simuler le départ normal du concours (1 unité sur chacune des 3 maisons, sans triangle
bonus), passe `1 0` à la fin de la commande :

```sh
./run-local-match.sh 123456 bot_simple.py bot.py 1 0
```

Pour voir la v4 contre l'ancienne heuristique avec ce départ standard :

```sh
./run-local-match.sh 20261108 bot_v4_capture_spawn.py bot.py 1 0
```

Pour rejouer le tournoi de comparaison (5 graines et inversion des deux sièges) :

```sh
./run-bot-benchmark.sh
```

Pour rejouer avec une autre graine :

```sh
./run-local-match.sh 123456
```

La forme générale est `./run-local-match.sh GRAINE BOT_ROUGE BOT_BLEU UNITÉS_PAR_MAISON TRIANGLES_BONUS`.
Par exemple, pour donner 3 unités par maison et 4 triangles bonus à chaque joueur :

```sh
./run-local-match.sh 123456 bot_simple.py bot.py 3 4
```

Pour lancer l'ancien agent heuristique `bot.py` contre lui-même :

```sh
./run-local-match.sh 20261108 bot.py
```

Le lanceur démarre le visualiseur local du referee. Pour comparer `bot.py` à un autre agent,
remplace le second chemin Python dans `run-local-match.sh`.

Le referee est le projet [eulerscheZahl/TryAngle-Catch](https://github.com/eulerscheZahl/TryAngle-Catch).
