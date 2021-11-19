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
    lastname VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    password VARCHAR(256) NOT NULL,
    salt VARCHAR(256),

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
INSERT INTO user (name,lastname,email,password) VALUES ('Nicolas','Mahnic','nmahic@gmail.com','1234');

INSERT INTO dum (user_id,name) VALUES (1, 'Heladera');
INSERT INTO dum (user_id,name) VALUES (1, 'Lavarropas');

INSERT INTO meter (mac_address,user_id,dum_id) VALUES ('84-D8-1B-0C-5B-C1',1,1);
INSERT INTO meter (mac_address,user_id,dum_id) VALUES ('B0-B2-8F-1D-4D-02',1,2);
INSERT INTO measure (dum_id,vrms,irms,active_power,pf,thd,cos_phi) VALUES (1,1.1,1.2,1.3,0.9,0.8,0.1);