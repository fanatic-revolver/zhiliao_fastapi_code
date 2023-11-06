from fastapi import APIRouter, Depends, UploadFile,File,Form
from sqlalchemy.orm import Session
from utils import token
from extend.get_db import get_db
from models.user.user_operation import (get_user_pagination, get_user_total, active, user_update,
                                        delete_user_by_id, add_user,
                                        query_user, get_user_query_total, get_departments, get_no_departments,
                                        get_query_user_pagenation, get_query_user_total)
from models.user.user_ret_model import UserRet
from utils.get_md5_data import get_md5_pwd
from fastapi.responses import JSONResponse

router=APIRouter(
    prefix="/user"
)



@router.get("/user_list",tags=["用户模块"])
def get_user_list(page_size:int,current_page:int,id:str=Depends(token.parse_token),db:Session=Depends(get_db)):
    users=get_user_pagination(db,page_size,current_page)
    total=get_user_total(db)
    departments=get_departments(db)
    content={
        "departments":departments,
        "users":users,
        "pageSize":page_size,
        "pageTotal":total,
        "currentPage":current_page
    }
    return content

@router.post("/active",tags=["用户模块"])
def active_user(user:UserRet,user_id:str = Depends(token.parse_token),db:Session = Depends(get_db)):

    if user.state == 1:  # 正在启用
        state = 2
    if user.state == 2: # 正在停用
        state = 1

    active(db,user.id,state)

    if user.state == 1:  # 正在启用
        return {"code":200, "msg":"停用成功","state":2}
    if user.state == 2: # 正在停用
        return {"code":200, "msg":"启用成功","state":1}




    # 单文件上传
@router.post("/edit",tags=["用户模块"])
async def edit(avatar:UploadFile= File(...),username: str = Form(...),
                    id: int = Form(...),
                    pwd: str = Form(...),
                    addr: str = Form(...),
                    state: int = Form(...),
                    user_id:str = Depends(token.parse_token),
                    department_name: str = Form(...),
                    db:Session = Depends(get_db)):
    rep = await avatar.read()
    file_path="uploads/users/"+avatar.filename
    with open(file_path,"wb") as f:
        f.write(rep)
    # print(username)
    if pwd:
        md5_pwd = get_md5_pwd(pwd)
    else:
        md5_pwd = None
    user_update(db, id, username, md5_pwd, addr, state, file_path,department_name)
    return {"code":200,"msg":"更新成功","id":id}


@router.post("/delete",tags=["用户模块"])
def delete_user( user:UserRet,user_id:str = Depends(token.parse_token),db:Session = Depends(get_db)):
    id=user.id
    delete_user_by_id(db,id)
    return JSONResponse(content={"code":200,"msg":"删除成功","id":id})


@router.post("/add",tags=["用户模块"])
async def add(
        avatar:UploadFile= File(...),
        username: str = Form(...),
        pwd: str = Form(None),
        addr: str = Form(...),
        state: int = Form(...),
        department_name: str = Form(...),
        user_id:str = Depends(token.parse_token),
        db:Session = Depends(get_db)):

    if avatar:
        rep = await avatar.read()
        file_path = "uploads/users/" + avatar.filename
        with open(file_path, "wb") as f:
            f.write(rep)

    md5_pwd = get_md5_pwd(pwd)
    add_user(db,username,md5_pwd,file_path,department_name,addr,state)

    return JSONResponse(content={"code":200,"msg":"添加成功"})


@router.get("/query",tags=["用户模块"])
def query(
        q:str = "",
        name:str = "",
        page_size:int=0,
        current_page:int=0,
        user_id: str = Depends(token.parse_token),
        db: Session = Depends(get_db)):

    if q == "" or q == None or q == '':
        users = get_query_user_pagenation(db,page_size,current_page,name)
        total = get_query_user_total(db,name)

    else:
        q = q.strip()
        users = query_user(db,q,page_size,current_page,name)
        total = get_user_query_total(db,q,name)
    print(users)
    content = {
        "users":users,
        "pageSize":page_size,
        "pageTotal":total,
        "currentPage":current_page
    }
    return content

@router.get("/get_departments",tags=["用户模块"])
def get_department_data(db:Session = Depends(get_db)):
    departments=get_departments(db)
    return {"code":200,"msg":"部门查询成功","departments":departments}


# 获取除了本身所在以外的所有部门
@router.get("/get_no_departments",tags=["用户模块"])
def get_no_department_datas(id:int,user_id: str = Depends(token.parse_token),db: Session = Depends(get_db)):
    departments = get_no_departments(db,id)
    return {"code":200,"msg":"查询成功","departments":departments}


