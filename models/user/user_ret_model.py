from pydantic import BaseModel
from typing import Optional

class UserRet(BaseModel):
    id:Optional[int]=None
    # 用户名
    username:Optional[str]=None
    # 密码
    pwd :Optional[str]=None
    # todo 部门外键
    dep_id:Optional[int]=None

    # 头像
    avatar:Optional[str]=None
    # 地址
    addr:Optional[str]=None
    # 状态,1表示启用，2表示停用
    state:Optional[int]=None
    # 上次登录日期
    last_login_date:Optional[str]=None
    # 上次登录的IP地址
    ip:Optional[str]=None

    # 创建时间: 年月日 时分秒
    create_time:Optional[str]=None
    # 创建日期：年月日
    create_date:Optional[str]=None

