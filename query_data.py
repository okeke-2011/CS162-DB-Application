from create import session, Agents, Offices, Sellers, Buyers, Houses, Sales, AgentOffice

for table in [Agents, Offices, Sellers, Buyers, Sales, Houses, AgentOffice]:
    rows = session.query(table).all()
    print(f"\n{table.__tablename__}")
    for row in rows:
        print(row)
    print("\n")
