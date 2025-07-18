-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Creato il: Lug 18, 2025 alle 17:57
-- Versione del server: 8.0.18
-- Versione PHP: 7.4.5

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `agrilogic`
--

-- --------------------------------------------------------

--
-- Struttura della tabella `assegna`
--

CREATE TABLE `assegna` (
  `id_utente` int(11) NOT NULL,
  `id_mansione` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dump dei dati per la tabella `assegna`
--

INSERT INTO `assegna` (`id_utente`, `id_mansione`) VALUES
(2, 3),
(2, 4),
(2, 5);

-- --------------------------------------------------------

--
-- Struttura della tabella `coltiva`
--

CREATE TABLE `coltiva` (
  `id` int(11) NOT NULL,
  `id_coltura` int(11) NOT NULL,
  `id_terreno` int(11) NOT NULL,
  `dataSeminazione` date NOT NULL,
  `dataRaccolta` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dump dei dati per la tabella `coltiva`
--

INSERT INTO `coltiva` (`id`, `id_coltura`, `id_terreno`, `dataSeminazione`, `dataRaccolta`) VALUES
(1, 1, 1, '2025-07-09', '2025-07-30'),
(2, 1, 1, '2025-07-16', '2025-07-17'),
(3, 1, 2, '2025-07-02', '2025-07-31'),
(4, 1, 3, '2025-07-17', NULL),
(5, 1, 3, '2025-07-17', '2025-07-17'),
(6, 1, 4, '2025-07-17', NULL),
(7, 1, 4, '2025-07-17', '2025-07-17'),
(8, 1, 2, '2025-07-22', '2025-07-18'),
(9, 1, 5, '2025-07-18', '2025-07-18'),
(10, 1, 6, '2025-07-18', NULL),
(11, 1, 6, '2025-07-18', NULL);

-- --------------------------------------------------------

--
-- Struttura della tabella `coltura`
--

CREATE TABLE `coltura` (
  `id` int(11) NOT NULL,
  `nome` varchar(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dump dei dati per la tabella `coltura`
--

INSERT INTO `coltura` (`id`, `nome`) VALUES
(1, 'carota'),
(2, 'pomodoro');

-- --------------------------------------------------------

--
-- Struttura della tabella `contiene`
--

CREATE TABLE `contiene` (
  `id_magazzino` int(11) NOT NULL,
  `id_prodotto` int(11) NOT NULL,
  `id` int(11) NOT NULL,
  `dataImmagazzinazione` date NOT NULL,
  `dataScadenza` date NOT NULL,
  `quantita` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dump dei dati per la tabella `contiene`
--

INSERT INTO `contiene` (`id_magazzino`, `id_prodotto`, `id`, `dataImmagazzinazione`, `dataScadenza`, `quantita`) VALUES
(2, 1, 5, '2025-07-18', '2025-07-20', 3),
(2, 2, 7, '2025-07-18', '2025-07-21', 3);

-- --------------------------------------------------------

--
-- Struttura della tabella `magazzino`
--

CREATE TABLE `magazzino` (
  `id` int(11) NOT NULL,
  `metratura` int(11) NOT NULL,
  `capienza` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dump dei dati per la tabella `magazzino`
--

INSERT INTO `magazzino` (`id`, `metratura`, `capienza`) VALUES
(2, 34, 234),
(3, 5, 8);

-- --------------------------------------------------------

--
-- Struttura della tabella `mansione`
--

CREATE TABLE `mansione` (
  `id` int(11) NOT NULL,
  `tipo` enum('FISSA','GIORNALIERA') NOT NULL,
  `stato` enum('COMPLETATA','IN_ATTESA','IN_CORSO') NOT NULL,
  `descrizione` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dump dei dati per la tabella `mansione`
--

INSERT INTO `mansione` (`id`, `tipo`, `stato`, `descrizione`) VALUES
(1, 'FISSA', 'COMPLETATA', 'GESTIONE_MAGAZZINO'),
(2, 'FISSA', 'IN_ATTESA', 'ijijj'),
(3, 'FISSA', 'COMPLETATA', 'GESTIONE_MAGAZZINO'),
(4, 'GIORNALIERA', 'COMPLETATA', 'GESTIONE_TERRENO'),
(5, 'GIORNALIERA', 'COMPLETATA', 'GESTIONE_TERRENO'),
(6, 'GIORNALIERA', 'COMPLETATA', 'GESTIONE_TERRENO');

-- --------------------------------------------------------

--
-- Struttura della tabella `prodotto`
--

CREATE TABLE `prodotto` (
  `id` int(11) NOT NULL,
  `nome` varchar(50) NOT NULL,
  `codice` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dump dei dati per la tabella `prodotto`
--

INSERT INTO `prodotto` (`id`, `nome`, `codice`) VALUES
(1, 'pomodoro', 'AAAAb'),
(2, 'carota', 'SADAD');

-- --------------------------------------------------------

--
-- Struttura della tabella `terreno`
--

CREATE TABLE `terreno` (
  `id` int(11) NOT NULL,
  `livelloIrrigazione` int(11) NOT NULL,
  `stato` enum('CRESCITA','MATURO','VUOTO') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dump dei dati per la tabella `terreno`
--

INSERT INTO `terreno` (`id`, `livelloIrrigazione`, `stato`) VALUES
(1, 100, 'CRESCITA'),
(2, 68, 'MATURO'),
(3, 100, 'VUOTO'),
(4, 80, 'VUOTO'),
(5, 45, 'VUOTO'),
(6, 23, 'VUOTO');

-- --------------------------------------------------------

--
-- Struttura della tabella `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `nome` varchar(50) NOT NULL,
  `cognome` varchar(50) NOT NULL,
  `ruolo` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `mansioniAssegnate` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dump dei dati per la tabella `user`
--

INSERT INTO `user` (`id`, `nome`, `cognome`, `ruolo`, `email`, `password`, `mansioniAssegnate`) VALUES
(2, 'thomas', 'carotti', 'dipendente', 'a', 'a', 1),
(3, 'michele', 'del moro', 'amministratore', 'b', 'b', NULL);

--
-- Indici per le tabelle scaricate
--

--
-- Indici per le tabelle `assegna`
--
ALTER TABLE `assegna`
  ADD PRIMARY KEY (`id_utente`,`id_mansione`),
  ADD KEY `assegna mansione` (`id_mansione`);

--
-- Indici per le tabelle `coltiva`
--
ALTER TABLE `coltiva`
  ADD PRIMARY KEY (`id`),
  ADD KEY `coltiva terreno` (`id_terreno`),
  ADD KEY `coltiva coltura` (`id_coltura`);

--
-- Indici per le tabelle `coltura`
--
ALTER TABLE `coltura`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nome` (`nome`);

--
-- Indici per le tabelle `contiene`
--
ALTER TABLE `contiene`
  ADD PRIMARY KEY (`id`),
  ADD KEY `contiene magazzino` (`id_magazzino`),
  ADD KEY `contiene prodotto` (`id_prodotto`);

--
-- Indici per le tabelle `magazzino`
--
ALTER TABLE `magazzino`
  ADD PRIMARY KEY (`id`);

--
-- Indici per le tabelle `mansione`
--
ALTER TABLE `mansione`
  ADD PRIMARY KEY (`id`);

--
-- Indici per le tabelle `prodotto`
--
ALTER TABLE `prodotto`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `codice` (`codice`);

--
-- Indici per le tabelle `terreno`
--
ALTER TABLE `terreno`
  ADD PRIMARY KEY (`id`);

--
-- Indici per le tabelle `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `mansione assegnata` (`mansioniAssegnate`);

--
-- AUTO_INCREMENT per le tabelle scaricate
--

--
-- AUTO_INCREMENT per la tabella `coltiva`
--
ALTER TABLE `coltiva`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT per la tabella `coltura`
--
ALTER TABLE `coltura`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT per la tabella `contiene`
--
ALTER TABLE `contiene`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT per la tabella `magazzino`
--
ALTER TABLE `magazzino`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT per la tabella `mansione`
--
ALTER TABLE `mansione`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT per la tabella `prodotto`
--
ALTER TABLE `prodotto`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT per la tabella `terreno`
--
ALTER TABLE `terreno`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT per la tabella `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Limiti per le tabelle scaricate
--

--
-- Limiti per la tabella `assegna`
--
ALTER TABLE `assegna`
  ADD CONSTRAINT `assegna dipendente` FOREIGN KEY (`id_utente`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `assegna mansione` FOREIGN KEY (`id_mansione`) REFERENCES `mansione` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Limiti per la tabella `coltiva`
--
ALTER TABLE `coltiva`
  ADD CONSTRAINT `coltiva coltura` FOREIGN KEY (`id_coltura`) REFERENCES `coltura` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `coltiva terreno` FOREIGN KEY (`id_terreno`) REFERENCES `terreno` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Limiti per la tabella `contiene`
--
ALTER TABLE `contiene`
  ADD CONSTRAINT `contiene magazzino` FOREIGN KEY (`id_magazzino`) REFERENCES `magazzino` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `contiene prodotto` FOREIGN KEY (`id_prodotto`) REFERENCES `prodotto` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
