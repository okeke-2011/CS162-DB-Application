from create import *


def clear_all(curr_engine):
    Base.metadata.drop_all(bind=curr_engine)


if __name__ == "__main__":
    clear_all(engine)