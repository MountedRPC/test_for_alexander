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

