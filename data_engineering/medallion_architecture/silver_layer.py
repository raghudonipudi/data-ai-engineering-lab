import pandas as pd
import numpy as np
from bronze_layer import customers_transform, products_transform, orders_transform

def silver_transformations(cust_pdf, prod_pdf, orders_pdf):
    cust_pdf = cust_pdf.drop_duplicates(subset='email')
    orders_pdf = orders_pdf.drop_duplicates(subset='order_id')
    orders_cust_pdf = orders_pdf.merge(cust_pdf, on='customer_id', how='inner')
    orders_cust_prod_pdf = orders_cust_pdf.merge(prod_pdf, on = 'product_id', how='left')
    orders_cust_prod_pdf = orders_cust_prod_pdf.dropna(subset=['product_name'])
                                                    
    orders_cust_prod_pdf["year"] = orders_cust_prod_pdf["order_date"].dt.year
    orders_cust_prod_pdf["month"] = orders_cust_prod_pdf["order_date"].dt.month
    orders_cust_prod_pdf["day"] = orders_cust_prod_pdf["order_date"].dt.day
    orders_cust_prod_pdf["order_amount_computed"] = orders_cust_prod_pdf["quantity"] * orders_cust_prod_pdf["product_price"]

    orders_cust_prod_pdf = orders_cust_prod_pdf[orders_cust_prod_pdf["status"] != 'inactive']
    orders_cust_prod_pdf["order_value"] = np.where(orders_cust_prod_pdf["order_amount_computed"] > 1000, "high_value_order", "low_value_order")
    ##print(orders_cust_prod_pdf[["order_id","customer_id", "product_id","product_name","product_price","order_amount", "order_value"]])
    #print(orders_cust_pdf)
    ##print(orders_cust_prod_pdf)
    ##print(orders_pdf)
    return orders_cust_prod_pdf




