import uvicorn
from fastapi import FastAPI

app = FastAPI(
    title="知了网盘分享系统",
    description="知了网盘分享系统"
)


@app.post("/login")
def Login():
    #1.用户信息获取
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
