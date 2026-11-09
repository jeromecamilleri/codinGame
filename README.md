# CodinGame – workspace de Jerome

## Projets
| Dossier | Jeu | Type |
|---|---|---|
| `tryangle-catch/` | Fall Challenge 2026 – TryAngle Catch | Bot 2 joueurs (v2…v6), replays, analyses |
| `fallChallenge2024/` | Fall Challenge 2024 – Selenia City | Optimisation solo, 24 tests locaux |
| `laResistance-codegolf/` | La résistance – Code Golf (`the-resistance-codesize`) | Code golf, tests locaux + visualiseur web |
| `cellularenaWinterChallenge2024/` | Winter Challenge 2024 – Cellularena | Bot + simulateur |
| fichiers `.py` à la racine, `Tron Battle/` | Anciens puzzles | – |

## Outils partagés (`common/`)
| Fichier | Rôle |
|---|---|
| `setup-tools.sh` | Installe Maven dans `.tools/` (ignoré par git) |
| `env.sh` | À sourcer : `MVN`, `cg()` (API avec token `~/.config/codingame/token`) |
| `referee_classpath.sh DIR` | Compile un referee Maven et affiche son classpath (cache `DIR/.classpath`) |
| `run_solo_referee.sh batch\|view DIR bot.py tests…` | Lance un referee solo : scores en batch, ou visualiseur web |
| `run_duel_referee.sh view\|batch DIR niveau seed port bot0 bot1` | Lance un referee à 2 joueurs (visualiseur ou scores) |
| `java/LocalBatch.java`, `LocalView.java` | Lanceurs Java utilisés par le script ci‑dessus |
| `cg_api.py replay ID…` / `puzzle PUBLIC_ID` | Télécharge replays (JSON) ou énoncé du puzzle |
| `statement_to_md.py` | Convertit un énoncé HTML de referee en Markdown (`--level` = ligue affichée) |
| `json_to_log.py` | Convertit un replay JSON en log texte (`replays/raw/`, depuis le dossier du projet) |

## Énoncés
Chaque projet a un `OBJECTIF.md` (objectif, règles, entrées/sorties). Pour les referees HTML : `common/statement_to_md.py FICHIER.html --level levelN > OBJECTIF.md` ; pour les puzzles : `common/cg_api.py puzzle ID`.

## Conventions
- Chaque projet garde son referee dans `vendor/` (ignoré par git) et ses bots versionnés `bot_vN_*.py`.
- Chaque projet tient un historique (`BOT_HISTORY.md`) et un document de passation (`docs/`).
- Les résultats locaux ne sont qu'un échantillon ; une nouvelle version n'est conservée que si elle bat les précédentes.
- Rien n'est commité sans relecture.

## Démarrage rapide
```sh
common/setup-tools.sh
cd fallChallenge2024 && ./run-local.sh bot_v1.py 1 2     # scores locaux
cd tryangle-catch && ./run-head-to-head.sh bot_v6_cycle_guard.py bot_v5_no_reversal.py
```
