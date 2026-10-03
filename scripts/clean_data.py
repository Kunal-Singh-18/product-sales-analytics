import pandas as pd

df=pd.read_csv(r"C:\Users\KUNAL\Desktop\Kunal_JIIT_Work&Projects\python\Product_Sales_project\Data\industry_sales_raw_100k.csv")

# standardizing columns which have multiple names for the same data.

df["city"]=df["city"].str.strip().str.title() # fixing inconsistencies like Mumbai and mumbai being treated as two different cities.
df["payment_mode"]=df["payment_mode"].str.strip().str.title() #fixes inconsistencies like upi and UPI being treated differently.
df["order_status"] = df["order_status"].str.strip().str.title() # same as above two.

# fixing amount column , currently it has datatyype str because of some values being listed as "invalid", so change those to numeric(NaN),
# and then fitting those with median.

df["amount"]=pd.to_numeric(df["amount"],errors="coerce")
df["amount"] = df["amount"].fillna(df["amount"].median())

# reason we filled with median is that upon using describe we found out that median(45000)
# appears a lot .that means that many of the rows have a typical amount of 45000 , also mean is around 60000 which means that that there are
# large values that make the mean higher. so data is skewed , thats why we use median. removing those rows removes half the dataset

df["order_date"] = df["order_date"].str.replace("/","-",regex=False)
df["order_date"] = pd.to_datetime(df["order_date"],dayfirst=True,errors="coerce")

# we observe that some dates had / as separator and some had - ( the correct separator to convert to conventional date time format)
# so we first replace all / with - in the order date column and then do pd.to_datetime to convert to standard date time

df["customer_name"] = df["customer_name"].fillna("Unknown")
df["gender"] = df["gender"].fillna("Unknown")
df["product"]=df["product"].fillna("Unknown")
df["category"]=df["category"].fillna("Unknown")
df["payment_mode"]=df["payment_mode"].fillna("Unknown")
df["order_status"]=df["order_status"].fillna("Unknown")
df["customer_type"]=df["customer_type"].fillna("Unknown")
df["sales_channel"]=df["sales_channel"].fillna("Unknown")

#we are replacing all categorical missing values (previously NaN) with unknown , we could have done probabilistic imputation or replacing
#with mode but that would lead to bias in some cases , and since we are not making a ml model we dont need to necessary replace empty values with
#a category, so unknown remains best , truest to the data.


df.to_csv("industry_sales_cleaned_100k.csv",index=False)
print("dataset cleaned and saved into a new file successfully.")


