# Module de commentaires pour Geotribu

Scripts et fichiers de configuration du module de commentaires du site de Geotribu, basé sur [isso](https://posativ.org/isso/) ([dépôt GitHub](https://github.com/posativ/isso)).

## Liens utiles

- URL de base de l'API de commentaires : <https://comments.geotribu.fr/>
- Interface d'administration : <https://comments.geotribu.fr/admin>
- voir aussi le [ticket sur la configuration dans MkDocs](https://github.com/squidfunk/mkdocs-material/issues/1466#issuecomment-810391442)

----

## Développement en local

1. Cloner le dépôt
2. Créer un environnement virtuel et l'activer :

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. Y installer les dépendances :

    ```bash
    python -m pip install -U pip setuptools wheel
    python -m pip install -U -r requirements.txt
    ```

4. Lancer l'exécution en local :

    ```bash
    isso -c isso-dev.cfg run
    ```

L'outil est accessible sur <http://localhost:8500/>.

Pour l'activer en local dans le site de Geotribu :

1. Lancer le site en local (voir [le guide dédié](https://static.geotribu.fr/contribuer/edit/local_edition_setup/))
2. Adapter l'URL dans [la configuration de MkDocs](https://github.com/geotribu/website/blob/master/mkdocs.yml#L111) du site. Par exemple : `comments_url=http://localhost:8500`

----

## Configuration au niveau de Gandi

### Sous-domaine

Créer un enregistrement DNS de type `A` :

```txt
comments 600 IN A 185.123.84.13
```

> Lien vers l'[interface de gestion](https://admin.gandi.net/domain/5e42db82-6b7c-11ea-8925-00163ea99cff/geotribu.fr/records)

### Compte email

Pour pouvoir envoyer des notifications, on utilise un compte email lié au domaine : <facteur@geotribu.fr>.

> Lien vers l'[interface de gestion](https://admin.gandi.net/domain/5e42db82-6b7c-11ea-8925-00163ea99cff/geotribu.fr/mail/mailboxes/5a52d348-6cbf-42f9-ab0f-7f9f21c9a8c0/edit)

----

## Déploiement

Le module est déployé sur le serveur prêté par GeoRezo, aux côtés du [mini-CDN de Geotribu](https://github.com/geotribu/minimalist-cdn) et d'[El Geo Paso](https://github.com/Guts/elgeopaso).

### Installation

Etapes suivies, dans le cas d'un environnement Apache et mod_wsgi déjà configuré pour les besoins d'El Geo Paso (voir [la documentation](https://elgeopaso.readthedocs.io/fr/latest/deployment/apache.html)) :

```bash
cd /var/www/geotribu
mkdir comments
cd comments/
python3.7 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -U isso gevent
python -m pip install -U mod-wsgi==4.7.*
```

### Configuration Isso

Copier les fichiers `isso-prod.cfg` et `isso-wsgi.py` sur le serveur dans `/var/www/geotribu/comments`.

#### Sécurité des secrets

Paramètres à ne jamais stocker dans le dépôt ou diffuser :

- `[admin]` : `password` : mot de passe d'accès à l'interface d'administration
- `[hash]` : `salt` : chaîne de caractères aléatoire (générée avec le [module secrets de Python](https://docs.python.org/3/library/secrets.html)) utilisée pour renforcer les identifiants face aux grilles du type [Rainbow Tables](https://fr.wikipedia.org/wiki/Rainbow_table)
- `[smtp]` : `password` : mot de passe du compte email

### Configuration Apache

> TO DOC

#### Ressources

> TO DOC

### Certificat SSL

> TO DOC

#### Ressources

- erreur [Name duplicates previous WSGI daemon definition.](https://github.com/certbot/certbot/issues/4880)

----

## Stockage et sauvegarde

La base de données des commentaires est dans le CDN, ainsi que l'export des commentaires de Disqus : <https://cdn.geotribu.fr/tinyfilemanager.php?p=commentaires>.

De cette façon, elle est accessible par l'équipe (les commentaires sont publics de toute façon) et surtout intégrée au [processus de sauvegarde du CDN](https://github.com/geotribu/minimalist-cdn#script-de-sauvegarde).
