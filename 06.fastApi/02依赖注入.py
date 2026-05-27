from fastapi import FastAPI, Query, Depends

app = FastAPI()

##注册依赖项
"""
ge:最小,大于等于---->gt大于
le：最大,小于等于--->lt小于
"""


async def common_parameter(
        page: int = Query(0, ge=0),
        pageSize: int = Query(10, le=60)
):
    return {'page': page, 'pageSize': pageSize}


@app.get("/query/carList")
async def queryCarList(result=Depends(common_parameter)):
    return result


@app.get("/query/userList")
async def queryCarList(result=Depends(common_parameter)):
    return result
