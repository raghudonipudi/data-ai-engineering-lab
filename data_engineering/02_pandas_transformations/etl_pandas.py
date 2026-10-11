import pandas as pd
etl_file = "/Volumes/Transcend/data-ai-engineering-lab/data-samples/sales.csv"
total_sales_file = "/Volumes/Transcend/data-ai-engineering-lab/data-samples/total_sales.csv"
df = pd.read_csv(etl_file)

df = df.dropna(subset=['amount'])

df = df[df['amount'] != 0]

df['date'] = pd.to_datetime(df['date'])
#print(df.head())

df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

total_sales = df.groupby(['year','month'])['amount'].sum().reset_index()
total_sales.to_csv(total_sales_file, index=False)
#print(total_sales)

#print(df.head())
