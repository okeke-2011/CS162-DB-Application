from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Numeric, Date, Boolean, ForeignKey

engine = create_engine('sqlite:///db.sqlite3', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Offices(Base):
    __tablename__ = 'offices'

    office_id = Column(Integer, primary_key=True)
    location = Column(String)

    def __repr__(self):
        attributes = [self.office_id, self.location]
        str_attrs = [str(attr) for attr in attributes]
        return " ".join(str_attrs)


class Agents(Base):
    __tablename__ = 'agents'

    agent_id = Column(Integer, primary_key=True)
    agent_name = Column(String)
    agent_email = Column(String)
    agent_mobile = Column(String)

    def __repr__(self):
        attributes = [self.agent_id, self.agent_name, self.agent_email, self.agent_mobile]
        str_attrs = [str(attr) for attr in attributes]
        return " ".join(str_attrs)


class AgentOffice(Base):
    __tablename__ = 'agent_office'

    office_id = Column(Integer, ForeignKey("offices.office_id"), primary_key=True)
    agent_id = Column(Integer, ForeignKey("agents.agent_id"), primary_key=True)

    def __repr__(self):
        attributes = [self.office_id, self.agent_id]
        str_attrs = [str(attr) for attr in attributes]
        return " ".join(str_attrs)


class Houses(Base):
    __tablename__ = 'houses'

    house_id = Column(Integer, primary_key=True)
    office_id = Column(Integer, ForeignKey("offices.office_id"))
    agent_id = Column(Integer, ForeignKey("agents.agent_id"))
    seller_id = Column(Integer, ForeignKey("sellers.seller_id"))
    num_bedrooms = Column(Integer)
    num_bathrooms = Column(Integer)
    listing_price = Column(Integer)
    zip_code = Column(Integer)
    listing_date = Column(Date)
    sold = Column(Boolean)

    def __repr__(self):
        attributes = [self.house_id, self.office_id, self.agent_id, self.seller_id,
                      self.num_bedrooms, self.num_bathrooms, self.listing_price,
                      self.zip_code, self.listing_date, self.sold]
        str_attrs = [str(attr) for attr in attributes]
        return " ".join(str_attrs)


class Sales(Base):
    __tablename__ = 'sales'

    sale_id = Column(Integer, primary_key=True)
    house_id = Column(Integer, ForeignKey("houses.house_id"))
    sale_price = Column(Integer)
    buyer_id = Column(Integer, ForeignKey("buyers.buyer_id"))
    sale_date = Column(Date)
    commission = Column(Integer)

    def __repr__(self):
        attributes = [self.sale_id, self.house_id, self.sale_price,
                      self.buyer_id, self.sale_date, self.commission]
        str_attrs = [str(attr) for attr in attributes]
        return " ".join(str_attrs)


class Sellers(Base):
    __tablename__ = 'sellers'

    seller_id = Column(Integer, primary_key=True)
    seller_name = Column(String)
    seller_email = Column(String)
    seller_mobile = Column(String)

    def __repr__(self):
        attributes = [self.seller_id, self.seller_name, self.seller_email, self.seller_mobile]
        str_attrs = [str(attr) for attr in attributes]
        return " ".join(str_attrs)


class Buyers(Base):
    __tablename__ = 'buyers'

    buyer_id = Column(Integer, primary_key=True)
    buyer_name = Column(String)
    buyer_email = Column(String)
    buyer_mobile = Column(String)

    def __repr__(self):
        attributes = [self.buyer_id, self.buyer_name, self.buyer_email, self.buyer_mobile]
        str_attrs = [str(attr) for attr in attributes]
        return " ".join(str_attrs)