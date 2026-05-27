from fastapi import FastAPI,Request

app = FastAPI()

##中间件是自下而上执行的
@app.middleware("http")
async def middleware(request:Request, call_next):
    print('中间件1 start')
    response = await  call_next(request)
    print('中间件1 end')
    return response

@app.middleware("http")
async  def middleware2(request:Request, call_next):
    print('中间件2 start')
    response = await call_next(request)
    print('中间件2 end')
    return response
# 中间件2 start
# 中间件1 start
# 中间件1 end
# 中间件2 end

@app.get("/")
async def root():
    return {"message": "Hello World"}
