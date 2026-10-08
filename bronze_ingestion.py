import pandas as pd
import glob as glob
import os
import pandas_gbq

x=glob.glob(r'C:\Users\Tanvir\Downloads\Northwind Traders Database\*.csv')

for data in x:
    y=pd.read_csv(data)
    y.columns=y.columns.str.replace(r'[\.\s\(\)]+','_',regex=True).str.strip('_')

    file_name=os.path.basename(data).replace('.csv','')
    new_name=os.path.join(f'extracted_{file_name}')

    gbq_project_name='elite-vista-474514-t0'
    gbq_dataset_name='bronze_dataset_Northwind'
    gbq_table_name=new_name

    new_path=f'{gbq_dataset_name}.{gbq_table_name}'

    pandas_gbq.to_gbq(
        y,
        project_id=gbq_project_name,
        destination_table=new_path,
        if_exists='append'


    )


