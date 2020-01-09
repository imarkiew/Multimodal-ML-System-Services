CREATE DATABASE multimodalMlSystemDatabase;
ALTER DATABASE multimodalMlSystemDatabase CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
USE multimodalMlSystemDatabase;
CREATE TABLE users (name VARCHAR(30) NOT NULL, surname VARCHAR(30) NOT NULL, specialization VARCHAR(100), email VARCHAR(50), phoneNumber VARCHAR(15), department VARCHAR(100), username VARCHAR(30) NOT NULL, passwordHash VARCHAR(60) NOT NULL, PRIMARY KEY (username));
INSERT INTO users (name, surname, specialization, email, phoneNumber, department, username, passwordHash) VALUES ('Adrian', 'Woźniak', 'dermatolog', 'AWozniak16@gmail.com', '535553652', 'Warszawa', 
'wozniak', '$2a$10$H8QI39JDnCBdWyh9PKndCOdExNrv8qz/YVhVQZsYKZ15yYoF5hyre'), ('Elżbieta', 'Kurek', 'Lekarz pierwszego kontaktu', 'EKurek015@gmail.com', '605553026', 'Poznań', 'kurek', '$2a$10$Mmgj8fB3ht5YdfVOIWzLeu7GN.FNke0lAPtITPDuqYw04ACy/BVxi');
CREATE TABLE examinations (id INT NOT NULL AUTO_INCREMENT, kind VARCHAR(30) NOT NULL, title VARCHAR(300), date CHAR(24) NOT NULL, results JSON NOT NULL, path VARCHAR(100) NOT NULL, username VARCHAR(30), PRIMARY KEY (id), FOREIGN KEY (username) REFERENCES users(username) ON UPDATE CASCADE ON DELETE CASCADE);

