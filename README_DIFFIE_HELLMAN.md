# Documentation technique de la feature Diffie-Hellman

## Objectif

Ce document explique ce qu'est Diffie-Hellman, ce que la feature ajoute dans le projet, et comment elle a ete implementee techniquement.

La feature permet de :

- generer des parametres Diffie-Hellman
- calculer une cle publique partielle, appelee ici half key
- calculer un secret partage a partir de sa cle privee et de la cle publique de l'autre partie
- utiliser ces operations directement dans la CLI

## En quoi consiste Diffie-Hellman

Diffie-Hellman est un mecanisme d'echange de cle permettant a deux parties de construire le meme secret partage sans echanger ce secret directement.

Le principe est le suivant :

1. les deux parties conviennent d'un modulo premier `p`
2. elles conviennent d'un generateur `g`
3. chaque partie choisit un secret prive
4. chaque partie calcule une valeur publique partielle
5. chaque partie combine sa valeur privee avec la valeur publique de l'autre
6. les deux obtiennent le meme secret partage

Formules :

- cle publique partielle de A : $A = g^a \bmod p$
- cle publique partielle de B : $B = g^b \bmod p$
- secret calcule par A : $s = B^a \bmod p$
- secret calcule par B : $s = A^b \bmod p$

Le resultat est le meme des deux cotes.

## Comportement retenu dans ce projet

L'implementation actuelle suit cette approche :

- un modulo premier `p` est choisi aleatoirement
- un generateur `g` est choisi aleatoirement entre `2` et `p - 1`
- une cle privee peut etre generee automatiquement ou fournie par l'utilisateur
- la cle publique partielle est calculee avec `pow(gen, priv_a, mod)`
- le secret partage est calcule avec `pow(gB, priv_a, mod)`

Cette implementation est pedagogique et pratique pour la CLI. Elle montre bien le mecanisme d'echange de cle sans ajouter une couche de complexite inutile.

## Fichiers impliques

- [Command.py](Command.py) : contient la logique Diffie-Hellman
- [CLI.py](CLI.py) : expose les commandes utilisateur `/dh`
- [README_DIFFIE_HELLMAN.md](README_DIFFIE_HELLMAN.md) : documente la feature

## Où la feature a ete implementee

La logique metier se trouve dans [Command.py](Command.py).

La CLI dans [CLI.py](CLI.py) ne fait pas les calculs elle-meme. Elle lit les arguments utilisateur, appelle les bonnes methodes, puis affiche les resultats.

Cette separation est volontaire :

- [Command.py](Command.py) gere l'algorithme
- [CLI.py](CLI.py) gere l'experience utilisateur

## Detail technique dans Command.py

La feature repose sur quatre methodes principales.

### 1. _is_prime

La methode `_is_prime(n)` sert a verifier si un entier est premier.

Son role est de filtrer les valeurs possibles pour produire un modulo `p` valable dans `dh_generate()`.

## 2. dh_generate

La methode `dh_generate(max_mod=None)` genere les parametres publics.

Son fonctionnement est le suivant :

1. choisir une borne maximale `max_mod`
2. construire la liste des nombres premiers inferieurs a cette borne
3. choisir aleatoirement un premier `p`
4. choisir aleatoirement un generateur `g`
5. retourner `(p, g)`

La sortie de cette methode correspond aux parametres publics partages entre les participants.

## 3. dh_halfkey

La methode `dh_halfkey(mod, gen, priv_a=None)` calcule la cle publique partielle.

Son fonctionnement :

1. si `priv_a` n'est pas fourni, elle le genere aleatoirement
2. elle calcule `half_key = pow(gen, priv_a, mod)`
3. elle retourne `(half_key, priv_a)`

Le nom half key est celui retenu dans ce projet pour des raisons pratiques dans la CLI. Sur le plan mathematique, il s'agit de la valeur publique partielle.

## 4. dh_secret

La methode `dh_secret(mod, gen, priv_a, gB)` calcule le secret partage.

La formule utilisee est :

$$
s = gB^a \bmod p
$$

Dans l'implementation Python, cela correspond a :

```python
pow(gB, priv_a, mod)
```

Le parametre `gB` represente la cle publique partielle recue de l'autre participant.

## Integration dans la CLI

La feature est exposee dans [CLI.py](CLI.py) via trois commandes :

```text
/dh generate [max_mod]
/dh halfkey <mod> <gen> [priv_a]
/dh secret <mod> <gen> <priv_a> <gB>
```

## Chaine d'appel cote CLI

Le point d'entree utilisateur est `_cmd_dh(args)` dans [CLI.py](CLI.py).

Cette methode agit comme routeur des sous-commandes Diffie-Hellman.

### Cas 1 : generation des parametres publics

Quand l'utilisateur tape :

```text
/dh generate 100
```

le flux est le suivant :

1. [CLI.py](CLI.py) recoit `/dh`
2. `handle_command()` appelle `_cmd_dh(args)`
3. `_cmd_dh()` detecte le sous-ordre `generate`
4. `_cmd_dh()` appelle `self.cmd.dh_generate(max_mod)`
5. [Command.py](Command.py) retourne `(p, g)`
6. la CLI affiche le modulo et le generateur

### Cas 2 : calcul d'une half key

Quand l'utilisateur tape :

```text
/dh halfkey 23 5 6
```

le flux est le suivant :

1. [CLI.py](CLI.py) parse `mod`, `gen` et eventuellement `priv_a`
2. `_cmd_dh()` appelle `self.cmd.dh_halfkey(mod, gen, priv_a)`
3. [Command.py](Command.py) retourne `(half_key, priv_a)`
4. la CLI affiche la valeur publique partielle et la cle privee utilisee

### Cas 3 : calcul du secret partage

Quand l'utilisateur tape :

```text
/dh secret 23 5 6 8
```

le flux est le suivant :

1. [CLI.py](CLI.py) parse `mod`, `gen`, `priv_a` et `gB`
2. `_cmd_dh()` appelle `self.cmd.dh_secret(mod, gen, priv_a, gB)`
3. [Command.py](Command.py) calcule le secret partage
4. la CLI affiche le resultat

## Gestion des erreurs

La gestion d'erreur actuelle dans [CLI.py](CLI.py) est simple et adaptee a un outil de ligne de commande :

- verification du nombre d'arguments
- verification que les parametres numeriques sont bien des entiers
- affichage d'un message d'usage clair en cas d'erreur

Exemples de controles presents :

- `max_mod doit etre un entier`
- `Les paramètres doivent être des entiers.`
- rappel du bon format de commande quand il manque des arguments

## Pourquoi cette architecture est correcte

Cette implementation est propre pour trois raisons.

### 1. La logique Diffie-Hellman est centralisee

Les calculs sont dans [Command.py](Command.py), pas disperses dans la CLI.

### 2. La CLI reste une couche d'orchestration

[CLI.py](CLI.py) ne fait pas les operations mathematiques. Elle :

- lit la commande utilisateur
- convertit les arguments
- appelle la bonne methode
- affiche le resultat

### 3. La feature est reusable

Comme la logique est dans [Command.py](Command.py), elle pourra etre reutilisee plus tard par :

- la GUI
- des tests unitaires
- un autre point d'entree du projet

## Exemple complet d'echange

Prenons cet exemple :

- modulo : `23`
- generateur : `5`
- secret prive de A : `6`
- secret prive de B : `15`

Calcul des valeurs publiques partielles :

- A calcule $A = 5^6 \bmod 23 = 8$
- B calcule $B = 5^{15} \bmod 23 = 19$

Calcul du secret partage :

- A calcule $s = 19^6 \bmod 23 = 2$
- B calcule $s = 8^{15} \bmod 23 = 2$

Les deux obtiennent bien le meme secret.

En CLI, cela se traduit par exemple par :

```text
/dh halfkey 23 5 6
/dh halfkey 23 5 15
/dh secret 23 5 6 19
/dh secret 23 5 15 8
```

Les deux commandes `/dh secret` doivent afficher la meme valeur finale.

## Validation logique

Le chemin d'execution est coherent avec l'architecture du projet :

- commande utilisateur dans [CLI.py](CLI.py)
- appel au moteur dans [Command.py](Command.py)
- calculs avec `pow(..., ..., ...)`
- affichage du resultat dans la CLI

## Resume

La feature Diffie-Hellman consiste a ajouter un mecanisme de generation de parametres, de calcul de cle publique partielle et de secret partage dans le projet.

Elle a ete implementee en separant clairement :

- la logique mathematique dans [Command.py](Command.py)
- l'appel utilisateur dans [CLI.py](CLI.py)

Cette architecture est simple, lisible, et coherente avec le reste du projet.