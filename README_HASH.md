# Documentation technique de la feature Hash

## Objectif

Ce document explique ce qu'est la feature Hash dans le projet, ce qu'elle fait exactement, et comment elle a ete implementee techniquement.

La feature permet de calculer l'empreinte SHA-256 d'un message texte depuis la CLI.

## En quoi consiste Hash dans ce projet

Ici, le mot Hash designe le calcul d'une fonction de hachage cryptographique sur un message.

Le projet utilise SHA-256, qui est une fonction de hachage a sens unique.

Cela signifie :

- on part d'un texte en entree
- on calcule une empreinte hexadecimale de longueur fixe
- on ne peut pas retrouver le texte original a partir du hash

Contrairement a Shift, Vigenere ou RSA, le hash n'est pas un chiffrement reversible.

Son but est plutot de :

- verifier l'integrite d'un message
- comparer deux contenus
- obtenir une empreinte stable d'une donnee

## Comportement retenu dans ce projet

L'implementation actuelle suit ce comportement :

- le hash est calcule avec SHA-256
- le texte source provient du `plain_buffer` de la CLI
- le texte est encode en UTF-8 avant calcul
- le resultat est retourne sous forme hexadecimale avec `hexdigest()`
- le resultat est affiche dans la CLI

Exemple :

- texte : `hello`
- hash SHA-256 : `2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824`

## Fichiers impliques

- [Command.py](Command.py) : contient le calcul du hash SHA-256
- [CLI.py](CLI.py) : expose la commande utilisateur `/hash`
- [README_HASH.md](README_HASH.md) : documente la feature

## Où la feature a ete implementee

L'essentiel de la logique est dans [Command.py](Command.py).

La CLI dans [CLI.py](CLI.py) ne calcule pas elle-meme le hash. Elle appelle la methode metier dediee.

Cette separation est volontaire :

- [Command.py](Command.py) porte la logique crypto
- [CLI.py](CLI.py) porte l'interaction utilisateur

## Detail technique dans Command.py

La feature repose sur une methode tres simple : `sha256(message)`.

Son implementation actuelle est la suivante dans [Command.py](Command.py) :

```python
def sha256(self, message):
    return hashlib.sha256(message.encode('utf-8')).hexdigest()
```

Cette methode fait trois choses :

1. elle prend un texte Python en entree
2. elle l'encode en UTF-8 avec `message.encode('utf-8')`
3. elle calcule le hash SHA-256 puis retourne le resultat en hexadecimal via `hexdigest()`

## Pourquoi hashlib est utilise

Le module standard `hashlib` est le bon choix ici car :

- il fait partie de la bibliotheque standard Python
- il expose directement SHA-256
- il evite de reimplementer une primitive cryptographique complexe
- il fournit une API fiable et concise

Dans ce projet, il n'y a aucune raison valable de reimplementer SHA-256 a la main.

## Integration dans la CLI

La feature est exposee dans [CLI.py](CLI.py) via la commande suivante :

```text
/hash
```

Cette commande travaille sur le contenu du `plain_buffer`.

## Chaine d'appel cote CLI

Quand l'utilisateur tape :

```text
/hash
```

le flux d'appel est le suivant :

1. [CLI.py](CLI.py) recoit la commande dans `handle_command()`
2. `handle_command()` detecte la commande `/hash`
3. `handle_command()` appelle `_cmd_hash()`
4. `_cmd_hash()` verifie que `plain_buffer` n'est pas vide
5. `_cmd_hash()` appelle `self.cmd.sha256(self.plain_buffer)`
6. [Command.py](Command.py) retourne le hash hexadecimale
7. la CLI affiche le resultat

## Methode _cmd_hash dans CLI.py

La methode `_cmd_hash()` est simple et sert uniquement d'adaptateur entre l'utilisateur et la logique metier.

Son role est de :

- verifier qu'un texte est present dans `plain_buffer`
- appeler la methode de hash du moteur `Command`
- afficher le resultat a l'utilisateur

L'implementation suit donc la meme architecture que les autres features : la CLI orchestre, le moteur execute.

## Gestion des erreurs

La gestion d'erreur actuelle est volontairement simple.

Dans [CLI.py](CLI.py), si `plain_buffer` est vide, la commande refuse de s'executer et affiche :

```text
Plain buffer est vide. Utilisez /set plain <text>
```

Cela evite de lancer un calcul sur une entree absente du point de vue utilisateur.

## Pourquoi cette architecture est correcte

Cette implementation est propre pour trois raisons.

### 1. La logique Hash est centralisee

Le calcul SHA-256 est dans [Command.py](Command.py), pas disperse dans la CLI.

### 2. La CLI reste une couche d'orchestration

[CLI.py](CLI.py) ne connait pas les details de `hashlib` ni de SHA-256. Elle :

- lit la commande utilisateur
- verifie l'etat du buffer
- appelle la methode metier
- affiche le resultat

### 3. La feature est reusable

Comme le calcul est dans [Command.py](Command.py), il pourra etre reutilise plus tard dans :

- la GUI
- des tests unitaires
- d'autres commandes ou workflows

## Exemple d'utilisation

### Exemple 1 : calculer le hash d'un texte

```text
/set plain hello
/hash
```

Resultat attendu :

```text
SHA-256: 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
```

### Exemple 2 : verifier que deux textes differents donnent des hashes differents

```text
/set plain hello
/hash
/set plain Hello
/hash
```

L'objectif ici est d'observer que la moindre difference dans le texte change le hash final.

## Ce que la feature ne fait pas

Il est important de clarifier le perimetre.

Cette feature :

- ne dechiffre rien
- ne permet pas de retrouver le message original
- ne signe pas le message
- ne stocke pas automatiquement le hash dans un buffer separe

Elle calcule et affiche uniquement une empreinte SHA-256 du `plain_buffer`.

## Validation logique

Le chemin d'execution est coherent avec l'architecture du projet :

- commande utilisateur dans [CLI.py](CLI.py)
- appel au moteur dans [Command.py](Command.py)
- utilisation de `hashlib.sha256`
- affichage du resultat dans la CLI

## Resume

La feature Hash consiste a ajouter un calcul d'empreinte SHA-256 sur le texte en clair saisi par l'utilisateur.

Elle a ete implementee en separant clairement :

- la logique de calcul dans [Command.py](Command.py)
- l'appel utilisateur dans [CLI.py](CLI.py)

Cette architecture est simple, correcte, et cohérente avec le reste du projet.