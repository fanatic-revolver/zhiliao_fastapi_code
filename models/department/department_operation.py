'''
@IDE ：PyCharm
@Author ：知了-海龙
@Date ：2021/8/13 15:17
@Email：hallen200806@163.com
@Desc ：user模块数据库操作方法
'''

from sqlalchemy.orm import Session
from models.user.user_model import Department
import datetime



def get_department_by_id(db:Session,id:int) -> Department:
    department = db.query(Department).filter(Department.id == id).first()

    return department

# 分页
# SELECT * from `user` LIMIT (page-1)*pagesize,5
def get_department_pagenation(db:Session,page_size:int,current_page:int) -> [Department]:
    departments = db.query(
        Department
    ).limit(page_size).offset((current_page-1)*page_size).all()
    return departments

# 获取总数量
def get_department_total(db:Session) -> int:
    total = db.query(Department).count()
    return total


# 部门编辑
def department_update(db:Session,id:int,name:str,leader:str,desc:str):
    department = db.query(Department).filter(Department.id == id).first()
    department.name = name
    department.leader = leader
    department.desc = desc

    db.commit()
    db.flush()

# 根据部门id删除部门
def delete_department_by_id(db:Session,id:int):
    department = db.query(Department).filter(Department.id == id).first()

    db.delete(department)
    db.commit()
    db.flush()


# 添加
def add_department(db:Session,name:str,leader:str,desc:str):
    department = Department(
        name = name,
        leader = leader,
        desc = desc,

    )

    db.add(department)
    db.commit()
    db.flush()

def query_department(db:Session,q:str,page_size:int,current_page:int) -> [Department]:

    departments = db.query(
       Department
    ).filter(Department.name.like('%'+q+'%')).limit(page_size).offset((current_page-1)*page_size).all()
    return departments

def get_department_query_total(db:Session,q:str) -> int:
    total = db.query(Department).filter(Department.name.like('%'+q+'%')).count()
    return total