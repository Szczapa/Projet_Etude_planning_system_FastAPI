-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : jeu. 11 mai 2023 à 22:46
-- Version du serveur :  10.4.18-MariaDB
-- Version de PHP : 8.0.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `teamwork_management`
--

-- --------------------------------------------------------

--
-- Structure de la table `activities`
--

CREATE TABLE `activities` (
  `id` int(11) NOT NULL,
  `planning_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `date` date NOT NULL,
  `place` varchar(255) NOT NULL,
  `creator_id` int(11) NOT NULL,
  `company_id` int(11) NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `activities`
--

INSERT INTO `activities` (`id`, `planning_id`, `name`, `date`, `place`, `creator_id`, `company_id`, `start_time`, `end_time`) VALUES
(1, 3, 'belle activité', '2023-05-11', 'Lille', 6, 1, '00:00:00', '00:00:00'),
(2, 3, 'Une belle activité', '2023-05-11', 'moncul', 6, 1, '00:00:00', '00:00:00'),
(4, 3, 'une activité', '2023-05-11', 'lille', 6, 1, '00:00:00', '00:00:00');

-- --------------------------------------------------------

--
-- Structure de la table `activity_participants`
--

CREATE TABLE `activity_participants` (
  `id` int(11) NOT NULL,
  `activity_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Structure de la table `companies`
--

CREATE TABLE `companies` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `companies`
--

INSERT INTO `companies` (`id`, `name`) VALUES
(1, 'Super_Box'),
(2, 'Super_Haricot'),
(3, 'Roberto');

-- --------------------------------------------------------

--
-- Structure de la table `plannings`
--

CREATE TABLE `plannings` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `creator` int(11) NOT NULL,
  `company_id` int(11) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `plannings`
--

INSERT INTO `plannings` (`id`, `name`, `creator`, `company_id`, `start_date`, `end_date`) VALUES
(1, 'string', 6, 1, '2023-05-06', '2023-05-06'),
(3, 'string', 6, 1, '2023-05-07', '2023-05-07');

-- --------------------------------------------------------

--
-- Structure de la table `planning_participant`
--

CREATE TABLE `planning_participant` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `planning_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `planning_participant`
--

INSERT INTO `planning_participant` (`id`, `user_id`, `planning_id`) VALUES
(2, 6, 1),
(5, 6, 3);

-- --------------------------------------------------------

--
-- Structure de la table `planning_user`
--

CREATE TABLE `planning_user` (
  `id` int(11) NOT NULL,
  `userid` int(11) NOT NULL,
  `planningid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Structure de la table `roles`
--

CREATE TABLE `roles` (
  `id` int(11) NOT NULL,
  `role` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `roles`
--

INSERT INTO `roles` (`id`, `role`) VALUES
(1, 'User'),
(2, 'Admin'),
(3, 'Maintainer');

-- --------------------------------------------------------

--
-- Structure de la table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role_id` int(11) NOT NULL,
  `company_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password`, `role_id`, `company_id`) VALUES
(6, 'Admin', 'Admin@admin.fr', '$2b$12$etTbQpnUidM7U3JbaooqLOtLaIyMUSJu37x6.5fclZnPeY.TZC3t2', 2, 1),
(7, 'Jean', 'jean@jean.fr', '$2b$12$wPJk8C/xr4B1ej0CFOGxLewJzZaO4YvYj3buWKlbBFqQE2.WyPWZO', 1, 1),
(8, 'string', 'string', '$2b$12$u4pZrsBdGklgNa8UjUSqeOOn9Upj2W.k2A69YvGjG1rvaQUdypllC', 1, 1),
(11, 'Maintainer', 'Maintainer@maintainer.fr', '$2b$12$eNp5vIp.vf9XiaxU8FhOReSfE0ZCPb7wevWepUWorQasYI6pXDNpO', 3, 0),
(13, 'robert', 'robert@admin.fr', '$2b$12$wkC01/HUrqWB/IEaAVduKOzHCBGKUJwFoIAoGkENjqut6lCu96f42', 2, 3);

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `activities`
--
ALTER TABLE `activities`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `activity_participants`
--
ALTER TABLE `activity_participants`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_activity_participants_id` (`id`),
  ADD KEY `ix_activity_participants_user_id` (`user_id`),
  ADD KEY `ix_activity_participants_activity_id` (`activity_id`);

--
-- Index pour la table `companies`
--
ALTER TABLE `companies`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `plannings`
--
ALTER TABLE `plannings`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `planning_participant`
--
ALTER TABLE `planning_participant`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `planning_user`
--
ALTER TABLE `planning_user`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD KEY `role_id` (`role_id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `activities`
--
ALTER TABLE `activities`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT pour la table `activity_participants`
--
ALTER TABLE `activity_participants`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT pour la table `companies`
--
ALTER TABLE `companies`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT pour la table `plannings`
--
ALTER TABLE `plannings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT pour la table `planning_participant`
--
ALTER TABLE `planning_participant`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT pour la table `planning_user`
--
ALTER TABLE `planning_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `roles`
--
ALTER TABLE `roles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT pour la table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
