# user模块数据库操作方法
from sqlalchemy.orm import Session
from models.user.user_model import User


def get_user_by_username_and_pwd(db:Session, username:str, md5_pwd:str)->User:
    user=db.query(User.id,User.username,User.avatar,User.ip,User.last_login_date).filter(User.username==username,User.pwd==md5_pwd).first()
    return user


def get_user_by_id(db:Session,id:int)->User:
    user = db.query(User.id, User.username, User.avatar, User.ip, User.last_login_date).filter(User.id==id).first()
    print(type(user))
    print(user)
    return user






