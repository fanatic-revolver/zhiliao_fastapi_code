from extend.db import Base
from sqlalchemy import Column,Integer,String,DateTime,Date,ForeignKey
import datetime
from sqlalchemy.orm import relationship


class Role(Base):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 角色名称
    name = Column(String(255), unique=True)
    # 角色描述
    desc = Column(String(255))

    # 多对多的第一种方式：使用sqlalchemy的模型关系
    # 角色和权限多对多
    # permissions = relationship("Permission",backref="role",secondary="role_permissions")
    # # 角色和用户多对多
    # users = relationship("User",backref="role",secondary="role_users")

    # 创建时间: 年月日 时分秒
    create_time = Column(DateTime, default=datetime.datetime.now())
    # 创建日期：年月日
    create_date = Column(Date, default=datetime.datetime.now())


# # 多对多的第二种方式：创建中间表模型，设置外键
# class RolePermissions(Base):
#     __tablename__ = "role_permissions"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     # 角色外键
#     role_id = Column(Integer,ForeignKey('role.id'))
#     # 权限外键
#     perm_id = Column(Integer,ForeignKey('permission.id'))
#     # 创建时间: 年月日 时分秒
#     create_time = Column(DateTime, default=datetime.datetime.now)
#     # 创建日期：年月日
#     create_date = Column(Date, default=datetime.datetime.now)
#
#
# class RoleUsers(Base):
#     __tablename__ = "role_users"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     # 角色外键
#     role_id = Column(Integer, ForeignKey('role.id'))
#     # 用户外键
#     user_id = Column(Integer, ForeignKey('user.id'))
#     # 创建时间: 年月日 时分秒
#     create_time = Column(DateTime, default=datetime.datetime.now)
#     # 创建日期：年月日
#     create_date = Column(Date, default=datetime.datetime.now)
