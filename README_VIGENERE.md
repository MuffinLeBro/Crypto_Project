# Documentation technique de la feature Vigenere

## Objectif

Ce document explique ce qu'est le chiffrement de Vigenere, ce que la feature ajoute dans le projet, et comment elle a ete implementee techniquement.

La feature permet maintenant :

- l'encodage Vigenere
- le decodage Vigenere
- l'utilisation de ces deux operations directement depuis la CLI

## En quoi consiste Vigenere

Le chiffrement de Vigenere est un chiffrement par substitution polyalphabetique.

L'idee est la suivante :

1. on prend un message en clair
2. on prend une cle composee de lettres
3. chaque lettre de la cle donne un decalage alphabetique
4. ce decalage change au fil du texte en suivant la cle de maniere cyclique

Exemple classique :

- message : ATTACKATDAWN
- cle : LEMON
- resultat : LXFOPVEFRNHR

Contrairement a un simple chiffrement par decalage fixe, Vigenere n'utilise pas le meme decalage pour toutes les lettres. C'est ce qui le rend plus fort qu'un Caesar simple dans un contexte pedagogique.

## Comportement retenu dans ce projet

L'implementation du projet suit les regles suivantes :

- seules les lettres alphabetiques sont chiffrees
- la casse est conservee
- les espaces, ponctuations et autres caracteres non alphabetiques sont conserves tels quels
- la cle est reutilisee en boucle
- les caracteres non alphabetiques ne consomment pas une lettre de la cle

Exemple :

- texte : Attack at dawn!
- cle : LEMON
- encode : Lxfopv ef rnhr!

Le texte reste lisible en structure, mais les lettres sont transformees.

## Fichiers impliques

- [Command.py](Command.py) : contient l'algorithme Vigenere
- [CLI.py](CLI.py) : expose les commandes utilisateur pour encoder et decoder
- [README_VIGENERE.md](README_VIGENERE.md) : documente la feature

## Où la feature a ete implementee

L'essentiel de l'implementation se trouve dans [Command.py](Command.py).

La CLI dans [CLI.py](CLI.py) ne contient pas l'algorithme. Elle appelle simplement les methodes du moteur metier.

Cette separation est volontaire :

- [Command.py](Command.py) gere la logique crypto
- [CLI.py](CLI.py) gere l'interaction utilisateur

## Detail technique dans Command.py

La feature a ete implemente sous la forme de quatre methodes.

### 1. _normalize_vigenere_key

Cette methode prepare la cle.

Son role :

- garder uniquement les lettres de la cle
- convertir ces lettres en majuscules
- refuser une cle vide ou invalide

Si la cle ne contient aucune lettre, une erreur `ValueError` est levee.

Cette etape permet d'avoir une base propre pour l'encodage et le decodage.

### 2. _transform_vigenere_char

Cette methode applique la transformation sur un seul caractere.

Son role :

- ignorer les caracteres non alphabetiques
- calculer la position de la lettre dans l'alphabet
- calculer le decalage donne par la lettre de la cle
- appliquer le decalage en modulo 26
- reconstituer la lettre finale en conservant la casse

Le parametre `direction` permet d'utiliser la meme methode pour :

- encoder avec `direction = 1`
- decoder avec `direction = -1`

## Encodage

La methode `encode_vigenere(message, key)` fonctionne ainsi :

1. normaliser la cle avec `_normalize_vigenere_key()`
2. parcourir le message caractere par caractere
3. si le caractere est une lettre, appliquer `_transform_vigenere_char(..., 1)`
4. si le caractere n'est pas une lettre, le recopier tel quel
5. avancer dans la cle uniquement quand une lettre du message a ete traitee

Cette logique permet de chiffrer un texte realiste qui contient des espaces ou de la ponctuation.

## Decodage

La methode `decode_vigenere(message, key)` suit exactement la meme structure que l'encodage, mais appelle `_transform_vigenere_char(..., -1)`.

Cela garantit que l'operation est reversible.

En pratique :

- encodage : ATTACKATDAWN -> LXFOPVEFRNHR avec LEMON
- decodage : LXFOPVEFRNHR -> ATTACKATDAWN avec LEMON

## Integration dans la CLI

La feature est exposee dans [CLI.py](CLI.py) via deux commandes :

```text
/encode vigenere <key>
/decode vigenere <key>
```

## Chaine d'appel cote CLI

### Encodage

Quand l'utilisateur tape :

```text
/encode vigenere LEMON
```

le flux d'appel est le suivant :

1. [CLI.py](CLI.py) recoit la commande dans `handle_command()`
2. `handle_command()` appelle `_cmd_encode()`
3. `_cmd_encode()` detecte la methode `vigenere`
4. `_cmd_encode()` appelle `self.cmd.encode_vigenere(self.plain_buffer, key)`
5. le resultat est stocke dans `encoded_buffer`
6. la CLI affiche le texte encode

### Decodage

Quand l'utilisateur tape :

```text
/decode vigenere LEMON
```

le flux d'appel est le suivant :

1. [CLI.py](CLI.py) recoit la commande dans `handle_command()`
2. `handle_command()` appelle `_cmd_decode()`
3. `_cmd_decode()` detecte la methode `vigenere`
4. `_cmd_decode()` appelle `self.cmd.decode_vigenere(self.encoded_buffer, key)`
5. le resultat est stocke dans `plain_buffer`
6. la CLI affiche le texte decode

## Gestion des erreurs

La feature gere aussi le cas d'une cle invalide.

Dans [Command.py](Command.py), une erreur est levee si la cle ne contient aucune lettre.

Dans [CLI.py](CLI.py), cette erreur est capturee pour afficher un message clair a l'utilisateur au lieu de faire planter la commande.

## Pourquoi cette architecture est correcte

Cette implementation est propre pour trois raisons.

### 1. La logique Vigenere est centralisee

Tout l'algorithme est dans [Command.py](Command.py). Il n'est ni duplique ni disperse dans la CLI.

### 2. La CLI reste une couche d'orchestration

[CLI.py](CLI.py) ne sait pas comment fonctionne Vigenere mathematiquement. Elle sait seulement :

- lire une commande utilisateur
- appeler la bonne methode
- stocker le resultat dans le bon buffer
- afficher le resultat

### 3. L'implementation est reusable

Comme la logique est dans [Command.py](Command.py), elle peut etre reutilisee plus tard par :

- la GUI
- des tests unitaires
- un autre point d'entree que la CLI

## Exemple d'utilisation

### Exemple 1 : texte classique

```text
/set plain ATTACKATDAWN
/encode vigenere LEMON
```

Resultat attendu :

```text
LXFOPVEFRNHR
```

Puis :

```text
/decode vigenere LEMON
```

Resultat attendu :

```text
ATTACKATDAWN
```

### Exemple 2 : texte avec espaces et ponctuation

```text
/set plain Attack at dawn!
/encode vigenere LEMON
```

Resultat attendu :

```text
Lxfopv ef rnhr!
```

Puis :

```text
/decode vigenere LEMON
```

Resultat attendu :

```text
Attack at dawn!
```

## Validation effectuee

La feature a ete verifiee sur ces cas :

- `ATTACKATDAWN` avec la cle `LEMON` encode bien en `LXFOPVEFRNHR`
- le decodage reconstitue bien `ATTACKATDAWN`
- un texte mixte comme `Attack at dawn!` reste reversible
- la casse est conservee
- les caracteres non alphabetiques sont preserves
- la CLI appelle correctement l'implementation de [Command.py](Command.py)

## Resume

La feature Vigenere consiste a ajouter un vrai chiffrement polyalphabetique reversible dans le projet.

Elle a ete implementee en separant clairement :

- l'algorithme dans [Command.py](Command.py)
- l'usage utilisateur dans [CLI.py](CLI.py)

Cette architecture est la bonne base pour garder un code simple, lisible et reutilisable.