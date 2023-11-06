'''
@IDE ：PyCharm
@Author ：知了-海龙
@Date ：2021/8/18 11:21
@Email：hallen200806@163.com
@Desc ：
'''

from fastapi import APIRouter,Depends,Form
from sqlalchemy.orm import Session
from utils import token
from extend.get_db import get_db
from models.department.department_operation import \
    get_department_pagenation,\
    get_department_total,\
    department_update,\
    delete_department_by_id,\
    add_department,\
    query_department,\
    get_department_query_total

from fastapi.responses import JSONResponse

from models.department.department_ret import DepartmentRet

router = APIRouter(
    prefix="/department"
)

@router.get("/department_list",tags=["部门模块"])
def get_department_list(page_size:int,current_page:int,id:str = Depends(token.parse_token),db:Session = Depends(get_db)):

    departments = get_department_pagenation(db,page_size,current_page)
    total = get_department_total(db)
    content = {
        "departments":departments,
        "pageSize":page_size,
        "pageTotal":total,
        "currentPage":current_page
    }
    return content


#用户修改，涉及到图片上次，所有得用FormData这种方式提交
@router.post("/edit",tags=["部门模块"])
def edit(
        id: int = Form(...),
        name: str = Form(...),
        leader: str = Form(None),
        desc: str = Form(...),
        user_id:str = Depends(token.parse_token),
        db:Session = Depends(get_db)):

    department_update(db,id,name,leader,desc)
    return {"code":200,"msg":"更新成功","id":id}


@router.post("/delete",tags=["部门模块"])
def delete_department(department:DepartmentRet,user_id:str = Depends(token.parse_token),
        db:Session = Depends(get_db)):
    id = department.id
    delete_department_by_id(db,id)
    return JSONResponse(content={"code":200,"msg":"删除成功","id":id})


@router.post("/add",tags=["部门模块"])
async def add(
        name: str = Form(...),
        leader: str = Form(None),
        desc: str = Form(...),

        user_id:str = Depends(token.parse_token),
        db:Session = Depends(get_db)):
    add_department(db,name,leader,desc)

    return JSONResponse(content={"code":200,"msg":"添加成功"})


# 查询
@router.get("/query",tags=["部门模块"])
def query(
        q:str,
        page_size:int,
        current_page:int,
        user_id: str = Depends(token.parse_token),
        db: Session = Depends(get_db)):
    if q == "" or q == None or q == '':

        departments = get_department_pagenation(db,page_size,current_page)
        total = get_department_total(db)
    else:
        q = q.strip()
        departments = query_department(db,q,page_size,current_page)
        total = get_department_query_total(db,q)

    content = {
        "departments":departments,
        "pageSize":page_size,
        "pageTotal":total,
        "currentPage":current_page
    }
    return content