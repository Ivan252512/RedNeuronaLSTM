import openpyxl
import datetime
import matplotlib.pyplot as plt

from dateutil.relativedelta import relativedelta
from calendar import monthrange

from prediccion_productos.models import RegistroVenta

books_names = ['ventas_productos_2018.xlsx', 'ventas_productos_2019.xlsx']

def get_all_sales(array_books):
    all_dates_prices = []
    all_dates = []
    all_prices = []
    all_descriptions = []
    all_firms = []
    all_rucs = []


    for i in array_books:
        new_book = openpyxl.load_workbook(i, data_only=True)
        for j in new_book.sheetnames:
            sheet = new_book[j]
            
            #Compare dates
            same_date = False
            last_date = 0
            last_price = 0
            
            for row in sheet.rows:
                print([row[i].value for i in range(len(row))])
                if isinstance(row[2].value, datetime.datetime):
                    if last_date != row[2].value:
                        new_date = row[2].value                       
                        new_price = row[10].value
                        new_description = row[5].value
                        new_firm = row[3].value
                        new_ruc = row[4].value
                        same_date = False
                    else:
                        new_date = last_date
                        new_price = last_price + row[10].value
                        new_description = last_description
                        new_firm = last_firm
                        new_ruc = last_ruc
                        same_date = True
                    
                    if not same_date:
                        all_dates_prices.append([new_date, new_price, new_description, new_firm, new_ruc])
                        last_date = new_date
                        last_price = new_price
                        last_description = new_description
                        last_firm = new_firm
                        last_ruc = new_ruc
    
    all_dates_prices.sort()
    
    for i in all_dates_prices:
        all_dates.append(i[0])
        all_prices.append(i[1])
        all_descriptions.append(i[2])
        all_firms.append(i[3])
        all_rucs.append(i[4])
    
    return [all_dates, all_prices, all_descriptions, all_firms, all_rucs, all_dates_prices]
        
        

date, price, description, firm, ruc, all_dates_prices = get_all_sales(books_names)

for i in range(len(date)):
    RegistroVenta.objects.create(fecha=date[i], precio=price[i], tipo=description[i], empresa=firm[i], ruc=ruc[i])