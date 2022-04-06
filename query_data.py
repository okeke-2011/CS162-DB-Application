from create import *
from sqlalchemy import case, func, join, text
import pandas as pd
import datetime

# 1. Top 5 offices with most sales in the most recent month
latest_date = session.query(Sales.sale_date).order_by(Sales.sale_date.desc()).first()[0]
month, year = latest_date.month, latest_date.year
stmt = session.query(Offices.location,
                     func.count(Offices.office_id).label("Houses Sold"),
                     func.sum(Sales.sale_price).label("Total Sale Price")).\
    join(Houses, Offices.office_id == Houses.office_id).\
    join(Sales, Houses.house_id == Sales.house_id).\
    filter(Sales.sale_date >= datetime.date(year, month, 1)).\
    group_by(Offices.office_id).order_by(func.count(Offices.office_id).desc()).limit(5)

print(pd.read_sql(stmt.statement, session.bind))
