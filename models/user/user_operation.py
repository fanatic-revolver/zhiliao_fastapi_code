# user模块数据库操作方法
from typing import List

from sqlalchemy.orm import Session
from models.user.user_model import User, Department
import datetime

def get_user_by_username_and_pwd(db:Session, username:str, md5_pwd:str)->User:
    user=db.query(User.id,User.username,User.avatar,User.ip,User.last_login_date,User.state).filter(User.username==username,User.pwd==md5_pwd).first()
    return user

def update_time_and_ip(db:Session,user_id:int,login_date:datetime.datetime,ip:str):
    user=db.query(User).filter(User.id==user_id).first()
    user.last_login_date=login_date
    user.ip=ip
    db.commit()
    db.flush()



def get_user_by_id(db:Session,id:int)->User:
    user = db.query(User.id, User.username, User.avatar, User.ip, User.last_login_date).filter(User.id==id).first()
    return user

def get_user_pagination(db:Session,page_size:int,current_page:int):
    users=db.query(User.id,User.dep_id,User.username,User.avatar,User.addr,User.state,User.last_login_date,User.ip,User.create_time,Department.name).join(Department).limit(page_size).offset((current_page-1)*page_size).all()
    users_dict_list = []
    for user in users:
        this_user={"id":user.id,"dep_id":user.dep_id,"username":user.username,"avatar":user.avatar,"addr":user.addr,"state":user.state,"last_login_date":user.last_login_date,"ip":user.ip,"create_time":user.create_time,"name":user[-1]}
        users_dict_list.append(this_user)
    return users_dict_list

def get_user_total(db:Session):
    total=db.query(User).count()
    return total

#启用停用
def active(db:Session,id:int,state:int):
    user=db.query(User).filter(User.id==id).first()
    user.state=state
    db.commit()
    db.flush()



def user_update(db:Session, id:int, username:str, pwd:str, addr:str, state:int, avatar:str,department_name:str):
    department = db.query(Department).filter(Department.name == department_name).first()
    user = db.query(User).filter(User.id == id).first()
    user.username = username
    user.state = state
    user.addr = addr
    user.dep_id = department.id

    user.avatar = "/" + avatar
    if pwd:
        user.pwd = pwd
    db.commit()
    db.flush()

#根据用户id删除用户
def delete_user_by_id(db:Session,id:int):
    user=db.query(User).filter(User.id==id).first()
    db.delete(user)
    db.commit()
    db.flush()


#添加用户
def add_user(db:Session,username:str,pwd:str,avatar:str,department_name:str,addr:str,state:int):

    department = db.query(Department).filter(Department.name == department_name).first()
    user = User(
        username = username,
        pwd = pwd,
        avatar = "/" + avatar,
        addr = addr,
        state = state,
        dep_id= department.id
    )

    db.add(user)
    db.commit()
    db.flush()

def get_query_user_pagenation(db:Session,page_size:int,current_page:int,name:str) -> [User]:
    department = db.query(Department).filter(Department.name == name).first()

    if department:
        users = db.query(
            User.id,
            User.username,
            User.avatar,
            User.addr,
            User.state,
            User.ip,
            User.last_login_date,
            User.create_time,
            User.dep_id,
            Department.name
        ).filter(User.dep_id == department.id).join(Department).limit(page_size).offset((current_page - 1) * page_size).all()
    else:
        users = db.query(
            User.id,
            User.username,
            User.avatar,
            User.addr,
            User.state,
            User.ip,
            User.last_login_date,
            User.create_time,
            User.dep_id,
            Department.name
        ).join(Department).limit(page_size).offset((current_page-1)*page_size).all()
    users_dict_list = []
    for user in users:
        this_user = {"id": user.id, "dep_id": user.dep_id, "username": user.username, "avatar": user.avatar,
                     "addr": user.addr, "state": user.state, "last_login_date": user.last_login_date, "ip": user.ip,
                     "create_time": user.create_time, "name": user[-1]}
        users_dict_list.append(this_user)
    return users_dict_list

# 获取总数量
def get_query_user_total(db:Session,name:str) -> int:
    department = db.query(Department).filter(Department.name == name).first()

    if department:

        total = db.query(User).filter(User.dep_id == department.id).count()
    else:
        total = db.query(User).count()
    return total

def query_user(db:Session,q:str,page_size:int,current_page:int,name:str):
    department = db.query(Department).filter(Department.name == name).first()

    if department:

        users = db.query(
            User.id,
            User.username,
            User.avatar,
            User.addr,
            User.state,
            User.ip,
            User.last_login_date,
            User.create_time,
            User.dep_id,
            Department.name
        ).filter(User.dep_id == department.id).join(Department).filter(User.username.like('%' + q + '%')).limit(
            page_size).offset((current_page - 1) * page_size).all()
    else:
        users = db.query(
            User.id,
            User.username,
            User.avatar,
            User.addr,
            User.state,
            User.ip,
            User.last_login_date,
            User.create_time,
            User.dep_id,
            Department.name
        ).join(Department).filter(User.username.like('%' + q + '%')).limit(page_size).offset(
            (current_page - 1) * page_size).all()
    users_dict_list = []
    for user in users:
        this_user = {"id": user.id, "dep_id": user.dep_id, "username": user.username, "avatar": user.avatar,
                     "addr": user.addr, "state": user.state, "last_login_date": user.last_login_date, "ip": user.ip,
                     "create_time": user.create_time, "name": user[-1]}
        users_dict_list.append(this_user)
    return users_dict_list
    return users


def get_user_query_total(db:Session,q:str,name:str)->int:
    department = db.query(Department).filter(Department.name == name).first()

    if department:
        total = db.query(User).filter(User.username.like('%' + q + '%'), User.dep_id == department.id).count()
    else:
        total = db.query(User).filter(User.username.like('%' + q + '%')).count()
    return total


def get_departments(db:Session) -> [Department]:
    departments = db.query(Department).all()
    dd=[]
    for d in departments:
        dd.append(d.to_dict())
    # print(dd)
    return dd

def get_no_departments(db:Session,id:int) -> [Department]:
    user = db.query(User).filter(User.id == id).first()
    departments = db.query(Department).filter(Department.id != user.dep_id).all()
    return departments





