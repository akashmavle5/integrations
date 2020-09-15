
import numpy as np
import pandas as pd
import psycopg2
from io import StringIO

host = "0.0.0.0"
port = 5555
user = "postgres"
password = "1234"
db = "db"

pg_engine = "user='{}' password='{}' host='{}' port='{}' dbname='{}'".format(user, password, host, port, db)

create_table_sql = """
CREATE TABLE IF NOT EXISTS income (
    id serial PRIMARY KEY,
    age integer,
    workclass varchar(128),
    fnlwgt integer,
    education varchar(128),
    education_num integer,
    marital_status varchar(128),
    occupation varchar(128),
    relationship varchar(128),
    race varchar(128),
    sex varchar(128),
    capital_gain integer,
    capital_loss integer,
    hours_per_week varchar(128), 
    native_country varchar(128),
    income varchar(128),
    predicted_income varchar(128)
)
"""

get_data_sql = """select * from income"""

try:
    conn = psycopg2.connect(pg_engine)
    cur = conn.cursor()
    cur.execute(create_table_sql)
    conn.commit()

    cur.execute(get_data_sql)
    df = pd.DataFrame(cur.fetchall())
    print(f"There is {df.shape[0]} records in the table.")

    if df.shape[0] == 0:
        print("Insert data into table ...")
        df = pd.read_csv("data/Adult_train.csv")
        df["predicted_income"] = None
        buffer = StringIO()
        df.to_csv(buffer, index_label='id', header=False)
        buffer.seek(0)
        cur.copy_from(buffer, "income", sep=",")
        conn.commit()
        print("Insert finished.")        

    cur.close()
except Exception as e:
    print("Problems:", str(e))