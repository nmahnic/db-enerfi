/*******************************************************************************
   Enerfi Database - Version 0.1
   Script: initEnerfi.sql
   Description: Creates and populates the Enerfi database.
   DB Server: MySql
   Author: Nicolas Mahnic
   License: 
********************************************************************************/

/*******************************************************************************
   Drop database if it exists
********************************************************************************/
DROP DATABASE IF EXISTS Enerfi;


/*******************************************************************************
   Create database
********************************************************************************/
CREATE DATABASE Enerfi;

USE Enerfi;


/*******************************************************************************
   Create Tables
********************************************************************************/
CREATE TABLE user
(
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    surname VARCHAR(50) NOT NULL,
    usernick VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    mail VARCHAR(80) NOT NULL,

    CONSTRAINT PK_user PRIMARY KEY  (id)
);

CREATE TABLE meter
(
    id INT NOT NULL AUTO_INCREMENT,
    mac_address VARCHAR(50),
    user_id INT,
    dum_id INT,
    CONSTRAINT PK_meter PRIMARY KEY  (id)
);

CREATE TABLE dum
(
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT,
    name VARCHAR(50),
    CONSTRAINT PK_dum PRIMARY KEY  (id)
);

CREATE TABLE measure
(
    id INT NOT NULL AUTO_INCREMENT,
    dum_id INT,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    vrms FLOAT,
    irms FLOAT,
    active_power FLOAT,
    pf FLOAT,
    thd FLOAT,
    cos_phi FLOAT,
    CONSTRAINT PK_measureID PRIMARY KEY  (id)
);

/*******************************************************************************
   Create Foreign Keys
********************************************************************************/
ALTER TABLE meter ADD CONSTRAINT FK_meterid
    FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE meter ADD CONSTRAINT FK_meterDUMID
    FOREIGN KEY (dum_id) REFERENCES dum (id) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE dum ADD CONSTRAINT FK_dumid
    FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE measure ADD CONSTRAINT FK_measureDUMID
    FOREIGN KEY (dum_id) REFERENCES dum (id) ON DELETE NO ACTION ON UPDATE NO ACTION;    

/*******************************************************************************
   Create Primary Key Unique Indexes
********************************************************************************/
                                    /* COMING SOON */

/*******************************************************************************
   Populate Tables
********************************************************************************/
INSERT INTO user (name,surname,usernick,password,mail) VALUES ('Nicolas','Mahnic','Mash','1234','nico.mahnic@gmail.com');
INSERT INTO user (name,surname,usernick,password,mail) VALUES ('Juan Manuel','Deseta','Juanma','1234','juanmanueldeseta@gmail.com');
INSERT INTO user (name,surname,usernick,password,mail) VALUES ('Juan Ignacio','Figueiras','Juani','1234','juanifigueiras@gmail.com');
INSERT INTO user (name,surname,usernick,password,mail) VALUES ('Eric','Ortiz','eric','1234','eric95ortiz@gmail.com');
INSERT INTO user (name,surname,usernick,password,mail) VALUES ('Tiago','Monteiro','TiagoMedidas','1234','tmonteiro@frba.utn.edu.ar');
INSERT INTO dum (user_id,name) VALUES (1, 'Heladera');
INSERT INTO dum (user_id,name) VALUES (1, 'Lavarropas');
INSERT INTO dum (user_id,name) VALUES (2, 'Lavarropas');
INSERT INTO dum (user_id,name) VALUES (3, 'Lavarropas');
INSERT INTO dum (user_id,name) VALUES (4, 'Zapatilla ');
INSERT INTO dum (user_id,name) VALUES (5, 'Lavarropas');
INSERT INTO dum (user_id,name) VALUES (5, 'Computadora');
INSERT INTO meter (mac_address,user_id,dum_id) VALUES ('84-D8-1B-0C-5B-C1',1,1);
INSERT INTO meter (mac_address,user_id,dum_id) VALUES ('B0-B2-8F-1D-4D-02',1,2);
INSERT INTO measure (dum_id,vrms,irms,active_power,pf,thd,cos_phi) VALUES (1,1.1,1.2,1.3,0.9,0.8,0.1);
INSERT INTO measure (dum_id,vrms,irms,active_power,pf,thd,cos_phi) VALUES (1,1.1,1.2,1.3,0.9,0.8,0.1);
INSERT INTO measure (dum_id,vrms,irms,active_power,pf,thd,cos_phi) VALUES (2,1.1,1.2,1.3,0.9,0.8,0.1);