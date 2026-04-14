# Crypto Project

## Documentation supplementaire

- [README_CLI.md](README_CLI.md) : detail technique sur l'implementation de la CLI

## Feature ajoutee : decoder les messages ISC

Le projet sait maintenant decoder une trame ISC de maniere explicite et reutilisable, avec une commande disponible cote CLI.

## Objectif de la feature

L'objectif etait d'ajouter un vrai decodeur de trames ISC qui fonctionne dans deux contextes :

- reception d'un message serveur en octets
- decodage manuel d'une trame ISC saisie en hexadecimal dans la CLI

L'implementation a ete faite en separant clairement la logique protocolaire de la logique d'interface.

## Fichiers impliques

- [MessageHandler.py](MessageHandler.py) : contient toute la logique du protocole ISC, en encodage et en decodage
- [CLI.py](CLI.py) : expose la commande utilisateur `/decode isc` et affiche le resultat
- [Client.py](Client.py) : recoit les octets depuis le serveur puis les transmet a la CLI
- [README.md](README.md) : documente le fonctionnement et les choix d'architecture

## Chaine d'appel technique

### Cas 1 : decodage manuel dans la CLI

Quand l'utilisateur tape une commande de ce type :

```text
/decode isc 4953437300020000004800000069
```

le flux d'appel est le suivant :

1. [CLI.py](CLI.py) recoit la commande dans `handle_command()`
2. `handle_command()` appelle `_cmd_decode()`
3. `_cmd_decode()` detecte la methode `isc` et appelle `_cmd_decode_isc()`
4. `_cmd_decode_isc()` transmet la trame hexadecimale a `MessageHandler.parse_hex_message()`
5. `parse_hex_message()` convertit l'hexadecimal en octets puis appelle `parse_message()`
6. `parse_message()` decode la trame ISC en plusieurs etapes et retourne un objet `ISCMessage`
7. [CLI.py](CLI.py) affiche le type, la longueur et le texte, puis copie le texte decode dans `plain_buffer`

### Cas 2 : message recu depuis le serveur

Quand des octets arrivent depuis le serveur :

1. [Client.py](Client.py) lit les octets avec `receive()` ou `receive_loop()`
2. la callback `CLI.on_message_received()` est appelee
3. `on_message_received()` appelle `MessageHandler.parse_message(raw_data)`
4. la meme logique de decodage ISC est reutilisee
5. le message decode est ajoute a l'historique CLI puis affiche a l'ecran

Ce point est important : le decodage serveur et le decodage manuel passent par le meme parseur. Cela evite d'avoir deux implementations differentes du protocole.

## Detail de l'implementation dans MessageHandler.py

Le fichier [MessageHandler.py](MessageHandler.py) centralise le protocole ISC. Le parseur a ete volontairement decoupe en petites etapes lisibles.

### 1. Parser le header

La methode `_read_header(raw_bytes)` lit les 3 premiers octets et valide qu'ils correspondent bien a `ISC`.

Si le header est incorrect, une erreur est levee immediatement.

### 2. Lire le type

La methode `_read_type(raw_bytes)` lit l'octet situe juste apres le header et le decode en UTF-8.

Le type represente la nature du message, par exemple `s` ou `r`.

### 3. Lire la longueur

La methode `_read_length(raw_bytes)` lit les 2 octets suivants et les convertit en entier avec `struct.unpack('>H', ...)`.

Le format `>H` signifie :

- `>` : big-endian
- `H` : entier non signe sur 2 octets

### 4. Extraire le message

La methode `_extract_text(body_bytes, char_count)` :

- verifie d'abord que la taille du corps correspond bien a `char_count * bytesPerChar`
- decoupe le corps en blocs fixes de 4 octets par caractere
- appelle `_decode_char_block()` pour chaque bloc
- reconstruit le texte final

La methode `_decode_char_block()` retire le padding en zero ajoute lors de l'encodage et decode le caractere UTF-8.

### 5. Retourner un objet structure

Au lieu de renvoyer seulement un tuple, `parse_message()` retourne un objet `ISCMessage` contenant :

- `msg_type`
- `text`
- `char_count`
- `raw_bytes`

Cette structure est plus propre pour la CLI, car elle permet d'afficher plusieurs informations sans recalculer le parsing.

## Pourquoi parse_hex_message existe en plus de parse_message

Il y a deux entrees possibles pour le decodeur :

- des octets reels recus depuis le reseau
- une chaine hexadecimale saisie par l'utilisateur

Pour garder une architecture propre :

- `parse_hex_message()` s'occupe uniquement de transformer une chaine hexadecimale en octets
- `parse_message()` s'occupe uniquement du protocole ISC binaire

Cette separation evite de melanger conversion d'entree et logique de parsing.

## Utilisation cote CLI

La commande suivante a ete ajoutee dans [CLI.py](CLI.py) :

```text
/decode isc [hex_message]
```

Deux usages sont possibles.

### Decoder une trame fournie directement

```text
/decode isc 4953437300020000004800000069
```

### Decoder le contenu deja stocke dans le buffer encoded

```text
/set encoded 4953437300020000004800000069
/decode isc
```

Resultat attendu :

- la trame est analysee
- le type ISC est affiche
- la longueur est affichee
- le texte extrait est place dans `plain_buffer`
- la derniere trame structuree est conservee dans `last_decoded_isc`

## Format ISC decode

Une trame ISC est lue dans cet ordre :

1. header sur 3 octets : `ISC`
2. type sur 1 octet
3. longueur sur 2 octets
4. corps du message avec 4 octets par caractere

Exemple de trame hexadecimale pour le message `Hi` de type `s` :

```text
4953437300020000004800000069
```

Lecture de cet exemple :

- `495343` -> header `ISC`
- `73` -> type `s`
- `0002` -> longueur `2`
- `00000048 00000069` -> texte `Hi`

## Choix d'architecture

Cette implementation suit une separation simple et robuste :

- [MessageHandler.py](MessageHandler.py) connait le protocole ISC
- [CLI.py](CLI.py) connait l'interaction utilisateur
- [Client.py](Client.py) connait le transport reseau

Cette repartition est importante car elle permet :

- de reutiliser le parseur partout
- de tester le protocole sans lancer le serveur
- d'eviter le code duplique entre le reseau et la CLI
- de faire evoluer la CLI sans casser le format ISC
