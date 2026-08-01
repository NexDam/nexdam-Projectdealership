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
    immagine VARCHAR(255) DEFAULT 'default-car.webp',
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
-- I marchi sono di fantasia: si tratta di un progetto dimostrativo, non di un
-- listino reale. Le foto in app/static/images/cars/ sono generate con AI.
INSERT INTO veicoli (marca, modello, anno, prezzo, km, carburante, cambio, colore, descrizione, immagine, disponibile) VALUES
('Nexa', 'Aria', 2021, 11900.00, 32000, 'Benzina', 'Manuale', 'Bianco', 'Citycar compatta in ottime condizioni, unico proprietario, tagliandi regolari. Ideale per chi si muove in citta e cerca bassi consumi.', 'nexa-aria.webp', 1),
('Verta', 'GT Line', 2020, 18500.00, 45000, 'Diesel', 'Manuale', 'Grigio', 'Berlina compatta full optional, gomme nuove, cerchi in lega da 18 pollici. Perfetta per uso quotidiano e viaggi lunghi.', 'verta-gt.webp', 1),
('Aureus', 'Corso SW', 2019, 24900.00, 60000, 'Diesel', 'Automatico', 'Nero', 'Station wagon executive con interni in pelle, navigatore, cruise control adattivo e ampio bagagliaio.', 'aureus-corso.webp', 1),
('Volta', 'E3', 2022, 38900.00, 15000, 'Elettrica', 'Automatico', 'Bianco', 'Berlina elettrica ad autonomia estesa, ricarica rapida, guida assistita e garanzia batteria ancora valida.', 'volta-e3.webp', 1),
('Kaido', 'Yura', 2021, 15900.00, 28000, 'Hybrid', 'Automatico', 'Rosso', 'Utilitaria ibrida dai consumi ridottissimi, cambio automatico fluido, ideale per il traffico urbano.', 'kaido-yura.webp', 1),
('Kestrel', 'Sport Wagon', 2018, 22500.00, 78000, 'Diesel', 'Automatico', 'Blu', 'Wagon sportiva con pacchetto Sport, sensori di parcheggio e assetto ribassato. Grande spazio senza rinunciare al piacere di guida.', 'kestrel-sw.webp', 0);
