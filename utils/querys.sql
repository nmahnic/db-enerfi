USE Enerfi;

-----------------------------------------------REQUEST FROM ANDROID-----------------------------------------------
/*  Android send User
    {
        'name':'Eric',
        'surname':'Ortiz',
        'usernick':'eric',
        'password':'1234',
        'mail':'eric95ortiz@gmail.com'
    }
    Server return 
    {
        'ExtRef':*ExtRef*
    }
*/
INSERT INTO user (name,surname,usernick,password,mail) VALUES ('Eric','Ortiz','eric','1234','eric95ortiz@gmail.com');
*ExtRef* = SELECT user.id FROM user WHERE name='Eric' AND surname='Ortiz' AND usernick='eric' AND password='1234' AND mail='eric95ortiz@gmail.com';

/*  Android send dum and meter
    {
        'userid':ExtRef,
        'name':'Heladera',
        'mac':'84-D8-1B-0C-5B-C1'
    }
    Server return 
    {}
*/
INSERT INTO dum (user_id,name) VALUES (*ExtRef*, 'Heladera');
-- SELECT LAST_INSERT_ID();
*DumId* = SELECT dum.id FROM dum WHERE user_id=*ExtRef* AND name='Heladera';
INSERT INTO meter (mac_address,user_id,dum_id) VALUES ('84-D8-1B-0C-5B-C1',*DumId*,*ExtRef*);

-----------------------------------------------REQUEST FROM ESP32-----------------------------------------------
/*  ESP32 send MEASURE 
    {
        'mac':'84-D8-1B-0C-5B-C1',
        'vrms':1.1,
        'irms':1.2,
        'active_power':1.3,
        'pf':0.9,
        'thd':0.8,
        'cos_phi':0.1
    }
    Server return 
    {}
*/
SELECT m.dum_id FROM meter AS m WHERE m.mac_address='84-D8-1B-0C-5B-C1';
INSERT INTO measure (
        dum_id,vrms,irms,
        active_power,pf,thd,cos_phi
    ) VALUES (
        *DumId*,1.1,1.2,
        1.3,0.9,0.8,0.1
    );


-----------------------------------------------OTHER QUERYS-----------------------------------------------
SHOW TABLES;

SELECT * FROM user;
SELECT * FROM dum;
SELECT * FROM meter;
SELECT * FROM measure;

SELECT user.name, user.surname, dum.name 
    FROM dum 
    INNER JOIN user 
    ON dum.user_id=user.id;

SELECT meter.mac_address, meter.ip, dum.name 
    FROM meter 
    INNER JOIN dum 
    ON meter.dum_id=dum.id;

SELECT user.name, user.surname, meter.mac_address, meter.ip, dum.name 
    FROM meter 
    INNER JOIN dum 
    ON meter.dum_id=dum.id 
    INNER JOIN user 
    ON dum.user_id=user.id;

SELECT ms.vrms, ms.irms, ms.dum_id FROM measure AS ms;

SELECT dum.name, ms.vrms, ms.irms, ms.dum_id 
    FROM measure AS ms 
    INNER JOIN dum 
    ON ms.dum_id=dum.id;