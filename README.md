# test_for_alexander


### Задание 1
Необходимо написать SQL запрос, который найдет и выведет всех покупателей, возраста от 18 и до 65 лет, которые купили только 2 товара и все товары одной и той же категории.
```sql
SELECT
    c.id AS ID,
    CONCAT(c.first_name, ' ', c.last_name) AS Name,
    ord.category AS Category,
    GROUP_CONCAT(ord.product SEPARATOR ', ') AS Products
FROM
    clients c
JOIN
    client_orders c_ord ON c.id = c_ord.client_id
JOIN
    orders ord ON c_ord.order_id = ord.id
WHERE
    c.age BETWEEN 18 AND 65
GROUP BY
    c.id, Name, Category
HAVING
    COUNT(DISTINCT ord.product) = 2
    AND COUNT(DISTINCT ord.category) = 1
```
### Задание 2
1. Откройте терминал или командную строку.
2. Перейдите в директорию с вашим Flask-приложением и Dockerfile.
3. Выполните следующую команду для создания Docker-образа. Замените my-flask-app на имя, которое вы хотите дать образу:
```sh
docker build -t my-flask-app .
```
#### Запуск контейнера
1. После успешной сборки Docker-образа, выполните следующую команду для запуска контейнера:

```sh
docker run -p 5000:5000 my-flask-app
```
2. Откройте веб-браузер и перейдите по адресу http://localhost:5000 (или другому порту, который вы выбрали) для доступа к вашему Flask-приложению.
