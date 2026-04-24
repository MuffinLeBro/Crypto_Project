# Crypto Project

Crypto Project est un projet de cryptographie pédagogique écrit en Python. Le repo combine une CLI connectée à un serveur ISC, une base d'interface graphique PyQt6, et plusieurs modules de chiffrement, de hachage et d'échange de clés.

L'objectif du projet est double : manipuler des mecanismes classiques de cryptographie et structurer une application claire autour de trois couches distinctes : algorithmes, protocole de communication et interface utilisateur.

## Pourquoi ce projet

Ce projet a été concu comme un projet de cryptographie a vocation academique. Il permet de :

- tester plusieurs algorithmes classiques dans un même environnement ;
- comprendre le format de trame ISC utilisé pour l'encodage et le décodage de messages ;
- manipuler une CLI à buffers pour chiffrer, dechiffrer, stocker et envoyer des messages ;
- poser les bases d'une interface graphique avec la librairie PyQt6.

Ce repo est adapté à l'apprentissage, à la démonstration et à l'experimentation. Il n'a pas vocation à etre utilisé tel quel comme solution de sécurite dans la réalisté.

## Fonctionnalites

- chiffrement par décalage ;
- chiffrement et dechiffrement de Vigenere ;
- génération de cles RSA, chiffrement et déchiffrement RSA ;
- calcul de hachage SHA-256 ;
- génération de parametres Diffie-Hellman et calcul de clés partagées ;
- création et analyse de trames ISC ;
- client TCP pour échange avec un serveur distant ;
- historique des messages, buffers plain/encoded et commandes utilitaires ;
- prototype d'interface graphique avec PyQt6.

## Architecture du projet

Le projet est organisé autour de composants simples et bien séparés :

- [Command.py](Command.py) centralise les operations cryptographiques ;
- [MessageHandler.py](MessageHandler.py) construit et decode les trames ISC ;
- [Client.py](Client.py) gere la connexion TCP au serveur ;
- [CLI.py](CLI.py) sert de point d'entrée pour le mode ligne de commande ;
- [main.py](main.py) charge l'interface graphique PyQt6 ;
- [cli/](cli/) contient le moteur de la CLI, les buffers, l'historique et les handlers de commandes ;
- [test/test_commands.py](test/test_commands.py) sert de script de demonstration rapide des commandes crypto.
- [MainWindow.py] contient tous le code de l'interface graphique
- [DiffieHellman.py] contient tous la génération de l'algorithme de cryptage DiffieHellman

## Prerequis

- Python 3.12 ou plus recent ;
- PyQt6 ;
- accés réseau au serveur

Le serveur configure dans le projet est :

- hote : `vlbelintrocrypto.hevs.ch`
- port : `6000`

## Installation

### Option 1 : avec uv

Le depot contient un fichier `uv.lock`, ce qui permet une installation rapide avec uv :

```bash
uv sync
```

### Option 2 : avec venv et pip

```bash
python -m venv .venv
. .venv/bin/activate
pip install pyqt6
```

Sur Linux, si vous utilisez l'environnement virtuel du depot, lancez de preference les scripts avec `.venv/bin/python`.

## Lancer le projet

### Mode CLI

```bash
.venv/bin/python CLI.py
```

ou avec uv :

```bash
uv run python CLI.py
```

La CLI tente de se connecter immediatement au serveur distant. Si le serveur est indisponible, l'application s'arrete apres l'echec de connexion.

### Mode interface graphique
```bash
.venv/bin/python main.py
```

L'interface graphique charge bien la vue PyQt6 definie dans `CryptoInterface.ui`. A ce stade, elle joue surtout le role de base d'interface ; la logique complete des boutons n'est pas encore entierement reliee a des actions metier dans le code.

## Commandes principales de la CLI

| Domaine | Commande | Description |
| --- | --- | --- |
| Aide | `/help` | Affiche la liste des commandes disponibles |
| Connexion | `/health` | Verifie l'etat de la connexion serveur |
| Envoi | `/send <text>` | Envoie un texte brut au serveur |
| Envoi | `/send plain` | Envoie le contenu du plain buffer |
| Envoi | `/send encoded` | Envoie le contenu du encoded buffer |
| Buffers | `/set plain <text>` | Definit le plain buffer |
| Buffers | `/set encoded <text>` | Definit le encoded buffer |
| Buffers | `/show` | Affiche les buffers courants |
| Buffers | `/clearbuf [plain|encoded]` | Vide un ou les deux buffers |
| Historique | `/list [n]` | Affiche les derniers messages |
| Historique | `/select <i> [e|c]` | Copie un message de l'historique dans un buffer |
| Shift | `/encode shift <k>` | Chiffre le plain buffer avec un decalage |
| Shift | `/decode shift <k>` | Dechiffre le encoded buffer avec un decalage |
| Vigenere | `/encode vigenere <key>` | Chiffre le plain buffer |
| Vigenere | `/decode vigenere <key>` | Dechiffre le encoded buffer |
| RSA | `/rsa generate` | Genere une paire de cles RSA |
| RSA | `/encode rsa <pub> <mod>` | Chiffre le plain buffer en liste d'entiers |
| RSA | `/decode rsa <priv> <mod>` | Dechiffre la liste RSA stockee dans encoded |
| Hash | `/hash` | Calcule le SHA-256 du plain buffer |
| Diffie-Hellman | `/dh generate [max_mod]` | Genere un modulo et un generateur |
| Diffie-Hellman | `/dh halfkey <mod> <gen> [priv_a]` | Calcule une demi-cle |
| Diffie-Hellman | `/dh secret <mod> <gen> <priv_a> <gB>` | Calcule le secret partage |
| ISC | `/decode isc [hex_message]` | Decode une trame ISC depuis un hex ou le buffer |
| Sortie | `/quit` ou `/exit` | Ferme la session |

## Exemple de session

```text
/set plain Bonjour le monde
/encode vigenere KEY
/show
/decode vigenere KEY
/hash
/rsa generate
/dh generate 500
```

## Format des trames ISC

Le projet encode et decode un format ISC simple via `MessageHandler`.

Structure d'une trame :

- 3 octets d'en-tete : `ISC`
- 1 octet pour le type de message
- 2 octets big-endian pour le nombre de caracteres
- corps du message : chaque caractere UTF-8 est aligne sur 4 octets

Ce mecanisme permet de construire une trame binaire stable et de la retransformer ensuite en texte lisible.

## Structure du depot

```text
.
├── CLI.py
├── Client.py
├── Command.py
├── CryptoInterface.ui
├── DiffieHellman.py
├── MainWindow.py
├── MessageHandler.py
├── main.py
├── pyproject.toml
├── cli/
│   ├── cli.py
│   ├── buffers.py
│   ├── history.py
│   ├── constants.py
│   └── handlers/
└── test/
    └── test_commands.py
```

## Etat actuel et limites

- la CLI dépend d'un serveur distant pour son exécution normale ;
- l'interface graphique présente permet une utilisation plus simple que l'utilisation en CLI. Elle est également la version qu'on doit utiliser pour exécuter le projet.
- le fichier `test/test_commands.py` ressemble aujourd'hui davantage a un script de verification manuelle qu'a une vraie suite de tests automatisee ;
- plusieurs algorithmes présents ici sont implémentés pour l'apprentissage et la compréhension, pas pour un usage sécuritaire réel.

## Pistes d'amélioration
- ajouter le décode des différents algorithme qui ne sont pas demandés comme le shift, vigénére

## Résumé

Crypto Project est un projet de cryptographie en Python qui sert à explorer plusieurs techniques classiques, à manipuler un protocole de message ISC et à construire une application organisée autour d'une CLI connectée et d'une interface graphique PyQt6. C'est une base propre pour un projet academique de cryptographie, avec une architecture déjà lisible et des extensions naturelles pour aller plus loin.
