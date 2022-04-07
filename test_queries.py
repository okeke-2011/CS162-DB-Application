from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

import unittest
import pandas as pd
import datetime

from create import Agents, Offices, Sellers, Buyers, Sales, AgentOffice, Houses
from insert_data import create_tables, insert_data
from clear_data import clear_all


class BaseTestCase(unittest.TestCase):
    test_engine = create_engine('sqlite:///test.sqlite3')
    test_engine.connect()
    Session = sessionmaker(bind=test_engine)
    test_session = Session()

    def setUp(self):
        clear_all(self.test_engine)
        create_tables(self.test_engine)
        insert_data(self.test_session)

    def tearDown(self):
        clear_all(self.test_engine)


class QueryTestCase(BaseTestCase):
    def test_add_agent(self):
        new_agent = Agents(agent_name="Sterne",
                           agent_email="phild@gmail.com",
                           agent_mobile="+1(535)735-4738")
        self.test_session.add(new_agent)
        self.test_session.commit()
        find_new_agent = self.test_session.query(Agents).filter_by(agent_name="Sterne",
                                                                   agent_email="phild@gmail.com",
                                                                   agent_mobile="+1(535)735-4738").first()
        self.assertEqual(new_agent, find_new_agent)

    def test_top_5_offices_sales(self):
        latest_date = self.test_session.query(Sales.sale_date).order_by(Sales.sale_date.desc()).first()[0]
        month, year = latest_date.month, latest_date.year

        stmt = self.test_session.query(Offices.location,
                                       func.count(Offices.office_id).label("Houses Sold"),
                                       func.sum(Sales.sale_price).label("Total Sale Price")). \
            join(Houses, Offices.office_id == Houses.office_id). \
            join(Sales, Houses.house_id == Sales.house_id). \
            filter(Sales.sale_date >= datetime.date(year, month, 1)). \
            group_by(Offices.office_id).order_by(func.count(Offices.office_id).desc()).limit(5)

        df = pd.read_sql(stmt.statement, self.test_session.bind)
        self.assertEqual(list(df["location"]), ["London", "Taipei", "San Francisco", "Seoul"])

    def test_top_5_agents_sales(self):
        stmt = self.test_session.query(Agents.agent_id, Agents.agent_name, Agents.agent_email, Agents.agent_mobile,
                                       func.count(Agents.agent_id).label("Houses Sold"),
                                       func.sum(Sales.sale_price).label("Total Sale Price")). \
            join(Houses, Agents.agent_id == Houses.agent_id). \
            join(Sales, Houses.house_id == Sales.house_id). \
            group_by(Agents.agent_id).order_by(func.count(Agents.agent_id).desc()).limit(5)

        df = pd.read_sql(stmt.statement, self.test_session.bind)
        self.assertEqual(list(df["Houses Sold"]), [3, 2, 1, 1])
        self.assertEqual(list(df["agent_name"]), ["Zoe", "Lee", "Song", "Favour"])

    def test_get_all_commission(self):
        stmt = self.test_session.query(Agents.agent_id, Agents.agent_name,
                                       func.sum(Sales.commission).label('Total Commission')). \
            join(Houses, Houses.agent_id == Agents.agent_id). \
            join(Sales, Sales.house_id == Houses.house_id). \
            group_by(Agents.agent_id).order_by(func.sum(Sales.commission).desc())

        df = pd.read_sql(stmt.statement, self.test_session.bind)
        self.assertEqual(list(df["Total Commission"]), [66000, 59400, 37500, 27000])
        self.assertEqual(list(df["agent_id"]), [5, 2, 1, 4])

    def test_avg_days_on_the_market(self):
        latest_date = self.test_session.query(Sales.sale_date).order_by(Sales.sale_date.desc()).first()[0]
        month, year = latest_date.month, latest_date.year

        stmt = self.test_session.query(
            func.avg(
                (func.julianday(Sales.sale_date) - func.julianday(Houses.listing_date))
            ).label("Average Number of Days on Market")). \
            join(Houses, Sales.house_id == Houses.house_id). \
            filter(Sales.sale_date >= datetime.date(year, month, 1))

        df = pd.read_sql(stmt.statement, self.test_session.bind)
        self.assertAlmostEqual(list(df["Average Number of Days on Market"])[0], 9.4, 1)

    def test_get_avg_sell_price(self):
        latest_date = self.test_session.query(Sales.sale_date).order_by(Sales.sale_date.desc()).first()[0]
        month, year = latest_date.month, latest_date.year

        stmt = self.test_session.query(func.avg(Sales.sale_price).label("Average Selling Price")). \
            filter(Sales.sale_date >= datetime.date(year, month, 1))

        df = pd.read_sql(stmt.statement, self.test_session.bind)
        self.assertEqual(list(df["Average Selling Price"])[0], 520000.0)


if __name__ == '__main__':
    unittest.main()