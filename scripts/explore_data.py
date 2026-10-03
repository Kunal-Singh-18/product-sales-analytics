import pandas as pd

df=pd.read_csv(r"C:\Users\KUNAL\Desktop\Kunal_JIIT_Work&Projects\python\Product_Sales_project\Data\industry_sales_raw_100k.csv")

#Basic information about the dataset.
print(f"shape: {df.shape}\n")
print(f"columns : {df.columns}\n")
print(f"info :")
df.info()
print()
print(f"Missing values:\n{df.isnull().sum()}\n")
print(f"Duplicate values : {df.duplicated().sum()}\n")

# categorical exploration.
print(f"Product Distribution:\n{df['product'].value_counts(dropna=False)}\n")
print(f"City Distribution:\n{df['city'].value_counts(dropna=False)}\n")
print(f"Customer Type Distribution:\n{df['customer_type'].value_counts(dropna=False)}\n")
print(f"Gender Distribution:\n{df['gender'].value_counts(dropna=False)}\n")
print(f"Category Distribution:\n{df['category'].value_counts(dropna=False)}\n")
print(f"Payment Mode Distribution:\n{df['payment_mode'].value_counts(dropna=False)}\n")
print(f"Order Status Distribution:\n{df['order_status'].value_counts(dropna=False)}\n")
print(f"Sales Channel Distribution:\n{df['sales_channel'].value_counts(dropna=False)}\n")

#exploring numerical columns.
print(f"Customer Age Statistics:\n{df['customer_age'].describe()}\n")
print(f"Quantity Statistics:\n{df['quantity'].describe()}\n")
print(f"Rating Statistics:\n{df['rating'].describe()}\n")

#looking at amount column- its an anomaly

print(f"Amount (First 20 Rows):\n{df['amount'].head(20)}\n")
print(f"Amount (Random Sample):\n{df['amount'].sample(20)}\n")
print(f"Most Common Amount Values:\n{df['amount'].value_counts().head(20)}\n")

# amount is stored as string even though it should be numeric.
# We need to investigate why before converting it.

# order_date is also stored as string.
# Future analytics such as monthly sales, yearly sales,
# and trend analysis will require datetime conversion.

print(f"Order Date (First 5 Rows):\n{df['order_date'].head()}\n")
print(f"Order Date (Random Sample):\n{df['order_date'].sample(20)}\n")

# we dont need to analyse customer_id , its a unique identifier

print(f"Customer Name Sample:\n{df['customer_name'].sample(10)}\n")

#just to see what it looks like. customer name is important for the purpose of cleaning but not for analysis( not high priority)

#all columns are covered.

