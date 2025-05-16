from pydantic import BaseModel, Field, ValidationError
import requests
from typing import List, Dict, Optional, Tuple, ClassVar, Type
from enum import Enum
import logging
import time
from dotenv import load_dotenv
import os

from module.search import (
    WordInstance,
    SelectionInstance,
    get_selection_obj,
    get_word_obj,
)
from module.book_parser import Book
from module.prompts import WORD_PROMPT, SELECTION_PROMPT

logger = logging.getLogger()


class Kind(Enum):
    WORD = "WORD"
    SELCETION = "SELCETION"


class HeadersSchema(BaseModel):
    authorization: str = Field(default="", alias="Authorization")
    content_type: str = Field(default="application/json", alias="Content-Type")

    # Singleton instance
    _instance: ClassVar[Optional["HeadersSchema"]] = None

    @classmethod
    def create(cls, api_key: str) -> "HeadersSchema":
        if cls._instance is None:
            cls._instance = cls(Authorization=f"Bearer {api_key}")
        return cls._instance

    class Config:
        populate_by_name = True


class MessageSchema(BaseModel):
    role: str
    content: str


class PayloadSchema(BaseModel):
    model: str = "llama-3.1-8b-instant"
    messages: List[MessageSchema]
    temperature: float = 0.4
    stream: bool = False
    max_tokens: int = 6000
    response_format: Dict[str, str] = {"type": "json_object"}
    top_p: float = 0.8
    frequency_penalty: float = 1.0
    presence_penalty: float = 1.5


class UsageSchema(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChoiceSchema(BaseModel):
    message: MessageSchema
    finish_reason: str


class ResponseSchema(BaseModel):
    """Groq API Response Format"""

    choices: List[ChoiceSchema]
    usage: UsageSchema

    def get_content(self) -> str:
        return str(self.choices[0].message.content)

    def get_usage(self) -> Tuple[int, int]:
        return (
            self.usage.prompt_tokens,
            self.usage.completion_tokens,
        )


class WordReturnSchema(BaseModel):
    """format of return from api"""

    meaning: str
    definition: str
    synonyms: List[str]
    example_sentence: List[str]


class SelectionReturnSchema(BaseModel):
    """format of return from api"""

    spoiler_free_explination: str
    spoiler_explination: str


def get_response(
    request_body: PayloadSchema, headers: HeadersSchema, max_retries: int = 3
) -> Optional[ResponseSchema]:
    url = "https://api.groq.com/openai/v1/chat/completions"
    session = requests.session()
    logger.info("getting response")
    for attempt in range(1, max_retries + 1):
        try:
            response = session.post(
                url=url,
                headers=headers.model_dump(mode="json"),
                json=request_body.model_dump(mode="json"),
                timeout=5,
            )

            code = response.status_code
            logger.info(f"response: {response}")
            if code == 200:
                response_data = response.json()
                logger.info(
                    f"[Response] : 200 : Input_Tokens={response_data['usage']['prompt_tokens']} | Output_Tokens={response_data['usage']['completion_tokens']}  | Time={response_data['usage']['total_time']}"
                )
                return ResponseSchema.model_validate(response_data)

            elif code in [500, 502, 503, 504]:  # Retry for server errors
                logger.warning(
                    f"[Response] : Server error ({code}), retrying {attempt}/{max_retries}..."
                )
            else:
                logger.info(
                    f"[Response] : Server error ({code}), response: {response.text}"
                )
        except (
            requests.ConnectionError,
            requests.Timeout,
            requests.exceptions.RequestException,
        ) as e:
            logger.warning(
                f"[Response] : Connection error: {e}, retrying {attempt}/{max_retries}..."
            )
        time.sleep(2**attempt)  # Exponential backoff: 2s, 4s, 8s


def get_msg(kind: Kind, model: BaseModel) -> List[MessageSchema]:
    role, schema = (
        (WORD_PROMPT, WordReturnSchema)
        if kind == Kind.WORD
        else (SELECTION_PROMPT, SelectionReturnSchema)
    )
    return [
        MessageSchema(role="system", content=f"{role}{schema.model_json_schema()}"),
        MessageSchema(role="user", content=model.model_dump_json(by_alias=True)),
    ]


def validate_schema(
    data: MessageSchema, schema: Type[WordReturnSchema | SelectionReturnSchema]
):
    try:
        schema.model_validate_json(data.content)
    except Exception as e:
        raise ValidationError(e)


def get_word_meaning(word_payload: WordInstance) -> Optional[WordReturnSchema]:
    messages = get_msg(Kind.WORD, word_payload)
    payload = PayloadSchema(
        messages=messages,
    )
    headers = HeadersSchema()
    response = get_response(request_body=payload, headers=headers)
    if not response:
        raise Exception("Failed to get response")
    return validate_schema(response.choices[0].message, WordReturnSchema)


def get_selection_meaning(
    selection_payload: SelectionInstance,
) -> Optional[SelectionReturnSchema]:
    messages = get_msg(Kind.SELCETION, selection_payload)
    payload = PayloadSchema(
        messages=messages,
    )
    headers = HeadersSchema()
    response = get_response(request_body=payload, headers=headers)
    if not response:
        raise Exception("Failed to get response")
    return validate_schema(response.choices[0].message, SelectionReturnSchema)


def main():
    load_dotenv()
    api = os.environ.get("API")
    assert api
    header = HeadersSchema().create(api)

    book = Book()
    book.load("/home/prince/projects/book2/tests/stuff/test_books/LP.epub")
    selection = """raise five thousand roses in the same garden—and they do
not find in it what they are looking for."""
    model = get_word_obj(book, word="rose", sentance=selection)
    assert model
    mess = get_msg(kind=Kind.WORD, model=model)
    payload = PayloadSchema(messages=mess)
    print(get_response(request_body=payload, headers=header))
    print()
    print()
    print(model.model_dump_json())


if __name__ == "__main__":
    main()
