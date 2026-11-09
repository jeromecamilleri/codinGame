# Historique des bots TryAngle Catch

- `bot.py` — première version heuristique, planifie les triangles et peut créer des chemins.
- `bot_simple.py` — version axée sur des déplacements prudents vers l'adversaire.
- `bot_v3_capture_spawn.py` — version expérimentale : cible explicitement les triangles
  presque capturés et dépense les triangles en surplus pour renforcer l'armée.
- `bot_v4_capture_spawn.py` — v3 ajustée pour éviter les détours et déplacer jusqu'à trois
  unités par tour sur des trajets distincts ; la v3 reste conservée.

Les anciennes versions sont conservées telles quelles pour que les comparaisons restent
reproductibles. Les matchs comparatifs utilisent les règles Bronze, 1 unité sur chacune
des trois maisons de départ (3 unités par joueur) et aucun triangle bonus.

## Comparaison locale du 8 novembre 2026

`run-bot-benchmark.sh` a joué 5 graines, chaque bot dans les deux sièges, soit 10 parties
par duel. Résultats par victoires/défaites/nuls :

- v3 contre `bot_simple.py` : 2 / 6 / 2.
- v3 contre `bot.py` : 4 / 6 / 0.
- `bot_simple.py` contre `bot.py` : 8 / 2 / 0.

La v3 n'est donc pas meilleure sur cet échantillon. C'est un petit tournoi local, pas une
mesure du classement CodinGame; les résultats peuvent dépendre des graines et de la version
du referee. Les scores détaillés se trouvent dans `benchmarks/2026-11-08-local-bronze.tsv`.

## Comparaison locale de la v4

La même série de 5 graines, avec les deux sièges inversés (10 parties par adversaire), donne :

- v4 contre `bot_simple.py` : 8 victoires / 1 défaite / 1 nul.
- v4 contre `bot.py` : 6 victoires / 4 défaites / 0 nul.

Les 30 matchs n'ont signalé aucune action rejetée. La v4 gagne donc contre chacune des deux
versions sur cette série, sans garantir un meilleur classement général. Les scores sont dans
`benchmarks/2026-11-08-v4-winning-bronze.tsv`.

## Différences entre v3 et v4

- **Triangles visés :** v3 donne la priorité 100 aux triangles dont deux sommets sont déjà à
  nous, 35 à ceux dont un sommet est à nous, et 5 aux triangles sans sommet à nous. En v4, ces
  priorités deviennent 100, 20 et 0. La v4 insiste donc sur les captures proches et poursuit
  beaucoup moins un triangle encore éloigné.
- **Déplacements :** v3 choisit au plus un déplacement par tour. V4 peut en choisir jusqu'à
  trois, en recalculant la situation après chacun. Elle réserve les maisons de départ et
  d'arrivée déjà utilisées pour éviter que ses propres ordres se gênent.
- **Renforts :** v3 dépense un triangle pour recruter si elle a moins de 8 unités et plus d'un
  triangle utilisable. V4 vise moins de 6 unités ; elle peut aussi dépenser son dernier triangle
  si elle tombe sous 4 unités. Cela accélère le recrutement quand son armée est très faible,
  tout en gardant un plafond plus bas.
- **Calcul des trajets :** v4 mémorise les chemins calculés pendant le tour pour éviter de
  refaire les mêmes recherches. Cela ne change pas la décision, seulement le travail de calcul.

Le reste de la stratégie de capture et le déplacement de secours vers l'adversaire viennent de
la v3. Sur les mêmes 5 graines et avec les sièges inversés, v3 avait fait 2 victoires, 6
défaites et 2 nulles contre `bot_simple.py`, puis 4 victoires et 6 défaites contre `bot.py`.
La v4 a obtenu respectivement 8 victoires, 1 défaite et 1 nulle, puis 6 victoires et
4 défaites. Ces résultats sont locaux et ne garantissent pas le même bilan sur d'autres cartes.

## Replay CodinGame enregistré

- Replay [918741865](https://www.codingame.com/replay/918741865), sauvegardé dans
  `replays/raw/918741865.json` (données brutes de l'API CodinGame, y compris le referee input).
- Joueur 0 : `jejecam`, contre Baron Bosswell (boss d'arène, joueur 1). Le bot soumis
  n'est pas identifié par le replay.
- Résultat : défaite au tour 179, `$0 no units or triangles left!` (scores -1 contre 71,
  rangs 1 / 0). Les deux camps ont capturé et recruté au début ; ensuite le boss a
  capturé et recruté presque seul, jusqu'à l'élimination totale de `jejecam`.
- Piste : le bot perd ses unités sans les renforcer (plusieurs « surrounded »), donc
  la priorité est la survie/recrutement dans la phase mi-partie.

## v5 (`bot_v5_no_reversal.py`)

v4 avec un seul changement : une unité ne peut pas repartir sur le trajet inverse d'un
déplacement fait au tour précédent (`A→B` puis `B→A`), ce qui coupe les allers-retours vus dans
les replays contre Baron Bosswell. Le reste est identique à v4.

Résultats locaux (`run-head-to-head.sh`, départ standard, sièges inversés, aucune action
rejetée), victoires / défaites / nulles de la v5 :

- contre v4 : 10 graines 11 / 2 / 7, puis 40 autres graines (80 parties) 39 / 21 / 20.
- contre v3 : 20 graines (40 parties) 20 / 9 / 11.
- contre `bot_simple.py` : 30 / 10 / 0 sur 40 parties.
- contre `bot.py` : 34 / 6 / 0 sur 40 parties.

Essai écarté : relever le plafond de recrutement de 6 à 10 unités donnait 37 / 26 / 17 contre
v4 (80 parties), moins bon que la v5 retenue. Ces résultats sont locaux et ne mesurent pas le
classement CodinGame ni la force contre Baron Bosswell.

## v6 (`bot_v6_cycle_guard.py`)

Issue des replays 918756754 (timeout de la soumission) et 918757432 (nul 0 / 0 avec trois
cycles de 3 maisons). Changements par rapport à la v5 :

- **Cycles :** mémorise les déplacements des 3 derniers tours et interdit un déplacement
  qui refermerait un cycle de 2 ou 3 maisons (`A→B→A`, `A→B→C→A`).
- **Robustesse :** la lecture ignore les jetons non numériques au lieu d'arrêter le programme ;
  une erreur d'analyse ou de décision répond `WAIT` au lieu de planter ou de rester muet.
  La cause exacte du timeout du 918756754 n'est pas prouvée.

Résultats locaux (v6 en position A, départ standard, sièges inversés, 0 action rejetée) :
contre `bot.py` 34 / 5 / 1 et `bot_simple.py` 35 / 4 / 1 (40 parties chacun) ; contre v4
33 / 29 / 18 (80 parties) ; contre v5 124 / 114 / 82 sur 320 parties.
**La v6 ne bat donc pas nettement la v5 en local** (écart non significatif) : son intérêt est la
robustesse, pas un gain de force prouvé. La v5 n'est pas remplacée comme référence de force.
