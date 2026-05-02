import pandas as pd

"""
customers_raw_csv = "/Volumes/Transcend/data-ai-engineering-lab/data-samples/medallion_architecture/customers_raw.csv"
products_raw_csv = "/Volumes/Transcend/data-ai-engineering-lab/data-samples/medallion_architecture/products_raw.csv"
orders_raw_csv = "/Volumes/Transcend/data-ai-engineering-lab/data-samples/medallion_architecture/orders_raw.csv"

cust_pdf = pd.read_csv(customers_raw_csv)
prod_pdf = pd.read_csv(products_raw_csv)
orders_pdf = pd.read_csv(orders_raw_csv) 
"""

def convert_snake_case(pdf):

    pdf.columns = pdf.columns.str.strip().str.lower().str.replace(' ','_').str.replace("-", "_").str.replace(r"[^a-zA-Z0-9_]", "", regex=True)
    #pdf.columns = pdf.columns.str.strip()
    return pdf

def remove_lead_trail_spaces(pdf):
    pdf = pdf.map(lambda x: x.strip() if isinstance(x, str) else x)

    return pdf

def customers_transform(pdf):
    pdf = convert_snake_case(pdf)
    pdf = remove_lead_trail_spaces(pdf)
    pdf = pdf.dropna(subset=['email'])
    pdf["created_at"] = pd.to_datetime(pdf["created_at"]).dt.tz_localize('America/New_York').dt.tz_convert('UTC')
    return pdf

def products_transform(pdf):
    pdf = convert_snake_case(pdf)
    pdf = remove_lead_trail_spaces(pdf)
    pdf["product_price"] = pdf["product_price"].fillna(pdf.groupby("category")["product_price"].transform("mean").round(2))
    return pdf

def orders_transform(pdf):
    pdf = convert_snake_case(pdf)
    pdf = remove_lead_trail_spaces(pdf)
    pdf.loc[pdf['order_amount'] < 0, 'order_amount'] = 0
    pdf["order_date"] = pd.to_datetime(pdf["order_date"]).dt.tz_localize('America/New_York').dt.tz_convert('UTC')
    return pdf
