import os
from dotenv import load_dotenv
from pathlib import Path
import mysql.connector
import pandas as pd
load_dotenv()

try:
    project_root = Path(__file__).resolve().parent.parent
    csv_path = project_root / "Data" / "industry_sales_cleaned_100k.csv"
    df = pd.read_csv(csv_path)

    connection = mysql.connector.connect(host=os.getenv("DB_HOST"),user=os.getenv("DB_USER"),password=os.getenv("DB_PASSWORD"),database=os.getenv("DB_NAME"))

    if connection.is_connected():
        print("Connected to MySQL successfully!")

    cursor=connection.cursor()

    query = """
    INSERT INTO sales (
        customer_id,
        customer_name,
        product,
        category,
        amount,
        city,
        payment_mode,
        order_status,
        order_date,
        quantity,
        customer_type,
        customer_age,
        gender,
        rating,
        sales_channel
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values_list = []

    for _,row in df.iterrows():
        values=(
            row["customer_id"],
            row["customer_name"],
            row["product"],
            row["category"],
            row["amount"],
            row["city"],
            row["payment_mode"],
            row["order_status"],
            row["order_date"],
            row["quantity"],
            row["customer_type"],
            row["customer_age"],
            row["gender"],
            row["rating"],
            row["sales_channel"]
        )

        values_list.append(values)

    if values_list:
        cursor.executemany(query,values_list)
        connection.commit()
        print(f"{len(values_list)} rows inserted successfully!")

except mysql.connector.Error as e:
    print(f"MySQL Error: {e}")

except Exception as e:
    print(f"Error: {e}")

finally:
    if 'cursor' in locals():
        cursor.close()

    if 'connection' in locals() and connection.is_connected():
        connection.close()

    print("MySQL Connection closed.")