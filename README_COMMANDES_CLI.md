# Guide de test CLI

Ce document liste les commandes disponibles dans la CLI du projet, avec des exemples concrets a taper pour les tester.

## Demarrage

Sous Linux, lancer la CLI avec :

```bash
cd /home/jaures/Téléchargements/Crypto_Project
./.venv/bin/python CLI.py
```

Au demarrage, la CLI tente de se connecter au serveur `vlbelintrocrypto.hevs.ch:6000`.

## Notions utiles

- `plain_buffer` : contient le texte en clair
- `encoded_buffer` : contient le texte encode, ou une liste d'entiers pour RSA
- `messages` : historique des messages envoyes et recus
- `/list` et `/select` utilisent l'historique `messages`
- `/send encoded` fonctionne si `encoded_buffer` contient une chaine
- apres `/encode rsa`, `encoded_buffer` contient une liste d'entiers, donc `/send encoded` ne convient plus

## Commandes de base

### `/help`

Affiche la liste des commandes.

Exemple :

```text
/help
```

### `/health`

Verifie l'etat de la connexion au serveur.

Exemple :

```text
/health
```

### `/quit` et `/exit`

Ferme la CLI et coupe la connexion.

Exemples :

```text
/quit
```

```text
/exit
```

### `/clear`

Efface l'ecran.

Exemple :

```text
/clear
```

### `<text>`

Toute ligne sans slash est envoyee directement au serveur comme message clair de type `s`.

Exemple :

```text
Bonjour serveur
```

## Buffers

### `/set <plain|encoded> <text>`

Place du texte dans l'un des deux buffers.

Exemples :

```text
/set plain Bonjour tout le monde
```

```text
/set encoded 4953437300020000004800000069
```

### `/show`

Affiche le contenu des buffers.

Exemple :

```text
/show
```

### `/clearbuf [plain|encoded]`

Vide les buffers.

Exemples :

```text
/clearbuf
```

```text
/clearbuf plain
```

```text
/clearbuf encoded
```

## Envoi

### `/send <text>|plain|encoded [-s]`

Envoie soit un texte direct, soit le contenu d'un buffer.

Exemples :

```text
/send Message envoye explicitement
```

```text
/set plain Message depuis plain_buffer
/send plain
```

```text
/set plain BONJOUR
/encode shift 3
/send encoded
```

```text
/send Message silencieux -s
```

Note : le flag `-s` envoie le message sans afficher `Message envoye: ...` dans la CLI.

## Historique

### `/list [n]`

Affiche les `n` derniers messages de l'historique. Si `n` n'est pas precise, la valeur par defaut est `10`.

Exemples :

```text
/list
```

```text
/list 5
```

### `/select <i> [e|c]`

Copie le message d'index `i` dans un buffer.

- `c` copie dans `plain_buffer`
- `e` copie dans `encoded_buffer`

Exemple de sequence :

```text
Bonjour historique
/send Test historique
/list 5
/select 0 c
/select 0 e
```

Adaptez l'index `0` a ce que `/list` affiche chez vous.

## Chiffrement par decalage

### `/encode shift <k>`

Encode `plain_buffer` avec un decalage entier `k`.

Exemple :

```text
/set plain BONJOUR
/encode shift 3
/show
```

Resultat attendu dans `encoded_buffer` : `ERQMRXU`

### `/decode shift <k>`

Decode `encoded_buffer` avec le meme decalage `k`.

Exemple :

```text
/decode shift 3
/show
```

Resultat attendu dans `plain_buffer` : `BONJOUR`

## Decodage ISC

### `/decode isc [hex_message]`

Decode une trame ISC en hexadecimal, soit directement en argument, soit depuis `encoded_buffer`.

Exemple invalide pour verifier le message d'aide :

```text
/decode isc 0102030405060708
```

La CLI doit afficher que l'en-tete ISC attendu est `495343 ('ISC')` et proposer un exemple valide.

Exemple valide direct :

```text
/decode isc 4953437300020000004800000069
```

Resultat attendu : type `s`, longueur `2`, texte `Hi`.

Exemple via `encoded_buffer` :

```text
/set encoded 4953437300020000004800000069
/decode isc
```

## Vigenere

### `/encode vigenere <key>`

Encode `plain_buffer` avec la cle Vigenere donnee.

Exemple :

```text
/set plain Attack at dawn!
/encode vigenere LEMON
/show
```

Resultat attendu dans `encoded_buffer` : `Lxfopv ef rnhr!`

### `/decode vigenere <key>`

Decode `encoded_buffer` avec la meme cle.

Exemple :

```text
/decode vigenere LEMON
/show
```

Resultat attendu dans `plain_buffer` : `Attack at dawn!`

## RSA

### `/rsa generate`

Genere une paire de cles RSA et le modulo par defaut du projet.

Exemple :

```text
/rsa generate
```

Avec les valeurs par defaut du code, la CLI affiche :

- cle publique `(17, 851)`
- cle privee `(233, 851)`

### `/encode rsa <pub> <mod>`

Encode `plain_buffer` en liste d'entiers RSA.

Exemple :

```text
/set plain Hi
/encode rsa 17 851
/show
```

Resultat attendu dans `encoded_buffer` : `[315, 512]`

### `/decode rsa <priv> <mod>`

Decode une liste RSA presente dans `encoded_buffer`.

Exemple :

```text
/decode rsa 233 851
/show
```

Resultat attendu dans `plain_buffer` : `Hi`

Note : pour cette commande, `encoded_buffer` doit venir d'un `/encode rsa` precedent.

## Hash

### `/hash`

Calcule le SHA-256 de `plain_buffer`.

Exemple :

```text
/set plain hello
/hash
```

Resultat attendu :

```text
SHA-256: 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
```

## Diffie-Hellman

### `/dh generate [max_mod]`

Genere un modulo premier et un generateur.

Exemple :

```text
/dh generate 100
```

Le resultat depend du tirage aleatoire.

### `/dh halfkey <mod> <gen> [priv_a]`

Calcule la valeur publique partielle a partir d'un modulo, d'un generateur et eventuellement d'une cle privee.

Exemples :

```text
/dh halfkey 23 5 6
```

Resultat attendu : `A (half key) = 8`

```text
/dh halfkey 23 5 15
```

Resultat attendu : `A (half key) = 19`

### `/dh secret <mod> <gen> <priv_a> <gB>`

Calcule le secret partage a partir de la cle privee locale et de la valeur publique recue.

Exemples :

```text
/dh secret 23 5 6 19
```

```text
/dh secret 23 5 15 8
```

Dans les deux cas, le resultat attendu est : `DH Shared Secret = 2`

## Sequence de test rapide

Si vous voulez faire un tour rapide des commandes principales dans un ordre logique, vous pouvez tester :

```text
/health
/set plain BONJOUR
/encode shift 3
/decode shift 3
/set plain Attack at dawn!
/encode vigenere LEMON
/decode vigenere LEMON
/decode isc 0102030405060708
/decode isc 4953437300020000004800000069
/rsa generate
/set plain Hi
/encode rsa 17 851
/decode rsa 233 851
/set plain hello
/hash
/dh halfkey 23 5 6
/dh halfkey 23 5 15
/dh secret 23 5 6 19
/dh secret 23 5 15 8
/list 10
```