![](images/selection.png)
![](images/login.png)
![](images/frontend.png)

```sql
ALTER TABLE game DROP PRIMARY KEY;

ALTER TABLE game DROP COLUMN id;

ALTER TABLE game ADD COLUMN id INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;
```