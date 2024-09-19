-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost:3306
-- Tiempo de generación: 26-07-2024 a las 21:51:18
-- Versión del servidor: 8.0.30
-- Versión de PHP: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `disponibilidad_equipos`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `equipo`
--

CREATE TABLE `equipo` (
  `idEquipo` int NOT NULL,
  `estadoEquipo` varchar(256) NOT NULL,
  `sala` varchar(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `equipo`
--

INSERT INTO `equipo` (`idEquipo`, `estadoEquipo`, `sala`) VALUES
(1, 'usado', 'D507'),
(2, 'libre', 'D507'),
(3, 'libre', 'D507'),
(4, 'libre', 'D507'),
(5, 'libre', 'D507'),
(6, 'libre', 'D507'),
(7, 'libre', 'D507'),
(8, 'libre', 'D507'),
(9, 'libre', 'D507'),
(10, 'libre', 'D507'),
(11, 'libre', 'D507'),
(12, 'libre', 'D507'),
(13, 'libre', 'D507'),
(14, 'libre', 'D507'),
(15, 'libre', 'D507'),
(16, 'libre', 'D507'),
(17, 'libre', 'D507'),
(18, 'libre', 'D507'),
(19, 'libre', 'D507'),
(20, 'libre', 'D507'),
(21, 'libre', 'D507'),
(22, 'libre', 'D507'),
(23, 'libre', 'D507'),
(24, 'libre', 'D507'),
(25, 'libre', 'D507'),
(26, 'libre', 'D507'),
(27, 'libre', 'D507'),
(28, 'libre', 'D507'),
(29, 'libre', 'D507'),
(30, 'libre', 'D507'),
(31, 'libre', 'D507'),
(32, 'libre', 'D507'),
(33, 'libre', 'D507'),
(34, 'libre', 'D507'),
(35, 'libre', 'D507'),
(36, 'libre', 'D507'),
(37, 'libre', 'D507'),
(38, 'libre', 'D507'),
(39, 'libre', 'D507'),
(40, 'libre', 'D507'),
(41, 'libre', 'D507'),
(42, 'libre', 'D507'),
(43, 'libre', 'D507'),
(44, 'libre', 'D507'),
(45, 'libre', 'D507'),
(46, 'libre', 'D507'),
(47, 'libre', 'D507'),
(48, 'libre', 'D507'),
(49, 'libre', 'D507'),
(50, 'libre', 'D507'),
(51, 'libre', 'D507'),
(52, 'libre', 'D507'),
(53, 'libre', 'D507'),
(54, 'libre', 'D507'),
(55, 'libre', 'D507'),
(56, 'libre', 'D507'),
(57, 'libre', 'D507'),
(58, 'libre', 'D507'),
(59, 'libre', 'D507'),
(60, 'libre', 'D507'),
(61, 'libre', 'D507'),
(62, 'libre', 'D507'),
(63, 'libre', 'D507'),
(64, 'libre', 'D507'),
(65, 'libre', 'D507'),
(66, 'libre', 'D507'),
(67, 'libre', 'D507'),
(68, 'libre', 'D507'),
(101, 'usado', 'H405'),
(102, 'libre', 'H405'),
(103, 'libre', 'H405'),
(104, 'libre', 'H405'),
(105, 'libre', 'H405'),
(106, 'libre', 'H405'),
(107, 'libre', 'H405'),
(108, 'libre', 'H405'),
(109, 'libre', 'H405'),
(110, 'libre', 'H405'),
(111, 'libre', 'H405'),
(112, 'libre', 'H405'),
(113, 'libre', 'H405'),
(114, 'libre', 'H405'),
(115, 'libre', 'H405'),
(116, 'libre', 'H405'),
(117, 'libre', 'H405'),
(118, 'libre', 'H405'),
(119, 'libre', 'H405'),
(120, 'libre', 'H405'),
(121, 'libre', 'H405'),
(122, 'libre', 'H405'),
(123, 'libre', 'H405'),
(124, 'libre', 'H405'),
(125, 'libre', 'H405'),
(126, 'libre', 'H405'),
(127, 'libre', 'H405'),
(128, 'libre', 'H405'),
(129, 'libre', 'H405'),
(130, 'libre', 'H405'),
(131, 'libre', 'H405'),
(132, 'libre', 'H405'),
(133, 'libre', 'H405'),
(134, 'libre', 'H405'),
(201, 'usado', 'I408'),
(202, 'libre', 'I408'),
(203, 'libre', 'I408'),
(204, 'libre', 'I408'),
(205, 'libre', 'I408'),
(206, 'libre', 'I408'),
(207, 'libre', 'I408'),
(208, 'libre', 'I408'),
(209, 'libre', 'I408'),
(210, 'libre', 'I408'),
(211, 'libre', 'I408'),
(212, 'libre', 'I408'),
(213, 'libre', 'I408'),
(214, 'libre', 'I408'),
(215, 'libre', 'I408'),
(216, 'libre', 'I408'),
(217, 'libre', 'I408'),
(218, 'libre', 'I408'),
(219, 'libre', 'I408'),
(220, 'libre', 'I408'),
(221, 'libre', 'I408'),
(222, 'libre', 'I408'),
(223, 'libre', 'I408'),
(224, 'libre', 'I408');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `facultad`
--

CREATE TABLE `facultad` (
  `idFacultad` int NOT NULL,
  `nombreFacultad` varchar(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `facultad`
--

INSERT INTO `facultad` (`idFacultad`, `nombreFacultad`) VALUES
(1, 'administrativo');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `historial`
--

CREATE TABLE `historial` (
  `Usuario_idUsuario` int NOT NULL,
  `fecha` date NOT NULL,
  `horaInicio` datetime NOT NULL,
  `horaFin` varchar(256) DEFAULT NULL,
  `Equipo_idEquipo` int NOT NULL,
  `nombreSala` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `idUsuario` int NOT NULL,
  `usuario` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `contraseña` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `nombreUsuario` varchar(256) NOT NULL,
  `identificacionUsuario` varchar(256) NOT NULL,
  `Facultad_idFacultad` varchar(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`idUsuario`, `usuario`, `contraseña`, `nombreUsuario`, `identificacionUsuario`, `Facultad_idFacultad`) VALUES
(1, 'administrador', 'scrypt:32768:8:1$w4Zb2voUVUf4ARlE$f1eb9223580e59f8f534abae8466a59c42dc765a62abeb456e38530a54808a345c508f7a62193d7a17102fe92833eed7c71cf610018ff35bd2571990cb28c6f4', 'Adminsitrador', '1', '1'),
(2, NULL, NULL, 'Jorge Ivan Molano', '1234567891', '1'),
(3, NULL, NULL, 'ssss', '44', '1');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `equipo`
--
ALTER TABLE `equipo`
  ADD PRIMARY KEY (`idEquipo`);

--
-- Indices de la tabla `facultad`
--
ALTER TABLE `facultad`
  ADD PRIMARY KEY (`idFacultad`);

--
-- Indices de la tabla `historial`
--
ALTER TABLE `historial`
  ADD PRIMARY KEY (`Usuario_idUsuario`,`Equipo_idEquipo`),
  ADD KEY `Equipo_idEquipo` (`Equipo_idEquipo`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`idUsuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `equipo`
--
ALTER TABLE `equipo`
  MODIFY `idEquipo` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=225;

--
-- AUTO_INCREMENT de la tabla `facultad`
--
ALTER TABLE `facultad`
  MODIFY `idFacultad` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `idUsuario` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `historial`
--
ALTER TABLE `historial`
  ADD CONSTRAINT `historial_ibfk_1` FOREIGN KEY (`Usuario_idUsuario`) REFERENCES `usuario` (`idUsuario`),
  ADD CONSTRAINT `historial_ibfk_2` FOREIGN KEY (`Equipo_idEquipo`) REFERENCES `equipo` (`idEquipo`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
