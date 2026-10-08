import pandas as pd
import pandas_gbq

project_name='elite-vista-474514-t0'
bronze_layer='bronze_dataset_Northwind'


query_categories=f'select * FROM `{project_name}.{bronze_layer}.extracted_categories`'
query_customers=f'select * FROM `elite-vista-474514-t0.bronze_dataset_Northwind.extracted_customers`'
query_employee_territory=f'select * FROM `elite-vista-474514-t0.bronze_dataset_Northwind.extracted_employee_territory`'
query_employees=f'select * FROM `elite-vista-474514-t0.bronze_dataset_Northwind.extracted_employees`'
query_order_details=f'select * FROM `elite-vista-474514-t0.bronze_dataset_Northwind.extracted_order_details`'
query_orders= f'select * FROM `elite-vista-474514-t0.bronze_dataset_Northwind.extracted_orders`'
query_products=f' select * FROM `elite-vista-474514-t0.bronze_dataset_Northwind.extracted_products`'
query_region=f' select * FROM `elite-vista-474514-t0.bronze_dataset_Northwind.extracted_region`'
query_shippers=f'select * FROM `elite-vista-474514-t0.bronze_dataset_Northwind.extracted_shippers`'
query_suppliers=f'select * FROM `elite-vista-474514-t0.bronze_dataset_Northwind.extracted_suppliers`'
query_territories=f'select * FROM `elite-vista-474514-t0.bronze_dataset_Northwind.extracted_territories`'

categories_data=pandas_gbq.read_gbq(query_categories, project_id=project_name)
customers_data=pandas_gbq.read_gbq(query_customers,project_id=project_name)
employee_territory_data=pandas_gbq.read_gbq(query_employee_territory,project_id=project_name)
employees_data=pandas_gbq.read_gbq(query_employees,project_id=project_name)
order_details_data=pandas_gbq.read_gbq(query_order_details,project_id=project_name)
orders_data=pandas_gbq.read_gbq(query_orders,project_id=project_name)
products_data=pandas_gbq.read_gbq(query_products,project_id=project_name)
region_data=pandas_gbq.read_gbq(query_region,project_id=project_name)
shippers_data=pandas_gbq.read_gbq(query_shippers,project_id=project_name)
suppliers_data=pandas_gbq.read_gbq(query_suppliers,project_id=project_name)
territories_data=pandas_gbq.read_gbq(query_territories,project_id=project_name)

# for categories:

categories_data.columns=categories_data.columns.str.strip().str.lower()

for col in categories_data.select_dtypes(include=['object','str']):
    categories_data[col]=categories_data[col].str.strip()

categories_data['categoryid']=categories_data['categoryid'].astype('Int64')

categories_data.dropna(subset=['categoryid'],inplace=True)
categories_data.drop_duplicates(inplace=True,keep='first')

# for customers:

customers_data.columns=customers_data.columns.str.strip().str.lower()

for col in customers_data.select_dtypes(include=['object','str']):
    customers_data[col]=customers_data[col].str.strip()


customers_data.dropna(subset=['customerid'],inplace=True)
customers_data.drop_duplicates(inplace=True,keep='first')
customers_data['country']=customers_data['country'].fillna('Unknown')

# for employee territory

employee_territory_data.columns=employee_territory_data.columns.str.strip().str.lower()

employee_territory_data.dropna(subset=['employeeid','territoryid'],inplace=True)

employee_territory_data['employeeid'] = employee_territory_data['employeeid'].astype('Int64')
employee_territory_data['territoryid'] = employee_territory_data['territoryid'].astype('Int64')

# for employees

employees_data.columns=employees_data.columns.str.strip().str.lower()

employees_data.dropna(subset=['employeeid'], inplace=True)
employees_data.drop_duplicates(inplace=True, keep='first')

for col in employees_data.select_dtypes(include=['object', 'str']):
    employees_data[col]=employees_data[col].str.strip()

employees_data['employeeid']=employees_data['employeeid'].astype('Int64')
employees_data['salary']=employees_data['salary'].astype(float)

employees_data['birthdate']=pd.to_datetime(employees_data['birthdate'], errors='coerce')
employees_data['hiredate']=pd.to_datetime(employees_data['hiredate'], errors='coerce')



# for order details

order_details_data.columns=order_details_data.columns.str.strip().str.lower()
order_details_data.dropna(subset=['orderid','productid'],inplace=True)
order_details_data.drop_duplicates(inplace=True, keep='first')

order_details_data['orderid']=order_details_data['orderid'].astype('Int64')
order_details_data['productid']=order_details_data['productid'].astype('Int64')
order_details_data['unitprice']=order_details_data['unitprice'].astype(float)
order_details_data['quantity']=order_details_data['quantity'].astype('Int64')
order_details_data['discount']=order_details_data['discount'].astype(float)

order_details_data.loc[order_details_data['unitprice']<0, 'unitprice']=0


# for order

orders_data.columns=orders_data.columns.str.strip().str.lower()

orders_data.dropna(subset=['orderid', 'customerid'], inplace=True)
orders_data.drop_duplicates(inplace=True,keep='first')


orders_data['orderid']=orders_data['orderid'].astype('Int64')
orders_data['employeeid']=orders_data['employeeid'].astype('Int64')
orders_data['shipvia']=orders_data['shipvia'].astype('Int64')
orders_data['freight']=orders_data['freight'].astype(float)


for data in orders_data.select_dtypes(include=['object','str']):
    orders_data[data]=orders_data[data].str.strip()

orders_data['orderdate']=pd.to_datetime(orders_data['orderdate'],errors='coerce')
orders_data['requireddate']=pd.to_datetime(orders_data['requireddate'],errors='coerce')
orders_data['shippeddate']=pd.to_datetime(orders_data['shippeddate'],errors='coerce')


# for products


products_data.columns=products_data.columns.str.strip().str.lower()

products_data.dropna(subset=['productid'],inplace=True)
products_data.drop_duplicates(inplace=True,keep='first')

products_data['productname']=products_data['productname'].str.strip()
products_data['quantityperunit']=products_data['quantityperunit'].str.strip()

products_data['productid']=products_data['productid'].astype('Int64')
products_data['supplierid']=products_data['supplierid'].astype('Int64')
products_data['categoryid']=products_data['categoryid'].astype('Int64')
products_data['unitprice']=products_data['unitprice'].astype(float)
products_data['unitsinstock']=products_data['unitsinstock'].astype('Int64')
products_data['unitsonorder']=products_data['unitsonorder'].astype('Int64')
products_data['reorderlevel']=products_data['reorderlevel'].astype('Int64')
products_data['discontinued']=products_data['discontinued'].astype('Int64')

products_data.loc[products_data['unitprice']<0, 'unitprice']=0


# for region

region_data.columns=region_data.columns.str.strip().str.lower()

region_data.dropna(subset=['regionid'],inplace=True)
region_data.drop_duplicates(inplace=True,keep='first')

region_data['regiondescription']=region_data['regiondescription'].str.strip()
region_data['regionid']=region_data['regionid'].astype('Int64')



#  for shippers

shippers_data.columns=shippers_data.columns.str.strip().str.lower()

shippers_data.dropna(subset=['shipperid'],inplace=True)
shippers_data.drop_duplicates(inplace=True,keep='first')

shippers_data['shipperid']=shippers_data['shipperid'].astype('Int64')
shippers_data['companyname']=shippers_data['companyname'].str.strip()
shippers_data['phone']=shippers_data['phone'].str.strip()


# for suppliers

suppliers_data.columns=suppliers_data.columns.str.strip().str.lower()

suppliers_data.dropna(subset=['supplierid'],inplace=True)
suppliers_data.drop_duplicates(inplace=True,keep='first')

for col in suppliers_data.select_dtypes(include=['object','str']):
    suppliers_data[col]=suppliers_data[col].str.strip()


suppliers_data['supplierid']=suppliers_data['supplierid'].astype('Int64')





# for territories

territories_data.columns=territories_data.columns.str.strip().str.lower()
territories_data.dropna(subset=['territoryid'],inplace=True)
territories_data.drop_duplicates(inplace=True,keep='first')

territories_data['territoryid']=territories_data['territoryid'].astype('Int64')

territories_data['regionid']=territories_data['regionid'].astype('Int64')

for col in territories_data.select_dtypes(include=['object','str']):
    territories_data[col]=territories_data[col].str.strip()




silver_tables = {
    'cleaned_categories': categories_data,
    'cleaned_customers': customers_data,
    'cleaned_employee_territory': employee_territory_data,
    'cleaned_employees': employees_data,
    'cleaned_order_details': order_details_data,
    'cleaned_orders': orders_data,
    'cleaned_products': products_data,
    'cleaned_region': region_data,
    'cleaned_shippers': shippers_data,
    'cleaned_suppliers': suppliers_data,
    'cleaned_territories': territories_data,
}



gbq_project_id='elite-vista-474514-t0'
gbq_dataset_name='silver_dataset_Northwind'

for table_name, df in silver_tables.items():
    new_path=f'{gbq_dataset_name}.{table_name}'

    pandas_gbq.to_gbq(
    df,
    destination_table=new_path,
    project_id=gbq_project_id,
    if_exists='append'

)




