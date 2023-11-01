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

# token过期时间
EXPIRE_MINUTE = 60

app = FastAPI(
    title="知了网盘分享系统",
    description="知了网盘分享系统"
)


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

    pass


# 首页数据返回
@app.get("/index")
def Index(id:str=Depends(token.parse_token),db:Session=Depends(get_db)):
    user=get_user_by_id(db,int(id))
    ret_user = {"id":user.id,"username": user.username, "avatar": user.avatar, "ip": user.ip,
                "last_login_date": user.last_login_date.strftime("%Y-%m-%d")}
    return ret_user


if __name__ == '__main__':
    uvicorn.run(app="main:app", reload=True, host="0.0.0.0", port=8080)
