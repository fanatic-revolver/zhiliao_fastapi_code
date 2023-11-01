from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

USERNAME="root"
PASSWORD="Mjy123456~"
HOST="localhost"
PORT="3306"
DB_NAME="zhiliao_share_system"
engine = create_engine(f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}")
SessionLocal=sessionmaker(bind=engine)
# 创建模型
Base = declarative_base()