from fastapi import FastAPI
from pydantic import BaseModel
from pydantic.fields import Field

app = FastAPI(title='Simple Math operations')


class Add(BaseModel):
    first_number: int = Field(title='First number')
    second_number: int = Field(title='Second number')


class Result(BaseModel):
    result: int = Field('Result')


@app.post('/add', response_model=Result)
async def create_item(item: Add):
    return {
        'result': item.first_number + item.second_number or 1
    }
