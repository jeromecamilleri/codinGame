# Profil de Baron Bosswell (observations reconstituées)

Source : `scripts/analyze_states.py` sur les 9 parties de `replays/states/` (6 contre Baron,
3 contre d'autres joueurs). « t20 » = 20e observation du joueur. Les nombres sont des
corrélations observées, pas des preuves de cause.

## Constats chiffrés (6 parties contre Baron)

| | Baron | jejecam (v4/v5) |
|---|---:|---:|
| Premier recrutement (tour) | 1 à 3 | 1 dans 1 partie, 28 dans 1, **jamais** dans 4 |
| Recrues par partie | 19 à 43 | 0 à 3 |
| Unités au tour 20 | 11 à 20 (moy. 13,7) | 3 à 6 (moy. 3,5) |
| Unités au tour 40 | 18 à 38 (moy. 23,8) | 2 à 4 (moy. 2,8) |
| Maisons occupées au tour 20 | 8 à 15 | 2 à 4 |
| Tours où il détient un triangle et recrute | **89 %** (199 sur 224 ; 100 % dans 4 parties sur 6) | 7 % (6 sur 88) |

Règle du referee utile : `SPAWN` consomme le triangle (il ne rapporte plus de point et ne peut
être repris que lorsque le joueur a quitté ses trois sommets) mais ajoute une unité. Baron
transforme donc presque chaque capture (89 % des tours où il tient un triangle) en unité et fait grossir son armée d'environ +1 par tour
tout en l'étalant sur beaucoup de maisons (une seule unité par maison, pile maximale de 5).
Il émet une commande `MOVE` par unité (10 à 26 par tour, jamais de déplacement de plusieurs
unités à la fois). Nos bots émettent 2 à 3 commandes par tour.

## Deux défaillances distinctes de nos bots

1. **Ouverture :** dans 4 des 6 parties contre Baron, jejecam ne détient jamais un triangle
   au début d'un tour (aucune capture réussie) ; Baron capture dès les tours 0 à 3.
2. **Pas de recrutement quand on capture :** dans les 2 parties où jejecam détient un triangle
   (43 et 45 tours), il ne recrute que 3 fois. La v4/v5 ne recrute que s'il détient plus d'un
   triangle ou si l'armée est sous 4, avec un plafond de 6 unités.

Contre-exemple utile : 918757157 (victoire 1012 / -1 contre Keelhaul) montre un bot qui détient
un triangle 131 tours sur 136 en ne recrutant que 4 fois, mais Keelhaul n'a que 5 recrues, 3
maisons et 4,1 commandes par tour : détenir sans recruter marche contre un adversaire passif,
pas contre Baron.

## Précautions

- `moves/turn` de Baron compte toutes les commandes émises, y compris d'éventuels doublons ou
  ordres rejetés ; seuls nos propres logs listent les rejets avec certitude.
- Le recrutement systématique n'est pas prouvé meilleur : le test local « plafond 10 » était
  moins bon contre la v4, mais la v4 n'est pas Baron. Il faut un adversaire local imitant Baron.
- Timeout du 918756754 : les bots v4, v5 et v6 répondent en ~35 ms sur l'observation du tour du
  timeout, sans erreur ; la cause reste inconnue (probablement pas liée à l'état du jeu).

## Pistes pour une v7 (à tester une à la fois)

1. Recruter dès qu'un triangle est détenu depuis le tour précédent (sans plafond fixe à 6).
2. Revoir l'ouverture : viser la capture d'un triangle dès les tours 0 à 2.
3. Déplacer plus d'unités par tour une fois l'armée grandie (aujourd'hui 3 déplacements max).
4. Écrire un adversaire local imitant ces règles de Baron pour valider chaque changement.
