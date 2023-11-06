from fastapi import APIRouter,Depends,Form
from sqlalchemy.orm import Session
from utils import token
from extend.get_db import get_db
from models.role.role_operation import \
    get_role_pagenation, \
    get_role_total,\
    role_update,\
    delete_role_by_id,\
    add_role,\
    query_role,\
    get_role_query_totle, \
    get_db_users,\
    add_role_users
    # get_permissions_tree,\
    # get_permission_ids_by_role_id,\
    # add_role_perms,\
    # get_role_id_by_user_id

from fastapi.responses import JSONResponse


from models.department.department_ret import DepartmentRet

router=APIRouter(
    prefix="/role"
)


@router.get("/role_list",tags=["角色模块"])
def get_role_list(page_size:int,current_page:int,id:str = Depends(token.parse_token),db:Session = Depends(get_db)):
    roles = get_role_pagenation(db,page_size,current_page)
    total = get_role_total(db)
    role_list = []
    for role in roles:
        this_role = {"name": role.name, "desc": role.desc, "id": role.id, "create_time": role.create_time}
        role_list.append(this_role)
    content = {
        "roles":role_list,
        "pageSize":page_size,
        "pageTotal":total,
        "currentPage":current_page
    }
    return content


#用户修改，涉及到图片上次，所有得用FormData这种方式提交
@router.post("/edit",tags=["角色模块"])
def edit(
        id: int = Form(...),
        name: str = Form(...),
        desc: str = Form(...),
        user_id:str = Depends(token.parse_token),
        db:Session = Depends(get_db)):
    role_update(db,id,name,desc)
    return {"code":200,"msg":"更新成功","id":id}


@router.post("/delete",tags=["角色模块"])
def delete_department(department:DepartmentRet,user_id:str = Depends(token.parse_token),
        db:Session = Depends(get_db)):
    id = department.id
    delete_role_by_id(db,id)
    return JSONResponse(content={"code":200,"msg":"删除成功","id":id})


@router.post("/add",tags=["角色模块"])
async def add(
        name: str = Form(...),
        leader: str = Form(None),
        desc: str = Form(...),

        user_id:str = Depends(token.parse_token),
        db:Session = Depends(get_db)):
    add_role(db,name,leader,desc)

    return JSONResponse(content={"code":200,"msg":"添加成功"})


# 查询
@router.get("/query",tags=["角色模块"])
def query(
        q:str,
        page_size:int,
        current_page:int,
        user_id: str = Depends(token.parse_token),
        db: Session = Depends(get_db)):

    if q == "" or q == None or q == '':

        roles = get_role_pagenation(db,page_size,current_page)
        total = get_role_total(db)
    else:
        q = q.strip()
        roles = query_role(db,q,page_size,current_page)
        total = get_role_query_totle(db,q)
    role_list=[]
    for role in roles:
        this_role={"name":role.name,"desc":role.desc,"id":role.id,"create_time":role.create_time}
        role_list.append(this_role)
    content = {
        "roles":role_list,
        "pageSize":page_size,
        "pageTotal":total,
        "currentPage":current_page
    }
    return content

@router.get("/get_users",tags=["角色模块"])
def get_users(role_id:int,user_id: str = Depends(token.parse_token),
        db: Session = Depends(get_db)):
    ret_dict = get_db_users(db,role_id)

    return {"code":200,"msg":"查询成功","ret":ret_dict}


# 角色配置用户
@router.post("/user_pz",tags=["角色模块"])
def user_pz(
        id: int = Form(...),
        users: str  = Form(...),
        user_id:str = Depends(token.parse_token),
        db:Session = Depends(get_db)):
    users = users.split(",")
    add_role_users(db,id,users)
    return {"code":200,"msg":"用户配置成功","id":id}

# # 角色权限配置
# @router.get("/get_permissions",tags=["角色模块"])
# def get_permissions(
#         role_id:int,
#         user_id:str = Depends(token.parse_token),
#         db:Session = Depends(get_db)):
#     # tree = json.dumps(get_permissions_tree(db,role_id))
#     tree = get_permissions_tree(db,role_id)
#
#     perms = get_permission_ids_by_role_id(db,role_id)
#     ret = {
#         # 所有的权限树
#         "tree":tree,
#         # 角色上已配置的权限
#         "checked":perms
#     }
#     return {"code":200,"msg":"查询成功","ret":ret}
#
#
# # 角色配置用户
# @router.post("/perm_pz",tags=["角色模块"])
# def perm_pz(
#         id: int = Form(...),
#         perms: str  = Form(...),
#         user_id:str = Depends(token.parse_token),
#         db:Session = Depends(get_db)):
#     perms = perms.split(",")
#     add_role_perms(db,id,perms)
#     return {"code":200,"msg":"权限配置成功","id":id}
#
# # 获取菜单
# from functools import reduce
# @router.get("/get_menus", tags=["角色模块"])
# def get_menus(
#         id: str = Depends(token.parse_token),
#         db: Session = Depends(get_db)
# ):
#     tree = get_role_id_by_user_id(db,int(id))
#
#     # 对重复的权限进行去重
#     run_function = lambda x, y: x if y in x else x + [y]
#
#     set_tree = reduce(run_function, [[], ] + tree)
#     # todo 假如tree为空，也就是没有权限，跳转到没有权限的页面
#     return {"code":200,"msg":"查询成功","tree":set_tree}