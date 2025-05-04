# Gameplay
<video controls>
  <source src="images/gameplay.mp4" type="video/mp4">
</video>

![](images/gameplay.mp4)
[Gameplay](images/gameplay.mp4)

# Images
![](images/selection.png)
![](images/login.png)
![](images/frontend.png)
![](images/gamplay.mp4)

# Käyttöohjeet
#### Luo MariaDB käyttäjä ja tietokanta
``` sql
CREATE USER 'pelaaja'@localhost IDENTIFIED BY 'pelaajansalasana';
CREATE DATABASE flight_game_projekti;
```

#### Valitse tietokanta ja anna käyttäjälle kaikki oikeudet
```sql
USE flight_game_projekti;
GRANT ALL PRIVILEGES ON flight_game_projekti.* TO 'pelaaja'@localhost IDENTIFIED BY 'pelaajansalasana';
```
#### Lataa tietokantaan pelin data
```powershell
mariadb --host="127.0.0.1" --port=3306 --user=pelaaja --password=pelaajansalasana flight_game_projekti < projekti.sql
```