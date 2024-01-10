from pydantic import BaseModel, Field, validator
from typing import Optional, List


class WebPage(BaseModel):
    url: str
    content: str


class Knowledgebase(BaseModel):
    kb: list[WebPage]


class Config(BaseModel):
    urls: list[str]
    output_file_name: Optional[List[str]] = None
    max_pages_to_crawl: Optional[int] = Field(default=10)

    @validator("output_file_name", pre=True, always=True)
    def set_default_output_file_name(cls, value, values):
        if value is None:
            return ["output"] * len(values.get("urls", []))
        return value


class NoSitemapError(Exception):
    pass
