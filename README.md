# Planning System V1

Dans le cadre de la dernière année de licence nous avons était ammené à réaliser un Systeme de Planning sous language Python.
Pour y parvenir nous avons utilisé l'api FastApi afin de permettre la gestion des fonctionnalités du projet.

## Deployment

Lien du git :

```bash
  https://github.com/Szczapa/planning_system.git
```

Pour déployer le projet voici la commande à entrer :

```bash
  docker-compose up --build
```

# Log Base de donnée

Comment initialiser la Base de données ?

Url phpmyadmin :

```bash
    http://localhost:8080/
```

```bash
    Username : Root
```

```bash
    Password : Root
```

# Accès à l'api FAST API

```bash
  http://localhost:81/docs
```

# Générale

- Auto création de la base de données et installation des dépendances
- Données sensible Chiffré ou hashé + salage
- Token JWT sur les connections utilisateurs
- Vérification des droits à chaque éxécution

# Maintainer

- Gestion total des users
- Gestion des entreprises
- Fullscreen mode
- Cross platform

# Admin

- Modification des users
- Gestion des plannings
- Gestion des Activités

# User

- Rejoindre / Quitter Planning
- Création d'activité
- Gestion des participants à son activité

## Tech Stack

- **Server:** - Mariadb, Apache, FastApi
- **Extentions:** - Bcrypt, Fernet, jwt, sqlalchemy, pydantic

## Tableau des utilisateurs :

| Entreprise    | Rôle       | Nom d'utilisateur | E-mail                 | Mot de passe |
| ------------- | ---------- | ----------------- | ---------------------- | ------------ |
| x             | Maintainer | Maintainer        | Maintainer@gestion.fr  | Maintainer   |
| SuperBox      | Admin      | charles-henry     | CharlesH@SuperBox.com  | Charles1234  |
| SuperBox      | Admin      | Robert            | Robert@SuperBox.com    | Robert1234   |
| SuperBox      | User       | Jhon              | Jhon@SuperBox.com      | Jhon1234     |
| Super_Haricot | Admin      | Sophie            | sophie@superharicot.fr | Sophie1234   |
| Super_Haricot | User       | Lucas             | lucas@superharicot.fr  | Lucas1234    |
| Super_Haricot | User       | Emma              | emma@superharicot.fr   | John1234     |
| Super_Haricot | User       | John              | john@superharicot.fr   | Emma1234     |
| Super_cars    | Admin      | Thomas            | thomas@supercars.fr    | Thomas1234   |
| Super_cars    | User       | Laura             | laura@supercars.fr     | Laura1234    |
| Super_cars    | User       | David             | david@supercars.fr     | David1234    |
| Super_cars    | User       | Sarah             | sarah@supercars.fr     | Sarah1234    |

## Authors

- [@Szczapa](https://github.com/Szczapa)
