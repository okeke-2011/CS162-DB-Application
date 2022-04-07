from create import *
import datetime


def create_tables(curr_engine):
    Base.metadata.create_all(curr_engine)


def insert_data(curr_session):
    curr_session.add_all([Offices(location="San Francisco"), Offices(location="Berlin"),
                          Offices(location="Taipei"), Offices(location="London"),
                          Offices(location="Seoul")])
    curr_session.add_all([Agents(agent_name="Favour", agent_email="okeke@gmail.com", agent_mobile="+1(512)351-0799"),
                          Agents(agent_name="Zoe", agent_email="zoe@gmail.com", agent_mobile="+1(351)093-7269"),
                          Agents(agent_name="Karl", agent_email="karl@gmail.com", agent_mobile="+1(747)628-9269"),
                          Agents(agent_name="Song", agent_email="dc@gmail.com", agent_mobile="+44(942)820-8462"),
                          Agents(agent_name="Lee", agent_email="ling@gmail.com", agent_mobile="+49(273)756-7630")])

    curr_session.add_all([AgentOffice(office_id=1, agent_id=1), AgentOffice(office_id=1, agent_id=2),
                          AgentOffice(office_id=2, agent_id=1), AgentOffice(office_id=1, agent_id=3),
                          AgentOffice(office_id=5, agent_id=4), AgentOffice(office_id=3, agent_id=5),
                          AgentOffice(office_id=4, agent_id=2)])

    curr_session.add_all([Buyers(buyer_name="John", buyer_email="john@gmail.com", buyer_mobile="+1(512)345-0799"),
                          Buyers(buyer_name="Kim", buyer_email="kim@gmail.com", buyer_mobile="+1(513)311-0799"),
                          Buyers(buyer_name="Kareem", buyer_email="kar@gmail.com", buyer_mobile="+1(592)351-0999"),
                          Buyers(buyer_name="Simdi", buyer_email="di123@gmail.com", buyer_mobile="+1(232)651-0729"),
                          Buyers(buyer_name="Ludan", buyer_email="lu@gmail.com", buyer_mobile="+1(592)851-0799"),
                          Buyers(buyer_name="Okele", buyer_email="oke@gmail.com", buyer_mobile="+1(587)351-0799")])

    curr_session.add_all([Sellers(seller_name="John", seller_email="john@gmail.com", seller_mobile="+1(512)345-0799"),
                          Sellers(seller_name="Kim", seller_email="kim@gmail.com", seller_mobile="+1(513)311-0799"),
                          Sellers(seller_name="Kareem", seller_email="kar@gmail.com", seller_mobile="+1(592)351-0999"),
                          Sellers(seller_name="Simdi", seller_email="di123@gmail.com", seller_mobile="+1(232)651-0729"),
                          Sellers(seller_name="Ludan", seller_email="lu@gmail.com", seller_mobile="+1(592)851-0799"),
                          Sellers(seller_name="Okele", seller_email="oke@gmail.com", seller_mobile="+1(587)351-0799")])

    curr_session.add_all([Houses(office_id=1, agent_id=1, seller_id=2, num_bedrooms=2, num_bathrooms=3,
                                 listing_price=750000.00, zip_code=94102, listing_date=datetime.date(2022, 3, 25),
                                 sold=False),
                          Houses(office_id=4, agent_id=2, seller_id=5, num_bedrooms=1, num_bathrooms=3,
                                 listing_price=500000.00, zip_code=53721, listing_date=datetime.date(2022, 3, 28),
                                 sold=False),
                          Houses(office_id=3, agent_id=5, seller_id=6, num_bedrooms=3, num_bathrooms=5,
                                 listing_price=1200000.00, zip_code=81009, listing_date=datetime.date(2022, 3, 30),
                                 sold=False),
                          Houses(office_id=1, agent_id=2, seller_id=1, num_bedrooms=1, num_bathrooms=1,
                                 listing_price=250000.00, zip_code=93102, listing_date=datetime.date(2022, 4, 2),
                                 sold=False),
                          Houses(office_id=3, agent_id=5, seller_id=3, num_bedrooms=2, num_bathrooms=2,
                                 listing_price=300000.00, zip_code=82010, listing_date=datetime.date(2022, 4, 3),
                                 sold=False),
                          Houses(office_id=4, agent_id=2, seller_id=1, num_bedrooms=2, num_bathrooms=1,
                                 listing_price=190000.00, zip_code=73682, listing_date=datetime.date(2022, 4, 7),
                                 sold=False),
                          Houses(office_id=5, agent_id=4, seller_id=2, num_bedrooms=3, num_bathrooms=2,
                                 listing_price=450000.00, zip_code=48121, listing_date=datetime.date(2022, 4, 15),
                                 sold=False),
                          Houses(office_id=2, agent_id=1, seller_id=2, num_bedrooms=1, num_bathrooms=1,
                                 listing_price=120000.00, zip_code=90017, listing_date=datetime.date(2022, 4, 16),
                                 sold=False)])
    curr_session.commit()

    def make_sale(house_id, buyer_id, sale_price, sale_date):
        if sale_price > 1000000:
            commission = sale_price * 0.04
        elif sale_price > 500000:
            commission = sale_price * 0.05
        elif sale_price > 200000:
            commission = sale_price * 0.06
        elif sale_price > 100000:
            commission = sale_price * 0.075
        elif sale_price <= 100000:
            commission = sale_price * 0.1

        new_sale = Sales(house_id=house_id, buyer_id=buyer_id, sale_price=sale_price,
                         sale_date=sale_date, commission=commission)
        curr_session.add(new_sale)
        curr_session.query(Houses).filter_by(house_id=house_id).update({"sold": True})
        curr_session.commit()

    make_sale(1, 1, 750000.00, datetime.date(2022, 4, 6))
    make_sale(2, 3, 490000.00, datetime.date(2022, 4, 7))
    make_sale(3, 4, 1200000.00, datetime.date(2022, 4, 8))
    make_sale(4, 2, 250000.00, datetime.date(2022, 4, 10))
    make_sale(5, 6, 300000.00, datetime.date(2022, 4, 16))
    make_sale(6, 5, 200000.00, datetime.date(2022, 4, 17))
    make_sale(7, 1, 450000.00, datetime.date(2022, 4, 19))



if __name__ == "__main__":
    create_tables(engine)
    insert_data(session)
