# user模块数据库操作方法
from sqlalchemy.orm import Session
from models.user.user_model import User


def get_user_by_username_and_pwd(db:Session, username:str, md5_pwd:str)->User:
    user=db.query(User.id,User.username,User.avatar,User.ip,User.last_login_date).filter(User.username==username,User.pwd==md5_pwd).first()
    return user


def get_user_by_id(db:Session,id:int)->User:
    user = db.query(User.id, User.username, User.avatar,
                    User.ip, User.last_login_date).filter(User.id==id).first()
    return user

def get_user_pagination(db:Session,page_size:int,current_page:int):
    users=db.query(User).limit(page_size).offset((current_page-1)*page_size).all()
    return users

def get_user_total(db:Session):
    total=db.query(User).count()
    return total

#启用停用
def active(db:Session,id:int,state:int):
    user=db.query(User).filter(User.id==id).first()
    user.state=state
    db.commit()
    db.flush()








