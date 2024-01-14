import pandas as pd
import polars as pl
import sys
from faker import Faker
import faker_commerce
import random
from datetime import datetime
from datetime import date
import inspect
import os
from pathlib import Path
base_dir = Path(__file__).resolve().parent.parent
sys.path.append(os.path.join(base_dir, 'watson/src'))
from WatsonExplorer import Explorer


fake = Faker()
fake.add_provider(faker_commerce.Provider)
product_list = []
production_data_dict = {'Start_date' : [],
                    'Week' : [],
                    'Bweek' : [],
                    'Product_name' : [],
                    'Operation' : [],
                    'Hours' : [],}
for _ in range(15):
    product_name = fake.ecommerce_name()
    product_list.append(product_name)

operations = ['Welding', 'Milling', 'Lathe']

for operation in operations:
    for _ in range(30000): 
        start_date = fake.date_between(start_date=date(2023,12,8), end_date=date(2024,3,10))
        Week = start_date.strftime('%Y%U')
        bweek = 'Backlog' if start_date < date.today() else ''
        production_data_dict['Hours'].append(random.randint(2, 12)) 
        production_data_dict['Start_date'].append(start_date)
        production_data_dict['Week'].append(Week)
        production_data_dict['Bweek'].append(bweek)  
        production_data_dict['Operation'].append(operation)  
        production_data_dict['Product_name'].append(product_list[random.randint(0,14)])
df13 = pd.DataFrame(production_data_dict).sort_values('Start_date')

production_data_dict2 = {'Start_date' : [],
                    'Week' : [],
                    'Bweek' : [],
                    'Product_name' : [],
                    'Operation' : [],
                    'Hours' : [],}

for operation in operations:
    for _ in range(30000):  
        start_date = fake.date_between(start_date=date(2023,12,8), end_date=date(2024,3,10))
        Week = start_date.strftime('%Y%U')
        bweek = 'Backlog' if start_date < date.today() else ''
        production_data_dict2['Hours'].append(random.randint(2, 12)) 
        production_data_dict2['Start_date'].append(start_date)
        production_data_dict2['Week'].append(Week)
        production_data_dict2['Bweek'].append(bweek)  
        production_data_dict2['Operation'].append(operation)  
        production_data_dict2['Product_name'].append(product_list[random.randint(0,14)])
df14 = pl.DataFrame(production_data_dict2).sort('Start_date')

# Find all DataFrame objects
watson = Explorer()