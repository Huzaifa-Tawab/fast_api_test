from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile, Form

class CourseInfoSchema(BaseModel):
    course_id: int

class DeleteUserDocsModel(BaseModel):
    phone_no: str
    # List for Student
    delete: list = []

class ClientDataSchema(BaseModel):
    client_id: int


class ApplyFilterSchema(BaseModel):
    search: str = ""
    start: int = 0
    end: int = 30
    country: list = ["All"]
    duration: list = [0, 99999999999]
    degree_level: list = ["All"]
    discipline: list = ["All"]
    fee: list = [0, 99999999999]
    institute: list = ["All"]
    language: list = ["All"]


class GetConvo(BaseModel):
    id: int


class SendMessageSchema(BaseModel):
    id: str
    sender_name: str
    message: str


class NewClientSchema(BaseModel):
    name: str
    phone: str
    email: str
    address: str


class FileSchema(BaseModel):
    id: str
    passport: list = ["File Type", "BIN Code"]
    cnic: list = ["File Type", "BIN Code"]


class FetchUserDataSchema(BaseModel):
    id: str


class CrmAuthSchema(BaseModel):
    email: str
    password: str


class DeleteClientSchema(BaseModel):
    id: str


class ChangePassSchema(BaseModel):
    email: str
    password: str


class NewBlogPostSchema(BaseModel):
    img: UploadFile


class NewUserSchema(BaseModel):
    name: str
    email: str
    password: str
    usertype: str = "Default"


class UploadFileSchema(BaseModel):
    file: UploadFile
