import dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from app.models import User, Transaction, BankAccount
from app.models.base_model import Base


name2class = {
    'User': User,
    'BankAccount': BankAccount,
    'Transaction': Transaction,
}
dotenv.load_dotenv()
db_user = os.getenv('BANK_SPHERE_DBUSER')
db_name = os.getenv('BANK_SPHERE_DBNAME')
db_host = os.getenv('BANK_SPHERE_DBHOST')
db_passwd = os.getenv('BANK_SPHERE_DBPASSWD')


class DBStorage:
    __session = None
    __engine = None

    def __init__(self) -> None:
        self.__engine = create_engine(
            f'mysql+mysqldb://{db_user}:{db_passwd}@{db_host}/{db_name}',
            pool_pre_ping=False
        )

    def all(self, cls=None):
        """Returns a dictionary of all the objects present"""
        if not self.__session:
            self.reload()
        objects = {}
        if type(cls) == str:
            cls = name2class.get(cls, None)
        if cls:
            for obj in self.__session.query(cls):
                objects[obj.__class__.__name__ + '.' + obj.id] = obj
        else:
            for cls in name2class.values():
                for obj in self.__session.query(cls):
                    objects[obj.__class__.__name__ + '.' + obj.id] = obj
        return objects

    def reload(self):
        """reloads objects from the database"""
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(session_factory)

    def new(self, obj):
        """creates a new object"""
        self.__session.add(obj)

    def save(self):
        """saves the current session"""
        self.__session.commit()

    def delete(self, obj=None):
        """deletes an object"""
        if not self.__session:
            self.reload()
        if obj:
            self.__session.delete(obj)

    def close(self):
        """Dispose of current session if active"""
        self.__session.remove()

    def get(self, cls, id):
        """Retrieve an object"""
        if cls is not None and type(cls) is str and id is not None and\
           type(id) is str and cls in name2class:
            cls = name2class[cls]
            result = self.__session.query(cls).filter(cls.id == id).first()
            return result
        else:
            return None

    def get_username(self, cls, username):
        """Retrieve an object"""
        if cls is not None and type(cls) is str and username is not None and\
           type(username) is str and cls in name2class:
            cls = name2class[cls]
            result = self.__session.query(cls).filter(
                cls.username == username).first()
            return result
        else:
            return None

    def get_by_field(self, cls, field, value):
        if cls is not None and type(cls) is str and field is not None and\
           type(field) is str and cls in name2class:
            exp = f'{cls.__class__.__name__}.{field}'
            result = self.__session.query(cls).filter(exp == value).first()
            return result
        else:
            return None

    def count(self, cls=None):
        """Count number of objects in storage"""
        total = 0
        if type(cls) == str and cls in name2class:
            cls = name2class[cls]
            total = self.__session.query(cls).count()
        elif cls is None:
            for cls in name2class.values():
                total += self.__session.query(cls).count()
        return total

    def get_session(self):
        return self.__session
