-- Total Revenue per Order
CREATE OR REPLACE VIEW `elite-vista-474514-t0.gold_dataset_Northwind.total_revenue_per_order` AS
SELECT
orderid,
ROUND(SUM ((unitprice * quantity)),2) as total_revenue
FROM `elite-vista-474514-t0.silver_dataset_Northwind.cleaned_order_details`
GROUP BY orderid
ORDER BY total_revenue DESC;


-- Top  5 Selling Products

CREATE OR REPLACE VIEW `elite-vista-474514-t0.gold_dataset_Northwind.top_five_selling_products` AS
SELECT
p.productname,
sum(o.quantity)as total_quantity_sold,
ROUND(SUM(o.unitprice * o.quantity),2) as total_revenu
FROM `elite-vista-474514-t0.silver_dataset_Northwind.cleaned_products` as p
JOIN `elite-vista-474514-t0.silver_dataset_Northwind.cleaned_order_details` as o
ON p.productid=o.productid
GROUP BY p.productname
ORDER BY total_revenu DESC
LIMIT 5;


-- Customer-wise Order Summary
CREATE OR REPLACE VIEW `elite-vista-474514-t0.gold_dataset_Northwind.customer_wise_order_summary` as
SELECT
c.companyname,
COUNT(DISTINCT d.orderid)as total_order,
ROUND(SUM (d.unitprice * d.quantity),2) as total_revenue

FROM `elite-vista-474514-t0.silver_dataset_Northwind.cleaned_customers` as c
JOIN `elite-vista-474514-t0.silver_dataset_Northwind.cleaned_orders` as o
ON c.customerid=o.customerid
JOIN `elite-vista-474514-t0.silver_dataset_Northwind.cleaned_order_details` as d
ON o.orderid=d.orderid
GROUP BY c.companyname
ORDER BY total_order DESC;


-- Employee Performance Analysis
CREATE OR REPLACE VIEW `elite-vista-474514-t0.gold_dataset_Northwind.employee_perfomance` as
SELECT
concat(e.firstname, ' ' ,e.lastname) as full_name,

COUNT(DISTINCT d.orderid)as total_order,
ROUND(SUM(d.unitprice * d.quantity),2)as total_revenue

FROM `elite-vista-474514-t0.silver_dataset_Northwind.cleaned_employees` as e
JOIN `elite-vista-474514-t0.silver_dataset_Northwind.cleaned_orders` as o
ON e.employeeid=o.employeeid
JOIN `elite-vista-474514-t0.silver_dataset_Northwind.cleaned_order_details`as d
ON o.orderid=d.orderid
GROUP BY full_name
ORDER BY total_revenue DESC
LIMIT 1;


-- Category-wise Revenue Contribution
CREATE OR REPLACE VIEW `elite-vista-474514-t0.gold_dataset_Northwind.category_revenue` as
SELECT
c.categoryname,
ROUND(SUM (d.unitprice * d.quantity),2)as total_revenue

FROM `elite-vista-474514-t0.silver_dataset_Northwind.cleaned_products` as p
JOIN `elite-vista-474514-t0.silver_dataset_Northwind.cleaned_categories` as c
ON p.categoryid=c.categoryid
JOIN `elite-vista-474514-t0.silver_dataset_Northwind.cleaned_order_details`as d
ON d.productid=p.productid
GROUP BY c.categoryname
ORDER BY total_revenue DESC
LIMIT 1;


-- Category-wise Top Selling Product Analysis
CREATE OR REPLACE VIEW `elite-vista-474514-t0.gold_dataset_Northwind.category_wise_top_selling` as
WITH rank_table as (SELECT
c.categoryname,
p.productname,
ROUND(SUM(d.unitprice * d.quantity),2) as total_revenue
FROM `elite-vista-474514-t0.silver_dataset_Northwind.cleaned_categories` as c
JOIN `elite-vista-474514-t0.silver_dataset_Northwind.cleaned_products` as p
ON c.categoryid=p.categoryid
JOIN `elite-vista-474514-t0.silver_dataset_Northwind.cleaned_order_details` as d
ON d.productid=p.productid
GROUP BY c.categoryname,p.productname),

new_table as (SELECT
rank_table.categoryname,
rank_table.productname,
rank_table.total_revenue,
RANK() OVER(partition by rank_table.categoryname order by rank_table.total_revenue DESC )as ranking
FROM rank_table)

SELECT
new_table.categoryname,
new_table.productname,
new_table.total_revenue
FROM new_table 
WHERE ranking=1

-- Customer Order Value Trend Analysis (LAG Function)
CREATE OR REPLACE VIEW `elite-vista-474514-t0.gold_dataset_Northwind.customer_order_value_trend` as
with table_one as (SELECT
c.companyname,
o.orderid,
o.orderdate,
ROUND (SUM (d.unitprice * d.quantity),2)as total_revenue
FROM `elite-vista-474514-t0.silver_dataset_Northwind.cleaned_customers` as c
JOIN `elite-vista-474514-t0.silver_dataset_Northwind.cleaned_orders` as o
ON c.customerid=o.customerid
JOIN `elite-vista-474514-t0.silver_dataset_Northwind.cleaned_order_details` as d
ON d.orderid=o.orderid
GROUP BY c.companyname, o.orderid,o.orderdate)

SELECT
table_one.companyname,
table_one.orderid,
table_one.orderdate,
table_one.total_revenue as current_revenue,
LAG(table_one.total_revenue) OVER(partition By table_one.companyname order By table_one.orderdate  ) as previous_revenue
FROM table_one


-- Products Above Category Average Price
CREATE OR REPLACE VIEW `elite-vista-474514-t0.gold_dataset_Northwind.products_above_category_average_price` as
with new_table as (SELECT
c.categoryname,
p.productname,
p.unitprice,
ROUND(AVG(p.unitprice) OVER(partition by c.categoryname),2) as avg_price
FROM `elite-vista-474514-t0.silver_dataset_Northwind.cleaned_products` as p
JOIN `elite-vista-474514-t0.silver_dataset_Northwind.cleaned_categories` as c
ON c.categoryid=p.categoryid)

SELECT
new_table.categoryname,
new_table.productname,
new_table.unitprice,
new_table.avg_price

FROM new_table 
WHERE new_table.unitprice>new_table.avg_price


-- Top 2 Customers per Country by Total Spend
CREATE OR REPLACE VIEW `elite-vista-474514-t0.gold_dataset_Northwind.top_two_customer_per_country` as
with new_table as (SELECT
c.country,
c.companyname,
ROUND(SUM (d.unitprice * d.quantity),2) as total_revenue
FROM `elite-vista-474514-t0.silver_dataset_Northwind.cleaned_orders` as o
JOIN `elite-vista-474514-t0.silver_dataset_Northwind.cleaned_customers` as c
ON o.customerid=c.customerid
JOIN `elite-vista-474514-t0.silver_dataset_Northwind.cleaned_order_details` as d
ON d.orderid=o.orderid
group by c.country,c.companyname),

final_table as (SELECT
new_table.country,
new_table.companyname,
new_table.total_revenue,
DENSE_RANK() OVER(partition by new_table.country ORDER BY new_table.total_revenue DESC ) as ranking
FROM new_table)

SELECT
final_table.country,
final_table.companyname,
final_table.total_revenue,
final_table.ranking
FROM final_table
WHERE final_table.ranking<=2

