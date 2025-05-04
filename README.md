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

```sql
ALTER TABLE game DROP PRIMARY KEY;

ALTER TABLE game DROP COLUMN id;

ALTER TABLE game ADD COLUMN id INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;
```