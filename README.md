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

## Fonctionement des Routers :

# Activity

- Get :

  - /activities: Récupères toutes les activités de l'entreprise
  - /activity/{activity_id}: Récupère l'activité à l'id spécifié + vérification d'existance et de présence dans l'entreprise

- Post:

  - /activity/{planning_id}: Créé l'activité avec les critères suivant
    - Nom
    - planning_id
    - creator_id : Automatique
    - company_id : Automatique
    - date : jour actuel ou à entré à la main
    - start_time : a entrer au format HH:MM:SS
    - end_time : a entrer au format HH:MM:SS
  - /activity/{activity_id}/join: Rejoins l'activité spécifié + vérification d'existance + vérification de présence dans le planning lié à l'activité
  
- Delete :
  - /activity/{activity_id}/delete: supprime l'activité à l'id noté + vérification d'existance dans l'entreprise + vérification des droits
  - /activity/{activity_id}/leave/{user_id} Retire l'utilisateur de la liste des participants + vérification de présence dans l'activité + existance de l'activité

## État actuelle des Activités :

| id  | planning_id                    | name | date       | place | crator_id | company_di | start_time | end_time |
| --- | ------------------------------ | ---- | ---------- | ----- | --------- | ---------- | ---------- | -------- |
| 1   | Dernier cours de développement | 2    | 2023-05-16 | Lille | 1         | 1          | 08:00:00   | 13:00:00 |

## État actuelle des Pariticipants aux Activités :

| id  | activity_id | user_id |
| --- | ----------- | ------- |
| 1   | 1           | 2       |

# Company : Uniquement disponible au role Maintainer

    - Get :
      - /companies: Récupère la totalité des entreprises enregitrées.
      -/company/{company_id}: Récupère l'entreprise à partir de son id.

    - Post :
      - /company: créé l'entreprise avec le nom données + comparaison de non existance.

    - Delete :
      - /company/{company_id}: supprime l'entreprise à partir de son id.

## État actuelle des Entreprises :

| id  | Nom             |
| --- | --------------- |
| 1   | Super_Box       |
| 2   | Super_Haricot   |
| 3   | Super_cars      |
| 4   | Test_for_delete |

# login

    - Post :
      - /login: Récupère le username de l'utilisateur **EMAIL** & le mot de passes , les déchiffres et les compares à
        ceux en base de données, si ça correspond alors il y a création d'un Token JWT pour certifier l'authentification de l'utilisateur.
    - Get :
      - /me: Retourne toute les informations du User connecté.

# planning

    - Get :
      - /plannings: Retourne la totalité des plannings qui appartiennent à l'entreprise du User.
      - /planning/{planning_id}/participants: Retourne la totalité des participants si le User à le role Admin, sinon il retourne le nombre d'inscrit au planning.

    - Post:
      -/planning: Créé le planning avec les critères suivant :
        - Nom
        - creator_id : Automatique
        - company_id : Automatique
      - /planning/{planning_id}/join: Rejoint le planning avec l'id concerné, Uniquement valable pour l'entreprise du User.
      
    - Delete:
      - /planning/{planning_id}/delete: Supprime le planning avec l'id concerné, Uniquement valable pour les Admin & dans l'entreprise de l'admin.
      - /planning/{planning_id}/leave/{user_id} Supprime l'utilisateur du planning si il est dans l'entreprise + Admin only

## État actuelle des Plannings :

| id  | name                | crator | company_id |
| --- | ------------------- | ------ | ---------- |
| 1   | développement Front | 2      | 1          |
| 2   | développement Back  | 2      | 1          |
| 3   | Exemple pour delete | 2      | 1          |
| 4   | Création de dessin  | 5      | 2          |
| 5   | Administration User | 9      | 3          |

# role

    - Get :
      - /roles: Affiche tout les roles uniquement role Maintainer
      

## État actuelle des Roles :

| id  | Nom        |
| --- | ---------- |
| 1   | User       |
| 2   | Admin      |
| 3   | Maintainer |

# user

    - Get :
      - /users: Récupères tout les users de l'entreprise de l'utilisateur.
      - /user/{user_id}: Récupère l'utilisateur avec l'id concerné

    - Post:
      - /user: Création de l'utilisateur, Uniquement disponible au Maintainer, Si le role n'existe pas = erreur, si role oublié utilisteur au rend de User par défaut.
        cryptage & salage du mot de passe + chiffrage du mail et du Username.
    - Delete:
      -/user/{user_id}: Supprime l'utilisateur avec l'id concerné, maintainer toute les entreprises & admin limité à son entreprise

## Tableau des utilisateurs inscrit :

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

## Evaluation grid

### 1. Structure du projet et organisation du code (35 points)

- [x] README.md clair et bien documenté (sachant qu'un README ne me permettant pas d'exécuter le code entrainera une réduction de la note globale de 33%) (5 points)
- [x] Organisation des fichiers et dossiers (5 points)
- [x] Utilisation appropriée des modules et packages (5 points)
- [ ] Lisibilité et propreté du code (10 points)
- [ ] Commentaires lisibles et faisant sens (5 points)
- [x] Bonne utilisation du git (commits de bonne taille, messages faisant sens) (5 points)

### 2. Implémentation des standards appris en cours (35 points)

- [x] Utilisation de pydantic (5 points)
- [x] Section d'import bien formaté (system, libs, local), et chemins absolus et non relatifs Requirements.py avec versions fixes (5 points)
- [x] Définition du type de donnée en retour des fonctions. (5 points)
- [x] Bonne utilisation des path & query parameters (10 points)
- [x] Retour des bons codes HTTP (10 points)

### 3. Implémentation des fonctionnalités demandées (85 points)

- [x] Connexion à la base de données (30 points)
- [x] Gestion des utilisateurs (15 points)
- [x] Gestion des plannings (15 points)
- [x] Gestion des activités (15 points)
- [x] Gestion des entreprises (10 points)

### 4. Sécurité (20 points)

- [x] Utilisation de tokens pour l'authentification (JWT) (5 points)
- [x] Validation et vérification des données entrantes avec modèles pydantics, not (5 points)
- [x] Gestion des erreurs et exceptions (5 points)
- [x] Sécurisation de la connexion à la base de données (5 points)

## Authors

- [@Szczapa](https://github.com/Szczapa)
