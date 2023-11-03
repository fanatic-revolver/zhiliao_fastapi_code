import uvicorn
from fastapi import FastAPI,Depends
from fastapi.security import OAuth2PasswordRequestForm

from fastapi.middleware.cors import CORSMiddleware
from extend.db import engine,SessionLocal,Base
from sqlalchemy.orm import Session
from extend.get_db import get_db
from utils.get_md5_data import get_md5_pwd
from models.user.user_operation import get_user_by_username_and_pwd,get_user_by_id
from fastapi.responses import JSONResponse
from utils import token
from datetime import timedelta
from apps.user.views import router as user_router

# token过期时间
EXPIRE_MINUTE = 60

app = FastAPI(
    title="知了网盘分享系统",
    description="知了网盘分享系统"
)

app.include_router(user_router)

# 跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

# 创建数据库表结构
Base.metadata.create_all(bind=engine)


@app.post("/login",name="用户登录")
def Login(user:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    # 1.用户信息获取
    username=user.username
    pwd=user.password
    # 密码加密
    md5_pwd=get_md5_pwd(pwd)
    # 2.数据库校验
    user=get_user_by_username_and_pwd(db, username, md5_pwd)
    if user:
        # 3.token生成
        expire_time = timedelta(minutes=EXPIRE_MINUTE)
        ret_token=token.create_token({"sub":str(user.id)},expire_time)
        # 4.返回token及用户信息
        ret_user={"username":user.username,"avatar":user.avatar,"ip":user.ip,"last_login_date":user.last_login_date.strftime("%Y-%m-%d")}
        content = {"code": 200, "msg": "登录成功","token":ret_token,"user":ret_user}
        return JSONResponse(content=content)
    else:
        content={"code":500,"msg":"用户名或密码错误"}
        return JSONResponse(content=content)


# 首页数据返回
@app.get("/index")
def Index(id:str=Depends(token.parse_token),db:Session=Depends(get_db)):
    user=get_user_by_id(db,int(id))
    ret_user = {"id":user.id,"username": user.username, "avatar": user.avatar, "ip": user.ip,
                "last_login_date": user.last_login_date.strftime("%Y-%m-%d")}
    #todo 图表数据需要从数据库动态查询
    schart_data={
        "labels":["1月","2月","3月","4月","5月","6月", "7月", "8月", "9月", "10月","11月","12月"],
        "datas":[
            [222,78,31,33,145,234, 278, 270, 190, 230,213,113],
            [111,56,69,52,111,164, 178, 150, 135, 160,267,129],
            [100,235,200,114,145,74, 218, 100, 135, 190,112,198]
        ]
    }
    content={
        "user":ret_user,
        #todo 数据需要从数据库查询
        "role":"管理员",
        "totalFiles":1000,
        "shareFiles":890,
        "personalFiles":90,
        "adminPer":25,
        "puPer":20,
        "staffPer":55,
        "schart_data":schart_data

    }
    return content




if __name__ == '__main__':
    uvicorn.run(app="main:app", reload=True, host="0.0.0.0", port=8080)
