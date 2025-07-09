from typing import List
from pydantic import BaseModel, Field
import requests


class EmbedRequest(BaseModel):
    input_: List[str] = Field(alias="input")
    model: str = "all-MiniLM-L6-v2"
    user: str = "0"


class Data(BaseModel):
    embedding: List[float]


class Usage(BaseModel):
    prompt_tokens: int
    total_tokens: int


class EmbedResponse(BaseModel):
    data: List[Data]


def call(payload: EmbedRequest):
    sess = requests.session()
    url = "http://localhost:8000/v1/embedding"
    try:
        res = sess.post(
            url,
            json=payload.model_dump(by_alias=True),
            headers={"Content-Type": "application/json"},
        )
        valid = EmbedResponse.model_validate(res.json())
        return valid
    except Exception as e:
        print(e)


def get_embbeding(input: str):
    payload = EmbedRequest(input=[input])
    out = call(payload)
    assert out
    return out.data[0].embedding
