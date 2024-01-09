# generated by fastapi-codegen:
#   filename:  ./frequency/api/v1/server.yaml
#   timestamp: 2024-01-07T04:28:40+00:00

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class V1Health(BaseModel):
    status: Optional[str] = None


class V1Info(BaseModel):
    version: Optional[str] = None


class V1LoadModelRequest(BaseModel):
    name: str
    type: str
    hf_repo: str
    cuda: Optional[bool] = None


class V1Model(BaseModel):
    name: str
    type: str
    hf_repo: str
    cuda: Optional[bool] = None
    adapters: Optional[List[str]] = None


class V1Models(BaseModel):
    models: List[V1Model]


class V1ChatRequest(BaseModel):
    query: str
    adapters: Optional[List[str]] = None
    history: Optional[List] = Field(None, description='A chat history')


class V1ChatResponse(BaseModel):
    text: str
    history: Optional[List] = Field(None, description='A chat history')


class V1Adapter(BaseModel):
    name: str
    uri: Optional[str] = None
    hf_repo: Optional[str] = None
    model: str


class V1Adapters(BaseModel):
    adapters: List[V1Adapter]
