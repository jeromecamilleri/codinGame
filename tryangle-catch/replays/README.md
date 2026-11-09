# Historique des replays CodinGame

`raw/` contient les journaux texte originaux récupérés depuis l'API CodinGame. Le fichier
`replay_history.jsonl` est un index dérivé : graine, joueurs, actions, événements, scores,
première capture et cause de fin.

Pour régénérer l'index après avoir ajouté des journaux :

```sh
python3 scripts/import_replay_history.py
```

Pour affronter localement les actions enregistrées du joueur 1 (Baron Bosswell dans ces parties) :

```sh
./run-vs-replay.sh 918739641 bot_v4_capture_spawn.py
```

Le bot de replay rejoue les sorties enregistrées sans les adapter au nouvel état. C'est un
adversaire de régression utile, mais la partie peut diverger dès qu'un ordre produit un état
différent de la partie d'origine. Les journaux ne contiennent pas les observations complètes
reçues à chaque tour ; ils ne suffisent donc pas à entraîner directement un modèle supervisé
état-action. Ils permettent en revanche d'étudier les décisions et les résultats et de rejouer
un comportement historique.

Les replays récupérés au format JSON (`raw/*.json`) sont convertis en `.log` par
`python3 scripts/json_to_log.py`, avant `import_replay_history.py`. Tous les replays
(`jejecam` = bot local v4 contre Baron Bosswell) ont été joués le 8 novembre 2026.

## Observations reconstituées

`scripts/reconstruct_states.sh <id>...` rejoue les deux sièges d'un log dans le referee local
(départ standard, même graine) avec `scripts/record_replay_agent.py`, et écrit
`states/<id>/seat0.txt` et `seat1.txt` : l'entrée initiale (nombre de maisons et coordonnées),
puis un bloc par tour séparé par `---` (scores, `maison mes_unités unités_adverses`, chemins,
triangles `a b c propriétaire peut_capturer adversaire_peut`, chemins possibles), exactement ce
que le bot du siège a reçu. Le score rejoué est identique à l'original dans 8 parties sur 9 ;
dans la partie à timeout 918756754, les tours après le timeout sont remplis par `WAIT`.
`python3 scripts/analyze_states.py` imprime les statistiques par partie et par type de joueur.
