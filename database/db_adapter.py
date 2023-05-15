from sqlalchemy.orm import sessionmaker


class DBAdapter:
    def __init__(self, engine):
        self.Session = sessionmaker(engine)

