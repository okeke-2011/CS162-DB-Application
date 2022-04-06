from create import Agents, Offices, Sellers, Buyers, Sales, Houses, AgentOffice, sessionmaker, engine
import pandas as pd


def get_all_tables(curr_engine):
    Session = sessionmaker(bind=curr_engine)
    session = Session()

    for table in [Agents, Offices, Sellers, Buyers, Sales, Houses, AgentOffice]:
        print(f"\n{table.__tablename__}")
        print(pd.read_sql(session.query(table).statement, session.bind))
        print("\n")


if __name__ == "__main__":
    get_all_tables(engine)
