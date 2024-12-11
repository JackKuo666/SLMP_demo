import uvicorn as uvicorn
from fastapi import FastAPI, status
from pydantic import BaseModel
app = FastAPI()  # 必须实例化该类，启动的时候调用
from meta_extract import meta_extract


import logging

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='my.log', level=logging.DEBUG, format=LOG_FORMAT)
logging.FileHandler(filename='my.log', encoding="utf-8")


class Query(BaseModel):  # 必须继承
    url: str = None
    id: str = None


# post请求带参数数据
@app.post('/paperExtract')
def insert(query: Query):
    logging.info("url："+query.url)
    logging.info("id："+str(query.id))
    extract_result = meta_extract(query.url, query.id)
    logging.info("搜索结果："+str(extract_result))
    return extract_result


if __name__ == '__main__':
    uvicorn.run(app=app, host="0.0.0.0", port=8877)
    # 注意：如果供其他电脑调用需要改为 "0.0.0.0"，另外需要关闭电脑的防火墙



