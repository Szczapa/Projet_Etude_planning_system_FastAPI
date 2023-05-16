-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : db
-- Généré le : mar. 16 mai 2023 à 20:14
-- Version du serveur : 5.7.42
-- Version de PHP : 8.1.17

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
CREATE DATABASE IF NOT EXISTS `teamwork_management` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `teamwork_management`;

-- --------------------------------------------------------

--
-- Structure de la table `activities`
--

DROP TABLE IF EXISTS `activities`;
CREATE TABLE IF NOT EXISTS `activities` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `planning_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `date` date NOT NULL,
  `place` varchar(255) NOT NULL,
  `creator_id` int(11) NOT NULL,
  `company_id` int(11) NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `activities`
--

INSERT INTO `activities` (`id`, `planning_id`, `name`, `date`, `place`, `creator_id`, `company_id`, `start_time`, `end_time`) VALUES
(1, 1, 'Dernier cours de développement', '2023-05-16', 'Lille', 2, 1, '08:00:00', '13:00:00');

-- --------------------------------------------------------

--
-- Structure de la table `activity_participants`
--

DROP TABLE IF EXISTS `activity_participants`;
CREATE TABLE IF NOT EXISTS `activity_participants` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `activity_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_activity_participants_id` (`id`),
  KEY `ix_activity_participants_user_id` (`user_id`),
  KEY `ix_activity_participants_activity_id` (`activity_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `activity_participants`
--

INSERT INTO `activity_participants` (`id`, `activity_id`, `user_id`) VALUES
(1, 1, 2);

-- --------------------------------------------------------

--
-- Structure de la table `companies`
--

DROP TABLE IF EXISTS `companies`;
CREATE TABLE IF NOT EXISTS `companies` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `companies`
--

INSERT INTO `companies` (`id`, `name`) VALUES
(1, 'Super_Box'),
(2, 'Super_Haricot'),
(3, 'Super_cars'),
(4, 'Test_for_delete');

-- --------------------------------------------------------

--
-- Structure de la table `plannings`
--

DROP TABLE IF EXISTS `plannings`;
CREATE TABLE IF NOT EXISTS `plannings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `creator` int(11) NOT NULL,
  `company_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `plannings`
--

INSERT INTO `plannings` (`id`, `name`, `creator`, `company_id`) VALUES
(1, 'Développement Front', 2, 1),
(2, 'Développement Back', 2, 1),
(3, 'Exemple pour Delete', 2, 1),
(4, 'Création de dessin', 5, 2),
(5, 'Administration User', 9, 3);

-- --------------------------------------------------------

--
-- Structure de la table `planning_participant`
--

DROP TABLE IF EXISTS `planning_participant`;
CREATE TABLE IF NOT EXISTS `planning_participant` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `planning_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `planning_participant`
--

INSERT INTO `planning_participant` (`id`, `user_id`, `planning_id`) VALUES
(1, 2, 1);

-- --------------------------------------------------------

--
-- Structure de la table `roles`
--

DROP TABLE IF EXISTS `roles`;
CREATE TABLE IF NOT EXISTS `roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role` varchar(15) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

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

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role_id` int(11) NOT NULL,
  `company_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `role_id` (`role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password`, `role_id`, `company_id`) VALUES
(1, 'Z0FBQUFBQmtZcEJmbld1VTFhSDE3c0NtNERwcWRnb1E1bjB6LXYyX3dMUnZrZ0tUY0xZMV9iTGFPeDM4empqYzNTb0g0SmU5R1BvbXVuTktBT0JRVVg5QV9fdlVKajdPaHc9PQ==', 'Z0FBQUFBQmtZcEJmaWZhdWRsQ1lpNzRBWUk3Sl9YOTR5SEhKME90SDJPTWVaTGtLdlY2TkNfejBfTEY0bWlHNUxLQUFmYzRjczlSZnNiN01SeEZWWDlVYkk5SFNMWVBHOWhOUXN3NU1VUE55Uk10NmsyNEdoSTQ9', '$2b$12$8Lx7240gWz6SJLyqpuNwDuh6F2ub5.NoO38Dzj8NOSiJDHARtIq2.', 3, 0),
(2, 'Z0FBQUFBQmtZcDZpR2VkWTdYRHVtZFRpVkpTd05BdG90QXM5b0VUTFpGc0tBVzBCN3FRQkMzSV9GZkZvM1B6T1IydDlVb0xObnlkbGE4dUVxYjlWeDNSalpBejE2d1FoOUE9PQ==', 'Z0FBQUFBQmtZcDZpeWRUQzdCczQ1R1podDBvZXNyUjRqdUlsVjBlU2w1d3ZxX3BfUkdQNUFqc0U0cGNYekc5UGY5VWtXd0JRd1Z2TkFGR2s0REI0RG15WkI0WVRDZ29RMWlSZmdUWXNUWmFDSG8wbGx5bTNqS1E9', '$2b$12$g5nmBICkM0B.6S6k2X4tSOmKjkQqi2wXWLLyqc8RWo1t4NvW.NhxC', 2, 1),
(3, 'Z0FBQUFBQmtZcDdsNW9uVkNTVzlNaWN5cXdqY2NNTlRBTXM5ZnpoXy01dUZBU0VVVV9tVUpiT182WUctM2Z6Z3dKb3JBdnJhZW0yNzRDUEZOVkNPZTlnVnhEcjRNVjZYSnc9PQ==', 'Z0FBQUFBQmtZcDdsT1BLTzJSY1lYN0kxa2xNRGtvVl9KQ2xuME55aWxOVTktdXFTeFpRdERiSXRkU2Vma1c3MFlUQl9QdXZWb2tLUjFCcnYzcHBhZHZENGlhZFI2ZVQzU1BCVE5nUHE2eFVCdno2VEVvWkVleEk9', '$2b$12$hRC.RaI/GVmFDj4yRZcZFuo63VlitAuJgyqSPw9NTWOd2KSMiBYsS', 2, 1),
(4, 'Z0FBQUFBQmtZcDhFMDdrRjFsZnJvRFNYN3hZS19hQ2ZoQnFVbllUN0VzRlQ5WUc5ZHFMUk5oZjJueE1PR0xCMV9VeFo3aEtGYWR4NUh6aGJrZE9aSm5MMTVFN1JieloyTEE9PQ==', 'Z0FBQUFBQmtZcDhFSEJjWm1jc0Y2OG1mQWo3OU1oYlQxd2RoTDhpZ1NBMjVwemtWZXl1MXA1X1RsaDVxeXE1M1QtN20yc0ItQ0ItZG8yTkJ2bHVDZS1XRGstZTlad2hTdVhmbVpwYlRZZFdwZ1JxQTRsLVh5T009', '$2b$12$B/y1nmvEBxN9/fjNIxT2I.SZ4OyjIdFEnx.EZ6OFb8ZyP0F3NGsqa', 1, 1),
(5, 'Z0FBQUFBQmtZcUZ0TFJvcTJJNl9TcjZJVUJlZDd3TGs2WEtmNV9VemZEbnJncm44ellSbGZQdi1WSzlVY2NUY1BXdkxyTEx3M1BnVEQwakJLeHAwd0VKNzJ3V0puUkppbmc9PQ==', 'Z0FBQUFBQmtZcUZ0R1F3MjBRZFBDaHJ3bFZvdWtmTExielU5ejNPMllvNU5hT3IwMDFYM1ZoMVpCSG5xVFZYeU15ZTdUdXhIcVhTbTlBUHZ1ZExhSDBXdUEwLXhiaDJxWHpMYmxaVmtHa3ViZjh4QW9KS3pmTXM9', '$2b$12$efeO4MaL9By735Vkw2OYne6E9sbuebdHddpXO690EDcIbbp/YRgem', 2, 2),
(6, 'Z0FBQUFBQmtZcUdFNW9BZlg4R1JNUWtaYkhma18xZ184QXE5MFVVUnZITjZ4MF84RVpMazZrS0dRZ3BMSTMxRmtMUEhuUUhqMlItY3JVNUlZNU1adjhvWEIyVzN5V1RsVFE9PQ==', 'Z0FBQUFBQmtZcUdFYld5X1Z2Y1RxbEFrWHVkV0hMWG5GeW9uNGUyNnZpSWVlcnY1TGNqSE1FNi1rck53aS1zT1B3V0VfcDUyWC1zQWY4LXNHYktibjUwT01xM1FLby1XQ0JyanpuenJ3U3l4VEhJRW95YS04VzA9', '$2b$12$bhamx2O7UwFkLI62Ck45eudFuuaXGPyjLkakYRnQXbptvEh5mF9Bu', 1, 2),
(7, 'Z0FBQUFBQmtZcUdQWktpcjV6Yjhpak02ckdwWUhxMUxuaFdkUU9qWGhyZWZPR24tbGNFU2xTbldCWlRnOXNiSzNIa3ZkZ3l6RDlEUjZVZjFSU2c5SlNmcWc0TEpuTURfX1E9PQ==', 'Z0FBQUFBQmtZcUdQTm5kRnE2R2ZUeVhJN2F4Z0oxZEgtSmRHNkVueXliQXBnekNvVVZTd0V4MG5meEY3MnVwRjdpNGVseUYzR190aHdTRE1rRzJHZERtR3V4MVRCb1FDcVZuTE5XMk5kQllBb2tNRkd4YVVQb1E9', '$2b$12$IV.0zdTZMHpCfkqpZWqQh.mAKUEQnUQ/FvxP/0LUxxOPuOsfkoY3S', 1, 2),
(8, 'Z0FBQUFBQmtZcUdjNkgwZUNCRThhS19lWDVpc1VSMktPUU9UcV9JTFZKTUZITExHNW1jOWdBekFQeWladjZ0cUtSZmo2WnExTWxLM0NMTTlzNWZDLXBqVkx6MnlvbGNZcEE9PQ==', 'Z0FBQUFBQmtZcUdjb3dxSjBFUjZRSzZEQXc4ZnBWRFN1bmxSTHdQYkxCSzJzSklQbTV6b25sQUwzNlh2TXFhcTB0ZXB3ejE1b0FLMmUxTGxrNjZTRFZTT0pLdGpVNW9GdS1WejhRRlhJdmpXQVRnNXRHTGRYOVk9', '$2b$12$jTYoRHndk6p/g2ZsvGmGRe/yfwOsMwnxXytZOpy0JFM/rkMtFV/4e', 1, 2),
(9, 'Z0FBQUFBQmtZcUc2X2NvbVV4RjZDazh3TnhuMXMyMGEwbTRMNEZ6UmFTRUF1Y2tPa3phVkYwVWpGLXpfVl8yaDRYajFGWmlGNXFvQ1R1OHctYW1IWHRNQ2ZFZ2lEbmRKbGc9PQ==', 'Z0FBQUFBQmtZcUc2cTJFM2xtZ0w4MlN4QTl2WDFtY0M5WlhZR0VleFpuRk0xNmFkLTFqd28tVkJIMHlheUJJNmFpb2xjMng3X2Nta1JaOU5VNjFCNk5WMjJoNmI3Uk5oOGplQ3F0em1zU29GcktQb0xHT0dfQzQ9', '$2b$12$gDihp7aAxZEDj09Fp78wpetRSnSU0JzBFoHK6xDWBE98ZeXCGR1Ii', 2, 3),
(10, 'Z0FBQUFBQmtZcUhRaXhJZFNxZmtVWmFEbTllSXZtQTV3Nmx1NG9YakxTX1hKaFVBNl80UVBFeG1fRW45ZzBFNl9zNVVxeHdrT1VFMThEMzZjR0szYUdyZWtMaklpTk12R2c9PQ==', 'Z0FBQUFBQmtZcUhRamZ4SWowbnJBZFZWS1QxSjByN3lfRXVCdEtRMzM3eTFyY0tHMk1CSy1EbmQtQXNDdVVLWjltZjNPekxjRzBqV2tneHJiODQyYW5nc19IY2c4WmJsV01sV2dqZ0t3V3pjRnFKWXI4QTV6RDQ9', '$2b$12$YmSObSxjlHuvSnAuN25m4urXYrO9kBWoCP6FvLk4GfBMbKSOSY2jm', 1, 3),
(11, 'Z0FBQUFBQmtZcUhlTTBHUEhveDllTU5hUjlLcFFhd3BXZnBCYzc0bjhqS1RtQXRzdFVjLVhfRUwzdFpzYnNCU052NHYwSzR0OThhcUl1TUI3a2pfREt4UXdocDVuT3cxS1E9PQ==', 'Z0FBQUFBQmtZcUhlN29SMzZlT0JlazZVbkNtN210ZHhIMlROdjFaeVlZUXFHcEEzTnJJNmY0Mzd0R0pVVXBhd2ZfTGpNUFVUZ1JGNmZmSTVGcU03MUloZzV0Ri1xVXJPWmxZVktkcmJNX0dTMlB1bHNDdDRfYUk9', '$2b$12$r2WM2fnxdV0nVExlLmuJgezoXof/Gbg/U/Hv2.LGdfxoOUKFfhxmS', 1, 3),
(12, 'Z0FBQUFBQmtZcUhuWmZBWnRlSURUeG5pMEtYTjNTRnF4cFdPWnBsYzlDQXMwaGoySFpRVkZjMThOdjNickt0TklPdDgzbjRPclYyQ0RVWk1tUnZYa1FHcjNFNjF0UXpmdXc9PQ==', 'Z0FBQUFBQmtZcUhuWmMzaGZXcjR3ZmthYjd1QlZkWGR5QTh3S2YzNEYzMVFHZ1RDVTV1S3lReTNXaGV5WjJjN3NCRWFUNDBVNzNTTmNjUkczVXZzSXJldFI1RllYdnd0LTc1R2h5Qi05ZGwyWnVHblRVY1F5V1U9', '$2b$12$/M4jERt5SyA1iE.L3BjVTOJrFV9zMTy04TFuSMkKaN9KOIMvV1IYC', 1, 3);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
