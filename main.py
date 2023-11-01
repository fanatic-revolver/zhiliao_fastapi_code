import uvicorn
from fastapi import FastAPI,Depends
from fastapi.security import OAuth2PasswordRequestForm

from fastapi.middleware.cors import CORSMiddleware
from extend.db import engine,SessionLocal,Base

app = FastAPI(
    title="知了网盘分享系统",
    description="知了网盘分享系统"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

#创建数据库表结构
Base.metadata.create_all(bind=engine)





@app.post("/login")
def Login(user:OAuth2PasswordRequestForm=Depends()):
    #1.用户信息获取
    username=user.username
    pwd=user.password
    #todo 密码加密
    #hash_pwd=
    #2.数据库校验
    #3.token生成
    #4.返回token及用户信息
    pass


# 首页数据返回
@app.get("/index")
def Index():
    pass


if __name__ == '__main__':
    uvicorn.run(app="main:app", reload=True, host="0.0.0.0", port=8080)
