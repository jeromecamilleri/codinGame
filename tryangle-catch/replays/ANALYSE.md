# Analyse des défaites contre Baron Bosswell

Quatre journaux texte et un replay JSON ont été récupérés par l'API et archivés dans `raw/`.
Les quatre journaux texte sont indexés par `replay_history.jsonl`; les nombres du replay JSON
918741865 ont été vérifiés directement dans ses frames et résumés. Les frames indiquent l'ordre
dans le journal, pas le numéro du tour CodinGame.

| Replay | Format | 1re capture Baron / jejecam | Triangles capturés Baron / jejecam | Renforts Baron / jejecam | Score final | Fin de partie |
|---|---|---:|---:|---:|---:|---|
| 918739641 | texte | 3 / 77 | 42 / 8 | 43 / 3 | -1 / 123 | jejecam ne pouvait plus marquer |
| 918740399 | texte | 7 / aucune | 23 / 0 | 18 / 0 | -1 / 27 | jejecam ne pouvait plus marquer |
| 918740963 | texte | 3 / aucune | 25 / 0 | 24 / 0 | -1 / 37 | jejecam ne pouvait plus marquer |
| 918741122 | texte | 3 / aucune | 54 / 0 | 43 / 0 | -1 / 239 | jejecam n'avait plus d'unités ni de triangles |
| 918741865 | JSON | 3 / 3 | 36 / 8 | 31 / 3 | -1 / 71 | jejecam n'avait plus d'unités ni de triangles |

## Motifs observés

- Dans les quatre replays texte, la première capture de Baron arrive aux frames 3 ou 7. Jejecam
  n'en capture aucun dans trois parties et ne capture son premier triangle qu'à la frame 77 dans
  la quatrième.
- Le JSON 918741865 nuance ce constat : les deux joueurs capturent dès la frame 3. Malgré cette
  ouverture égale, Baron finit par capturer 36 triangles et recruter 31 unités, contre 8 et 3
  pour jejecam.
- Sur les cinq replays, jejecam recrute de zéro à trois unités, contre 18 à 43 pour Baron. Le
  déséquilibre durable d'expansion et de renforts est donc commun aux défaites ; la course à la
  première capture ne suffit pas à les expliquer.
- Les sorties de jejecam montrent des allers-retours récurrents entre les mêmes maisons, par
  exemple `3→11` et `11→3` dans le replay 918739641, `23→1` et `1→23` dans le 918740399, et
  `19→1` / `1→19` dans le 918741122. Cela suggère que le choix de cible change d'un tour à
  l'autre sans que les unités progressent durablement.
- Trois parties finissent par « can't score any more points ». Les deux autres finissent quand
  jejecam n'a plus d'unités ni de triangles. Le referee arrête la partie quand un joueur ne peut
  plus revenir au score ou n'a plus de force ni de triangle.

## Lien avec la v4

Le code actuellement renvoyé par l'API CodinGame correspond exactement à `bot_v4_capture_spawn.py`.
Les journaux ne contiennent toutefois pas d'identifiant de soumission par partie : je ne peux
pas prouver indépendamment que chaque replay a été produit par ces octets exacts. Le profil des
sorties est compatible avec la v4.

J'ai aussi fait jouer la v4 contre les actions enregistrées du Baron du replay 918739641, avec
la même graine et le départ standard : le résultat local reproduit le score final -1 / 123.
Cela valide l'outil de replay pour cette partie.

## Limite pour l'entraînement

Les journaux ne contiennent pas les observations, mais on les reconstitue en rejouant les
commandes des deux sièges dans le referee local (`scripts/reconstruct_states.sh`). Voir
`PROFIL_BARON.md` pour ce qu'on en tire.

## Replays postérieurs à la v5 (soumission `agentId` 6865462)

| Replay | Adversaire | Place de jejecam | Score (jejecam / adversaire) | Fin |
|---|---|---:|---:|---|
| 918756754 | bor2 (joueur) | 0 | -1 / 0 | `$0 timeout` au tour 28 : aucune sortie au tour 27 |
| 918757157 | [CG]Keelhaul | 1 | 1012 / -1 | victoire, adversaire dominé au tour 299 |
| 918756471 | Baron Bosswell | 0 | -1 / 55 | défaite, « can't score any more points » au tour 220 |

- 918756754 : la défaite vient d'un timeout, pas du jeu. Le bot avait 3 captures et l'adversaire
  envoyait 12 ordres invalides. La v4 répond en 2 ms au maximum en local ; un plantage ou une
  sortie vide de la v5 reste à investiguer (la lecture d'entrée s'arrête silencieusement si une
  ligne n'est pas numérique, et le processus quitte alors sans plus rien répondre).
- 918757157 : jejecam joue en position 1 ; l'adversaire à rejouer avec `run-vs-replay.sh` est
  donc l'indice 0 (3e argument).

### 918757432 — nul 0 / 0 contre Winshersterame (jejecam en position 1)

Les deux camps n'ont capturé aucun triangle en 200 tours ; Winshersterame répète `MOVE 3 17 1`
(200 ordres invalides). Les trois unités de jejecam tournent sur trois **cycles de longueur 3**
(`11→17→19→11`, `33→14→6→33`, `40→28→37→40`, ~60 fois chacun). L'interdiction de retour
immédiat de la v5 ne coupe que les cycles de longueur 2 ; elle laisse ces boucles à trois maisons.
Le classement affiche l'adversaire premier à 0 / 0 (`ranks` [0, 1]).
