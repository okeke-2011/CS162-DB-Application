from create import *
from sqlalchemy import func
import pandas as pd
import datetime

latest_date = session.query(Sales.sale_date).order_by(Sales.sale_date.desc()).first()[0]
month, year = latest_date.month, latest_date.year

# 1. Top 5 offices with most sales in the most recent month
stmt = session.query(Offices.location,
                     func.count(Offices.office_id).label("Houses Sold"),
                     func.sum(Sales.sale_price).label("Total Sale Price")). \
    join(Houses, Offices.office_id == Houses.office_id). \
    join(Sales, Houses.house_id == Sales.house_id). \
    filter(Sales.sale_date >= datetime.date(year, month, 1)). \
    group_by(Offices.office_id).order_by(func.count(Offices.office_id).desc()).limit(5)

print(pd.read_sql(stmt.statement, session.bind))

# 2. Top 5 agents with most sales of all time
stmt = session.query(Agents.agent_id, Agents.agent_name, Agents.agent_email, Agents.agent_mobile,
                     func.count(Agents.agent_id).label("Houses Sold"),
                     func.sum(Sales.sale_price).label("Total Sale Price")). \
    join(Houses, Agents.agent_id == Houses.agent_id). \
    join(Sales, Houses.house_id == Sales.house_id). \
    group_by(Agents.agent_id).order_by(func.count(Agents.agent_id).desc()).limit(5)

print(pd.read_sql(stmt.statement, session.bind))

# 3. Commission of each agent
stmt = session.query(Agents.agent_id, Agents.agent_name,
                     func.sum(Sales.commission).label('Total Commission')). \
    join(Houses, Houses.agent_id == Agents.agent_id). \
    join(Sales, Sales.house_id == Houses.house_id). \
    group_by(Agents.agent_id).order_by(func.sum(Sales.commission).desc())

print(pd.read_sql(stmt.statement, session.bind))

# 4. Average number of days on the market
stmt = session.query(
    func.avg(
        (func.julianday(Sales.sale_date) - func.julianday(Houses.listing_date))
    ).label("Average Number of Days on Market")). \
    join(Houses, Sales.house_id == Houses.house_id). \
    filter(Sales.sale_date >= datetime.date(year, month, 1))

print(pd.read_sql(stmt.statement, session.bind))

# 5. Average selling price of a house
stmt = session.query(func.avg(Sales.sale_price).label("Average Selling Price")). \
    filter(Sales.sale_date >= datetime.date(year, month, 1))
print(pd.read_sql(stmt.statement, session.bind))
