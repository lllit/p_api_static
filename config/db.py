from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

try:
    engine = create_engine("mysql+pymysql://root:Homero123@127.0.0.1:3306/lllit_data", echo=True)
    
    session= sessionmaker(bind=engine)
    
    base = declarative_base()
    
    meta_data = MetaData() 
    
    print('Conexion Exitosa') 
except:
    print('No se conecto') 

