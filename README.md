# Crypto Project

Crypto Project est un projet de cryptographie pedagogique ecrit en Python. Le depot combine une CLI connectee a un serveur ISC, une base d'interface graphique PyQt6, et plusieurs modules de chiffrement, de hachage et d'echange de cles.

L'objectif du projet est double : manipuler des mecanismes classiques de cryptographie et structurer une application claire autour de trois couches distinctes : algorithmes, protocole de message et interface utilisateur.

## Pourquoi ce projet

Ce projet a ete concu comme un projet de cryptographie a vocation academique. Il permet de :

- tester plusieurs algorithmes classiques dans un meme environnement ;
- comprendre le format de trame ISC utilise pour l'encodage et le decodage de messages ;
- manipuler une CLI a buffers pour chiffrer, dechiffrer, stocker et envoyer des messages ;
- poser les bases d'une interface graphique en PyQt6.

Ce depot est adapte a l'apprentissage, a la demonstration et a l'experimentation. Il n'a pas vocation a etre utilise tel quel comme solution de securite en production.

## Fonctionnalites

- chiffrement par decalage ;
- chiffrement et dechiffrement de Vigenere ;
- generation de cles RSA, chiffrement et dechiffrement RSA ;
- calcul de hachage SHA-256 ;
- generation de parametres Diffie-Hellman et calcul de cle partagee ;
- creation et analyse de trames ISC ;
- client TCP pour echange avec un serveur distant ;
- historique des messages, buffers plain/encoded et commandes utilitaires ;
- prototype d'interface graphique avec PyQt6.

## Architecture du projet

Le projet est organise autour de composants simples et bien separes :

- [Command.py](Command.py) centralise les operations cryptographiques ;
- [MessageHandler.py](MessageHandler.py) construit et decode les trames ISC ;
- [Client.py](Client.py) gere la connexion TCP au serveur ;
- [CLI.py](CLI.py) sert de point d'entree pour le mode ligne de commande ;
- [main.py](main.py) charge l'interface graphique PyQt6 ;
- [cli/](cli/) contient le moteur de la CLI, les buffers, l'historique et les handlers de commandes ;
- [test/test_commands.py](test/test_commands.py) sert de script de demonstration rapide des commandes crypto.

## Prerequis

- Python 3.12 ou plus recent ;
- PyQt6 ;
- acces reseau au serveur si vous utilisez la CLI connectee.

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

- la CLI depend d'un serveur distant pour son execution normale ;
- l'interface graphique est presente, mais reste encore une base d'integration ;
- le fichier `test/test_commands.py` ressemble aujourd'hui davantage a un script de verification manuelle qu'a une vraie suite de tests automatisee ;
- plusieurs algorithmes presents ici sont implementes pour l'apprentissage et la comprehension, pas pour un usage securitaire reel.

## Pistes d'amelioration

- relier les boutons de l'interface graphique aux operations de `Command.py` ;
- transformer les verifications manuelles en tests automatises ;
- ajouter une couche de configuration pour le serveur ;
- completer la documentation des formats d'entree et de sortie pour chaque commande.

## Resume

Crypto Project est un projet de cryptographie en Python qui sert a explorer plusieurs techniques classiques, a manipuler un protocole de message ISC et a construire une application organisee autour d'une CLI connectee et d'une interface graphique PyQt6. C'est une base propre pour un projet academique de cryptographie, avec une architecture deja lisible et des extensions naturelles pour aller plus loin.