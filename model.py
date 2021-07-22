from sqlalchemy import create_engine, Column, Integer, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('my-sqlite.json', echo=True)
Base = declarative_base()
session_maker = sessionmaker(bind=engine)


def get_session():
    return session_maker()


class Number(Base):
    __tablename__ = 'number'

    number = Column(Integer, primary_key=True)
    chat_id = Column(Integer, primary_key=True)
    count = Column(Integer)

    def __repr__(self):
        return f'Number(number={self.number}, chat_id={self.chat_id}, count={self.count}'


class BotModelWrapper:

    @classmethod
    def insert(cls, data):
        with get_session() as session:
            number_instance = session.query(Number).filter_by(number=data.number, chat_id=data.chat_id).all()
            if number_instance:
                session.query(Number).filter_by(number=data.number, chat_id=data.chat_id). \
                    update({"count": number_instance[0].count+1}, synchronize_session="fetch")
            else:
                data.count = 0
                session.add(data)
            session.commit()

    @classmethod
    def get_popular_from(cls, chat_id):
        with get_session() as session:
            number = session.query(Number.number, func.max(Number.count)).filter_by(chat_id=chat_id).first()
        return number[0]

    @classmethod
    def empty(cls, chat_id):
        all_table = get_session().query(Number).filter_by(chat_id=chat_id).first()
        return not all_table

    @classmethod
    def get_all(cls):
        with get_session() as session:
            return session.query(Number).all()


Base.metadata.create_all(engine)


if __name__ == '__main__':
    todo = Number(number=5, chat_id=8347872345)
    BotModelWrapper.insert(todo)
    print('******')
    print(BotModelWrapper.get_popular_from(chat_id=8347872345))
