# Importation des modules utilisés
import sqlite3
import pandas as pd

# Création de la connexion
conn = sqlite3.connect("ClassicModel.sqlite")

# Récupération du contenu de Customers avec une requête SQL
pd.read_sql_query("SELECT * FROM Customers;", conn)

# 1 ; Lister les clients n’ayant jamais effecuté une commande

query = '''
    SELECT c.customerNumber, c.customerName
    FROM Customers c
    LEFT JOIN Orders o ON c.customerNumber = o.customerNumber
    WHERE o.customerNumber IS NULL;
'''

df = pd.read_sql_query(query, conn)

print(df)


# 2 Pour chaque employé, le nombre de clients, le nombre de commandes et le montant total de celles-ci ;

query = '''
    SELECT e.employeeNumber, e.firstName, e.lastName,
           COUNT(DISTINCT c.customerNumber) AS NombreClient,
           COUNT(DISTINCT o.orderNumber) AS NombreProduit,
           SUM(p.amount) AS totalOrderAmount
    FROM Employees e
    LEFT JOIN Customers c ON e.employeeNumber = c.salesRepEmployeeNumber
    LEFT JOIN Orders o ON c.customerNumber = o.customerNumber
    LEFT JOIN Payments p ON o.customerNumber = p.customerNumber
    GROUP BY e.employeeNumber, e.firstName, e.lastName;
'''

df2 = pd.read_sql_query(query, conn)

print(df2)


# 3 Idem pour chaque bureau (nombre de clients, nombre de commandes et montant total), avec en plus le nombre de clients d’un pays différent, s’il y en a ;


query = '''
    SELECT o.officeCode, o.city, o.country as Pays,
           COUNT(DISTINCT c.customerNumber) AS NombreClient,
           COUNT(DISTINCT ord.orderNumber) AS NombredeProduit,
           SUM(p.amount) AS totalOrderAmount,
           COUNT(DISTINCT CASE WHEN c.country != o.country THEN c.customerNumber END) AS numberOfForeignClients
    FROM Offices o
    LEFT JOIN Employees e ON o.officeCode = e.officeCode
    LEFT JOIN Customers c ON e.employeeNumber = c.salesRepEmployeeNumber
    LEFT JOIN Orders ord ON c.customerNumber = ord.customerNumber
    LEFT JOIN Payments p ON ord.customerNumber = p.customerNumber
    GROUP BY o.officeCode, o.city, o.country;
'''

df3 = pd.read_sql_query(query, conn)

print(df3)

# 4 Pour chaque produit, donner le nombre de commandes, la quantité totale commandée, et le nombre de clients différents ;

query = '''
    SELECT p.productCode, p.productName,
           COUNT(DISTINCT od.orderNumber) AS Nombre_Commande,
           SUM(od.quantityOrdered) AS QuantitéTotale,
           COUNT(DISTINCT o.customerNumber) AS NombredeClient
    FROM Products p
    LEFT JOIN OrderDetails od ON p.productCode = od.productCode
    LEFT JOIN Orders o ON od.orderNumber = o.orderNumber
    GROUP BY p.productCode, p.productName;
'''


df4 = pd.read_sql_query(query, conn)

# Affichage des résultats
print(df4)


# 5 Donner le nombre de commande pour chaque pays du client, ainsi que le montant total des commandes et le montant total payé : on veut conserver les clients n’ayant jamais commandé dans le résultat final ;

query = '''
    SELECT
    c.country,
    c.customerNumber,
    c.customerName,
    COUNT(DISTINCT o.orderNumber) AS numberOfOrders,
    COALESCE(SUM(od.priceEach * od.quantityOrdered), 0) AS totalOrderValue,
    COALESCE(SUM(p.amount), 0) AS totalAmountPaid
FROM
    Customers c
    LEFT JOIN Orders o ON c.customerNumber = o.customerNumber
    LEFT JOIN OrderDetails od ON o.orderNumber = od.orderNumber
    LEFT JOIN Payments p ON c.customerNumber = p.customerNumber
GROUP BY
    c.country, c.customerNumber, c.customerName
ORDER BY
    c.country, c.customerNumber;

'''

df5 = pd.read_sql_query(query, conn)


print(df5)

# 6 On veut la table de contigence du nombre de commande entre la ligne de produits et le pays du client ;

query ='''SELECT
    p.productLine,
    c.country,
    COUNT(o.orderNumber) AS numberOfOrders
FROM
    Orders o
    JOIN OrderDetails od ON o.orderNumber = od.orderNumber
    JOIN Products p ON od.productCode = p.productCode
    JOIN Customers c ON o.customerNumber = c.customerNumber
GROUP BY
    p.productLine, c.country;'''


df6 = pd.read_sql_query(query, conn)


print(df6)

# 7

query='''SELECT
    p.productCode,
    p.productName,
    AVG(od.priceEach - p.buyPrice) AS averageMargin
FROM
    OrderDetails od
    JOIN Products p ON od.productCode = p.productCode
GROUP BY
    p.productCode, p.productName
ORDER BY
    averageMargin DESC
LIMIT 10;'''

df7 = pd.read_sql_query(query, conn)


print(df7)


# 8

query='''SELECT
    p.productCode,
    p.productName,
    c.customerNumber,
    c.customerName,
    od.priceEach,
    p.buyPrice
FROM
    OrderDetails od
    JOIN Products p ON od.productCode = p.productCode
    JOIN Orders o ON od.orderNumber = o.orderNumber
    JOIN Customers c ON o.customerNumber = c.customerNumber
WHERE
    od.priceEach < p.buyPrice;'''
   
df8 = pd.read_sql_query(query, conn)
print(df8)
   
# 9


query='''SELECT
    c.customerName,
    c.customerNumber,
    p.productName,
    p.productCode,
    od.priceEach,
    p.buyPrice,
    (od.priceEach - p.buyPrice) AS lossAmount
FROM
    OrderDetails od
    INNER JOIN Orders o ON od.orderNumber = o.orderNumber
    INNER JOIN Products p ON od.productCode = p.productCode
    INNER JOIN Customers c ON o.customerNumber = c.customerNumber
WHERE
    od.priceEach < p.buyPrice
ORDER BY
    c.customerName, p.productName, od.orderLineNumber;
'''

df9 = pd.read_sql_query(query, conn)
print(df9)

# 10

query='''SELECT
    c.customerName,
    c.customerNumber,
    p.productName,
    p.productCode,
    od.priceEach,
    p.buyPrice as PrixAchat,
    (od.priceEach - p.buyPrice) AS Perte
FROM
    OrderDetails od
    INNER JOIN Orders o ON od.orderNumber = o.orderNumber
    INNER JOIN Products p ON od.productCode = p.productCode
    INNER JOIN Customers c ON o.customerNumber = c.customerNumber
WHERE
    od.priceEach < p.buyPrice
ORDER BY
    c.customerName, p.productName, od.orderLineNumber;
'''

df10 = pd.read_sql_query(query, conn)
print(df10)

# Fermeture de la connexion : IMPORTANT à faire dans un cadre professionnel
conn.close()
        
