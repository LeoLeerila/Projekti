``` sql
CREATE USER 'pelaaja'@localhost IDENTIFIED BY 'pelaajansalasana';
CREATE DATABASE flight_game_projekti;
USE flight_game_projekti;
GRANT ALL PRIVILEGES ON *.* TO 'pelaaja'@localhost IDENTIFIED BY 'pelaajansalasana';
SOURCE "C:\Users\Rene School\Github\Projekti\projekti.sql";
mariadb --host="127.0.0.1" --port=3306 --user=pelaaja --password pelaajansalasana flight_game_projekti < projekti.sql
```