'''
@IDE ：PyCharm
@Author ：知了-海龙
@Date ：2021/8/18 11:44
@Email：hallen200806@163.com
@Desc ：
'''

from pydantic import BaseModel
from typing import Optional

class DepartmentRet(BaseModel):
    id : Optional[int]=None
    # 部门名称
    name : Optional[str]=None
    # 部门主管
    leader : Optional[str]=None
    # 部门职责
    desc : Optional[str]=None
    create_time : Optional[str]=None