from sqlalchemy import Column, Integer, ForeignKey, String, MetaData, Table, DECIMAL, create_engine
from sqlalchemy.orm import registry

DB_DIALECT = "postgresql"
DB_USER = "postgres"
DB_PASSWD = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "restaurant"
# engine = create_engine("postgresql://postgres:postgres@localhost:5432/restaurant")

engine = create_engine(f"{DB_DIALECT}://{DB_USER}:{DB_PASSWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

metadata = MetaData()

menu = Table('menus', metadata,
             Column('id', Integer(), primary_key=True),
             Column('title', String(50), unique=True),
             Column('description', String(50))
             )

submenu = Table('submenus', metadata,
                Column('id', Integer(), primary_key=True),
                Column('title', String(50), unique=True),
                Column('description', String(50)),
                Column('menu_id', Integer(), ForeignKey("menus.id", onupdate="CASCADE", ondelete="CASCADE")),
                )

dish = Table('dishes', metadata,
             Column('id', Integer(), primary_key=True),
             Column('title', String(50), unique=True),
             Column('description', String(50)),
             Column('price', DECIMAL(5, 2)),
             Column('submenu_id', Integer(), ForeignKey("submenus.id", onupdate="CASCADE", ondelete="CASCADE"))
             )


class Menu(object):
    pass


mapper_registry = registry()
mapper_registry.map_imperatively(class_=Menu, local_table=menu)


class SubMenu(object):
    pass


mapper_registry = registry()
mapper_registry.map_imperatively(class_=SubMenu, local_table=submenu)


class Dish(object):
    pass


mapper_registry = registry()
mapper_registry.map_imperatively(class_=Dish, local_table=dish)

metadata.create_all(engine)

# class SubMenu(Base):
#     __tablename__ = 'submenus'
#     id = Column(Integer, primary_key=True)
#     title = Column(String(50))
#     description = Column(String(50))
#     menu_id = Column(Integer, ForeignKey("menus.id"))
#     menu = relationship("Menu", back_populates="submenus", cascade="all, delete")
#     # dishes = relationship("Dish", back_populates="submenu")

#
# class Dish(Base):
#     __tablename__ = 'dishes'
#     id = Column(Integer, primary_key=True)
#     title = Column(String(50))
#     description = Column(String(50))
#     price = Column(Float)
#     submenu_id = Column(Integer, ForeignKey("submenus.id"))
#     submenu = relationship("Submenu", back_populates="dishes", cascade="all, delete")
