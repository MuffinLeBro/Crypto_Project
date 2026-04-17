# Documentation technique de la CLI

## Objectif

Ce document explique comment la CLI du projet a ete implementee, quelles classes elle utilise, comment les commandes sont distribuees, et quels fichiers sont appeles pendant l'execution.

Le coeur de la CLI se trouve dans [CLI.py](CLI.py).

## Fichiers impliques

- [CLI.py](CLI.py) : interface texte, boucle de lecture, dispatch des commandes, affichage utilisateur
- [Client.py](Client.py) : connexion TCP, envoi, reception, boucle de lecture reseau
- [MessageHandler.py](MessageHandler.py) : encodage et decodage du protocole ISC
- [Command.py](Command.py) : operations crypto exposees a la CLI
- [main.py](main.py) : point d'entree global du projet, qui peut instancier la CLI

## Vue d'ensemble de l'architecture

La CLI suit une architecture simple en couches.

1. La couche interaction utilisateur est dans [CLI.py](CLI.py).
2. La couche reseau est dans [Client.py](Client.py).
3. La couche protocole est dans [MessageHandler.py](MessageHandler.py).
4. La couche logique crypto est dans [Command.py](Command.py).

La CLI n'implemente donc ni le socket, ni le protocole binaire, ni les algorithmes crypto. Elle orchestre simplement ces composants.

## Point d'entree de la CLI

La CLI peut etre lancee de deux manieres.

### Lancement direct

En bas de [CLI.py](CLI.py), le bloc suivant permet d'executer la CLI directement :

```python
if __name__ == "__main__":
    cli = CLI()
    cli.run()
```

### Lancement depuis le projet global

Dans [main.py](main.py), une instance de `CLI` est aussi creee et executee avec `cli.run()`.

Techniquement, cela signifie que la CLI est utilisable comme module autonome, mais aussi comme composant appele depuis un point d'entree plus large.

## Construction de l'objet CLI

Dans `CLI.__init__()`, la classe initialise ses dependances principales.

```python
self.client = Client()
self.handler = MessageHandler()
self.cmd = Command()
```

Ces trois objets definissent les responsabilites externes de la CLI :

- `Client()` pour parler au serveur
- `MessageHandler()` pour construire et decoder les trames ISC
- `Command()` pour chiffrer, dechiffrer, hasher et generer des valeurs crypto

La CLI initialise aussi son etat interne :

- `plain_buffer` : texte clair courant
- `encoded_buffer` : texte encode courant ou liste d'entiers pour RSA
- `messages` : historique des messages envoyes et recus
- `last_decoded_isc` : derniere trame ISC decodee sous forme structuree

## Boucle d'execution

La methode `run()` est la boucle principale de la CLI.

Elle fait les operations suivantes dans cet ordre :

1. connexion au serveur avec `self.client.connect(...)`
2. verification que la connexion est etablie
3. demarrage de la reception asynchrone avec `self.client.start_receiving(self.on_message_received)`
4. affichage du banner avec `show_banner()`
5. lecture continue des entrees utilisateur avec `input()`
6. redirection de l'entree soit vers le routeur de commandes, soit vers l'envoi direct d'un message

Le squelette logique ressemble a ceci :

```python
def run(self):
    self.client.connect(ADDRSERVER, PORT)
    self.client.start_receiving(self.on_message_received)
    self.show_banner()

    while self.client.running:
        user_input = input("> ")
        if user_input.startswith("/"):
            self.handle_command(user_input.strip())
        else:
            self.send_to_server("s", user_input)
```

## Routing des commandes

Le point central du dispatch est `handle_command()` dans [CLI.py](CLI.py).

Cette methode :

1. decoupe la ligne utilisateur en commande + arguments
2. identifie la commande principale
3. delegue vers une methode privee specialisee

Exemples de redirection :

- `/clearbuf` -> `_cmd_clearbuf()`
- `/set` -> `_cmd_set()`
- `/show` -> `_cmd_show()`
- `/list` -> `_cmd_list()`
- `/select` -> `_cmd_select()`
- `/send` -> `_cmd_send()`
- `/encode` -> `_cmd_encode()`
- `/decode` -> `_cmd_decode()`
- `/rsa` -> `_cmd_rsa()`
- `/hash` -> `_cmd_hash()`
- `/dh` -> `_cmd_dh()`

Cette structure est importante car elle evite d'avoir toute la logique metier dans une seule grande methode. Chaque sous-commande a sa propre unite de code.

## Pourquoi le dispatch est bien structure

L'implementation choisit une structure simple :

- un point d'entree unique pour les commandes
- une methode par groupe fonctionnel
- des validations locales sur les arguments dans chaque sous-commande

Cela rend la CLI plus facile a faire evoluer. Pour ajouter une nouvelle commande, il suffit en general de :

1. ajouter la ligne dans le `BANNER`
2. ajouter un `elif` dans `handle_command()`
3. creer une methode privee dediee

## Buffers internes

La CLI repose sur deux buffers principaux.

### plain_buffer

`plain_buffer` contient le texte en clair. Il est utilise comme entree pour :

- `/encode shift`
- `/encode vigenere`
- `/encode rsa`
- `/hash`

### encoded_buffer

`encoded_buffer` contient une forme encodee du message. Selon le contexte, ce buffer peut stocker :

- une chaine pour shift ou vigenere
- une chaine hexadecimale pour la commande ISC
- une liste d'entiers pour RSA

La CLI verifie donc parfois le type du buffer avant de lancer une operation, par exemple pour RSA ou le decodage ISC.

## Historique des messages

La liste `messages` conserve l'historique des echanges sous la forme :

```python
(direction, msg_type, text)
```

Exemple :

- `("sent", "s", "bonjour")`
- `("recv", "r", "reponse")`

Cet historique est exploite par :

- `_cmd_list()` pour afficher les derniers messages
- `_cmd_select()` pour recopier un message dans `plain_buffer` ou `encoded_buffer`

## Flux d'envoi d'un message

Quand l'utilisateur envoie un message, le flux technique est le suivant :

1. [CLI.py](CLI.py) recoit l'entree utilisateur
2. `send_to_server(msg_type, text)` est appelee
3. `MessageHandler.build_message(msg_type, text)` construit la trame ISC
4. `Client.send(payload)` envoie les octets au serveur
5. la CLI enregistre l'operation dans `messages`

Le point important ici est que [CLI.py](CLI.py) ne construit pas elle-meme les octets du protocole. Cette responsabilite est delegatee a [MessageHandler.py](MessageHandler.py).

## Flux de reception d'un message

Quand le serveur envoie des donnees, le flux est le suivant :

1. [Client.py](Client.py) lit les octets dans `receive_loop()`
2. `Client.start_receiving()` appelle la callback `CLI.on_message_received`
3. `CLI.on_message_received()` transmet les octets a `MessageHandler.parse_message(raw_data)`
4. le message decode est converti en objet structure
5. la CLI ajoute le message a l'historique puis l'affiche

Ce flux montre bien la separation des responsabilites :

- [Client.py](Client.py) transporte les octets
- [MessageHandler.py](MessageHandler.py) les decode
- [CLI.py](CLI.py) les presente a l'utilisateur

## Commandes principales et modules appeles

### Commandes de buffer

- `_cmd_set()` modifie les buffers internes
- `_cmd_clearbuf()` vide les buffers
- `_cmd_show()` affiche leur etat

Ces commandes restent purement locales a [CLI.py](CLI.py).

### Commandes reseau

- `_cmd_send()` appelle `send_to_server()`
- `/health` utilise `Client.health()`
- `/quit` change l'etat `self.client.running`

Ces commandes s'appuient directement sur [Client.py](Client.py).

### Commandes crypto

Les commandes suivantes passent par [Command.py](Command.py) :

- `_cmd_encode()`
- `_cmd_decode()`
- `_cmd_rsa()`
- `_cmd_hash()`
- `_cmd_dh()`

Autrement dit, [CLI.py](CLI.py) ne contient pas l'algorithme de chiffrement lui-meme. Elle utilise [Command.py](Command.py) comme moteur metier.

### Commande ISC

La sous-commande `_cmd_decode_isc()` utilise [MessageHandler.py](MessageHandler.py) pour decoder une trame ISC hexadecimale :

1. elle recupere soit l'argument passe a la commande, soit `encoded_buffer`
2. elle appelle `self.handler.parse_hex_message(...)`
3. elle recupere un `ISCMessage`
4. elle affiche le type, la longueur et le texte
5. elle copie le texte decode dans `plain_buffer`

## Choix d'implementation

La CLI a ete implementee comme un orchestrateur, pas comme une classe qui sait tout faire.

Ce choix apporte plusieurs avantages :

- le code reseau reste dans [Client.py](Client.py)
- le protocole reste dans [MessageHandler.py](MessageHandler.py)
- la logique crypto reste dans [Command.py](Command.py)
- [CLI.py](CLI.py) reste concentre sur le flux utilisateur et le dispatch

Cette separation est la bonne direction pour garder une architecture lisible et extensible.

## Limites actuelles

Dans l'etat actuel du projet :

- la CLI est fonctionnelle et autonome
- [main.py](main.py) melange encore interface graphique et interface CLI dans le meme point d'entree
- la CLI utilise encore des verifications locales simples plutot qu'une couche de validation commune

Ce sont des limites d'orchestration, pas de conception de base de la CLI elle-meme.

## Resume technique

La CLI a ete implementee autour de quatre idees simples :

1. une boucle principale dans `run()`
2. un routeur central dans `handle_command()`
3. des sous-methodes specialisees par famille de commandes
4. une delegation claire vers [Client.py](Client.py), [MessageHandler.py](MessageHandler.py) et [Command.py](Command.py)

Cette implementation est saine car elle garde une responsabilite claire par fichier et rend l'ajout de nouvelles commandes relativement simple.