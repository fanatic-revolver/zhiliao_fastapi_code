#user的模型
import datetime

from extend.db import Base
from sqlalchemy import Column,Integer,String,DateTime,Date,ForeignKey
import datetime
from sqlalchemy.orm import relationship

class Department(Base):
    __tablename__="department"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name=Column(String(255))
    leader=Column(String(255))
    desc=Column(String(255))
    state = Column(Integer, default=1)
    user=relationship("User",backref="department")
    # 创建时间
    create_time = Column(DateTime, default=datetime.datetime.now())
    # 创建年月日
    create_date = Column(Date, default=datetime.datetime.now())

class User(Base):
    __tablename__="user"
    id=Column(Integer,primary_key=True,autoincrement=True)
    username=Column(String(255))
    pwd=Column(String(255))
    #todo 部门外键
    dep_id=Column(Integer,ForeignKey("department.id"))
    avatar=Column(String(255))
    addr=Column(String(255))
    #状态1表示启用，2表示弃用
    state=Column(Integer,default=1)
    last_login_date = Column(Date, default=datetime.datetime.now())
    #上次登录的IP地址
    ip=Column(String(255))
    # 创建时间
    create_time = Column(DateTime, default=datetime.datetime.now())
    # 创建年月日
    create_date = Column(Date, default=datetime.datetime.now())



