CREATE TABLE Car
(
	IdC                  INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
	coordinates          VARCHAR(20) NULL,
	year                 INTEGER NULL,
	km                   INTEGER NULL,
	transmision          VARCHAR(20) NULL,
	fuel                 VARCHAR(20) NULL,
	price_per_day        DECIMAL(6,2) NULL,
	images               VARCHAR(100) NULL,
	descr                 VARCHAR(500) NULL,
	IdMan                INTEGER NULL,
	IdU                  INTEGER NULL,
	type                 VARCHAR(20) NULL,
	name                 VARCHAR(20) NULL
);


CREATE TABLE Document
(
	IdD                  INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
	issuing_date         DATE NULL,
	valid_date           DATE NULL,
	issuing_place        VARCHAR(50) NULL,
	reg_number           VARCHAR(20) NULL,
	image1               VARCHAR(50) NULL,
	image2               VARCHAR(50) NULL
);



CREATE TABLE Holding
(
	IdC                  INTEGER NOT NULL,
	IdR                  INTEGER NOT NULL,
	price                DECIMAL(6,2) NULL
);

ALTER TABLE Holding
ADD CONSTRAINT XPKHolding PRIMARY KEY (IdR);

CREATE TABLE Manufacturer
(
	IdMan                INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
	name                 VARCHAR(20) NULL
);


CREATE TABLE Model
(
	IdMan                INTEGER NOT NULL,
	name                 VARCHAR(20) NOT NULL
);

ALTER TABLE Model
ADD CONSTRAINT XPKModel PRIMARY KEY (IdMan,name);

CREATE TABLE PasswordReset
(
	IdPR                 INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
	IdU                  INTEGER NULL,
	token                VARCHAR(50) NULL
);


CREATE TABLE RatingCar
(
	IdO                  INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
	car_rating           INTEGER NULL,
	descr                 VARCHAR(500) NULL,
	djiler_rating        INTEGER NULL,
	IdR                  INTEGER NULL,
	IdC                  INTEGER NULL,
	IdD                  INTEGER NULL
);


CREATE TABLE RatingDriver
(
	IdO                  INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
	rating               INTEGER NULL,
	IdR                  INTEGER NULL,
	IdU                  INTEGER NULL,
	IdD                  INTEGER NULL,
	descr                 VARCHAR(500) NULL
);

CREATE TABLE Reservation
(
	IdR                  INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
	date_from            DATE NULL,
	date_to              DATE NULL,
	status               CHAR(1) NULL,
	IdU                  INTEGER NULL,
	IdC                  INTEGER NULL
);


CREATE TABLE User
(
	IdU                  INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
	name                 VARCHAR(20) NULL,
	email                VARCHAR(50) NOT NULL,
	password             VARCHAR(50) NULL,
	avatar               VARCHAR(50) NULL,
	email_verified       boolean NULL,
	token                VARCHAR(50) NULL,
	tel                  VARCHAR(20) NULL,
	bio                  VARCHAR(256) NULL,
	username             VARCHAR(20) NOT NULL,
	doc_verified         boolean NULL,
	IdD                  INTEGER NULL
);


ALTER TABLE Car
ADD CONSTRAINT R_4 FOREIGN KEY (IdMan, name) REFERENCES Model (IdMan, name);

ALTER TABLE Car
ADD CONSTRAINT R_17 FOREIGN KEY (IdU) REFERENCES User (IdU);

ALTER TABLE Holding
ADD CONSTRAINT R_2 FOREIGN KEY (IdC) REFERENCES Car (IdC);

ALTER TABLE Holding
ADD CONSTRAINT R_24 FOREIGN KEY (IdR) REFERENCES Reservation (IdR);

ALTER TABLE Model
ADD CONSTRAINT R_3 FOREIGN KEY (IdMan) REFERENCES Manufacturer (IdMan);

ALTER TABLE PasswordReset
ADD CONSTRAINT R_18 FOREIGN KEY (IdU) REFERENCES User (IdU);

ALTER TABLE RatingCar
ADD CONSTRAINT R_16 FOREIGN KEY (IdR) REFERENCES Reservation (IdR);

ALTER TABLE RatingCar
ADD CONSTRAINT R_21 FOREIGN KEY (IdC) REFERENCES Car (IdC);

ALTER TABLE RatingCar
ADD CONSTRAINT R_22 FOREIGN KEY (IdD) REFERENCES User (IdU);

ALTER TABLE RatingDriver
ADD CONSTRAINT R_15 FOREIGN KEY (IdR) REFERENCES Reservation (IdR);

ALTER TABLE RatingDriver
ADD CONSTRAINT R_19 FOREIGN KEY (IdU) REFERENCES User (IdU);

ALTER TABLE RatingDriver
ADD CONSTRAINT R_23 FOREIGN KEY (IdD) REFERENCES User (IdU);

ALTER TABLE Reservation
ADD CONSTRAINT R_11 FOREIGN KEY (IdU) REFERENCES User (IdU);

ALTER TABLE Reservation
ADD CONSTRAINT R_12 FOREIGN KEY (IdC) REFERENCES Car (IdC);

ALTER TABLE User
ADD CONSTRAINT R_10 FOREIGN KEY (IdD) REFERENCES Document (IdD);
