'''
Our first HTTP API!
'''
from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def root():
  return {'message': 'Hello World'}


@app.get('/predict')
async def predict(parameter: str = 'implement-me'):
  return parameter
