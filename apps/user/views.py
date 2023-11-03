from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from utils import token
from extend.get_db import get_db
from models.user.user_operation import get_user_pagination,get_user_total,active
from models.user.user_ret_model import UserRet2,UserRet

router=APIRouter(
    prefix="/user"
)

@router.get("/user_list")
def get_user_list(page_size:int,current_page:int,id:str=Depends(token.parse_token),db:Session=Depends(get_db)):
    users=get_user_pagination(db,page_size,current_page)
    total=get_user_total(db)
    content={
        "users":users,
        "pageSize":page_size,
        "pageTotal":total,
        "currentPage":current_page
    }
    return content

@router.post("/active",tags=["用户模块"])
def active_user(user:UserRet,id:str = Depends(token.parse_token),db:Session = Depends(get_db)):

    if user.state == 1:  # 正在启用
        state = 2
    if user.state == 2: # 正在停用
        state = 1

    active(db,user.id,state)

    if user.state == 1:  # 正在启用
        return {"code":200, "msg":"停用成功","state":2}
    if user.state == 2: # 正在停用
        return {"code":200, "msg":"启用成功","state":1}

