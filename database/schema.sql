-- Database per Concessionaria NexDam
-- Importare in phpMyAdmin di XAMPP (o eseguire con mysql client)

CREATE DATABASE IF NOT EXISTS concessionaria CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE concessionaria;

CREATE TABLE IF NOT EXISTS veicoli (
    id INT AUTO_INCREMENT PRIMARY KEY,
    marca VARCHAR(100) NOT NULL,
    modello VARCHAR(100) NOT NULL,
    anno INT NOT NULL,
    prezzo DECIMAL(10,2) NOT NULL,
    km INT NOT NULL DEFAULT 0,
    carburante ENUM('Benzina','Diesel','Elettrica','Hybrid','GPL','Metano') NOT NULL,
    cambio ENUM('Manuale','Automatico') NOT NULL,
    colore VARCHAR(50),
    descrizione TEXT,
    immagine VARCHAR(255) DEFAULT 'default-car.svg',
    disponibile TINYINT(1) NOT NULL DEFAULT 1,
    creato_il TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS richieste_contatto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    telefono VARCHAR(30),
    messaggio TEXT NOT NULL,
    veicolo_id INT NULL,
    creato_il TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    letto TINYINT(1) NOT NULL DEFAULT 0,
    FOREIGN KEY (veicolo_id) REFERENCES veicoli(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL
);

-- Utente admin di default: username "admin" / password "admin123"
-- (l'hash viene generato dallo script seed.py, non inserirlo qui a mano)

-- Dati di esempio
INSERT INTO veicoli (marca, modello, anno, prezzo, km, carburante, cambio, colore, descrizione, immagine, disponibile) VALUES
('Fiat', 'Panda', 2021, 11900.00, 32000, 'Benzina', 'Manuale', 'Bianco', 'Fiat Panda in ottime condizioni, unico proprietario, tagliandi regolari.', 'default-car.svg', 1),
('Volkswagen', 'Golf', 2020, 18500.00, 45000, 'Diesel', 'Manuale', 'Grigio', 'VW Golf 8, full optional, gomme nuove, perfetta per uso quotidiano.', 'default-car.svg', 1),
('Audi', 'A4', 2019, 24900.00, 60000, 'Diesel', 'Automatico', 'Nero', 'Audi A4 Avant, interni in pelle, navigatore, cruise control adattivo.', 'default-car.svg', 1),
('Tesla', 'Model 3', 2022, 38900.00, 15000, 'Elettrica', 'Automatico', 'Bianco', 'Tesla Model 3 Long Range, autopilota incluso, garanzia ancora valida.', 'default-car.svg', 1),
('Toyota', 'Yaris', 2021, 15900.00, 28000, 'Hybrid', 'Automatico', 'Rosso', 'Toyota Yaris Hybrid, bassi consumi, ideale per la citta.', 'default-car.svg', 1),
('BMW', 'Serie 3', 2018, 22500.00, 78000, 'Diesel', 'Automatico', 'Blu', 'BMW Serie 3 Touring, pacchetto Sport, sensori di parcheggio.', 'default-car.svg', 0);
