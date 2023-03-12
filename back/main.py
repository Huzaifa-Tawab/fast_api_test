from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import binascii
from src.database import interect_with_database
from src.utils import (
    get_filter_options,
    get_full_info,
    apply_filter,
    get_full_convo,
    get_clients_info,
    send_sms,
    get_client_data_all,
    create_new_client,
    get_crm_auth,
    delete_client,
    update_password,
    get_all_blogs,
    new_blog_post,
    new_crm_user,
    upload_user_docs,
    delete_user_docs,
)
from src.models import (
    CourseInfoSchema,
    ApplyFilterSchema,
    GetConvo,
    CrmAuthSchema,
    ClientDataSchema,
    NewClientSchema,
    FileSchema,
    FetchUserDataSchema,
    CrmAuthSchema,
    DeleteClientSchema,
    ChangePassSchema,
    NewBlogPostSchema,
    NewUserSchema,
    UploadFileSchema,
    SendMessageSchema,
    DeleteUserDocsModel,
)
import os
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/Images", StaticFiles(directory="Images"), name="Images")


"""
// to start the script type in terminal
uvicorn main:app

// for Swagger UI - Testing API from UI
http://127.0.0.1:8000/docs

// example of body for endpoint2
{
	"course_id": 1654833,
}

// example of body for endpoint3
{
	"search": "",
	"limit": 100,
	"Country": ["All"],
	"Duration (years)": [2, 3],
	"Degree Level": ["Bachelors","Certificate","Diploma"],
	"Discipline": ["All"],
	"Fee": [1203255.96, 13068627.27],
	"Institute": ["University"],
	"Language": ["All"],
}
"""

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print(" -------- APP STARTED -------- ")

@app.get("/")
async def index():
    return "This is the back-end for YEC"

@app.get("/get_filter_options")
async def end_point_1():
    return interect_with_database(
        lambda mycursor: get_filter_options(mycursor)
    )
    
@app.post("/get_course_info")
async def end_point_2(course_info_schema: CourseInfoSchema):
    return interect_with_database(
        lambda mycursor: get_full_info(mycursor, course_info_schema.course_id)
    )

@app.post("/apply_filter")
async def end_point_3(apply_filter_schema: ApplyFilterSchema):
    body = {
        "search": apply_filter_schema.search,
        "start": apply_filter_schema.start,
        "end": apply_filter_schema.end,
        "Country": apply_filter_schema.country,
        "Duration (years)": apply_filter_schema.duration,
        "Degree Level": apply_filter_schema.degree_level,
        "Discipline": apply_filter_schema.discipline,
        "Fee": apply_filter_schema.fee,
        "Institute": apply_filter_schema.institute,
        "Language": apply_filter_schema.language,
    }
    return interect_with_database(
        lambda mycursor: apply_filter(mycursor, body)
    )


@app.get("/get_clients")
async def end_point_6():
    return interect_with_database(
        lambda mycursor: get_clients_info(mycursor)
    )


@app.post("/get_convo")
async def end_point_4(GetConvo: GetConvo):
    return interect_with_database(
        lambda mycursor: get_full_convo(mycursor, GetConvo.id)
    )


@app.post("/sendmassage")
async def end_point_7(SendMessageSchema: SendMessageSchema):
    body = {
        "client_id": SendMessageSchema.id,
        "sender_name": SendMessageSchema.sender_name,
        "message": SendMessageSchema.message,
    }
    return interect_with_database(
        lambda mycursor: send_sms(mycursor, body),
        commit = True,
    )


@app.post("/get_client_data")
async def end_point_8(client_data_schema: ClientDataSchema):
    return interect_with_database(
        lambda mycursor: get_client_data_all(mycursor, client_data_schema.client_id)
    )


@app.post("/create_new")
async def end_point_9(NewClientSchema: NewClientSchema):
    body = {
        "name": NewClientSchema.name,
        "email": NewClientSchema.email,
        "phone": NewClientSchema.phone,
        "address": NewClientSchema.address,
    }
    return interect_with_database(
        lambda mycursor: create_new_client(mycursor, body),
        commit = True,
    )


@app.post("/fetch_user-docs")
async def end_point10(FetchUserDataSchema: FetchUserDataSchema):
    dict = {}
    subDir = ""
    parentDir = "Images/ClientsData/"
    imgDir = ""
    entries = os.listdir(parentDir)
    for entry in entries:
        if entry == FetchUserDataSchema.id:
            subDir = entry
            print("found it")
            print(entry)
            items = os.listdir(parentDir + subDir)
            for item in items:
                x = item.split(".")
                print(x[0])
                imgDir = parentDir + subDir + "/" + item
                dict[x[0]] = {imgDir}
    return dict


@app.post("/files")
async def UploadImage(FileSchema: FileSchema):
    imgDir = "Images/ClientsData/" + FileSchema.id
    print(imgDir)
    for item in FileSchema:
        # print(item)
        if item[0] != "id":
            if item[1][0] != "null":
                x = item[1][0].split("/")
                fulldir = imgDir + "/" + item[0] + "." + x[1]
                y = bytes(item[1][1], "utf8")
                with open(fulldir, "wb") as image:
                    image.write(y)
                    image.close()


@app.get("/test101")
async def end_point101():
    dict = {}
    subDir = ""
    parentDir = "Images/ClientsData/"
    imgDir = ""
    entries = os.listdir(parentDir)
    for entry in entries:
        if entry == "huzaifa":
            subDir = entry
            items = os.listdir(parentDir + subDir)
            for item in items:
                x = item.split(".")
                print(x[0])
                imgDir = parentDir + subDir + "/" + item

                with open(imgDir, "rb") as f:
                    z = f.read()
                    data = binascii.hexlify(z)
                    dict[x[0]] = {x[1], data}
    return dict


@app.post("/crm-auth")
async def end_point_11(CrmAuthSchema: CrmAuthSchema):
    body = {
        "Email": CrmAuthSchema.email,
        "Password": CrmAuthSchema.password,
    }
    return interect_with_database(
        lambda mycursor: get_crm_auth(mycursor, body)
    )


@app.post("/delete_client")
async def end_point_12(DeleteClientSchema: DeleteClientSchema):

    return interect_with_database(
        lambda mycursor: delete_client(mycursor, DeleteClientSchema.id),
        commit = True,
    )


@app.post("/change_password")
async def end_point_13(ChangePassSchema: ChangePassSchema):
    body = {"email": ChangePassSchema.email, "pswd": ChangePassSchema.password}
    return interect_with_database(
        lambda mycursor: update_password(mycursor, body),
        commit = True,
    )


@app.get("/get_blogs")
async def end_point_14():
    return interect_with_database(
        lambda mycursor: get_all_blogs(mycursor)
    )

# ========= DEMO FUNCTION ========= 

@app.post("/create_new_blog")
async def end_point_15(
    file: UploadFile = File(),
    title: str = Form(),
    decs: str = Form(),
    cat: str = Form(),
):
    body = {"title": title, "decs": decs, "cat": cat}
    return interect_with_database(
        lambda mycursor: new_blog_post(mycursor, body, file),
        commit = True,
    )

# ========= NEW FUNCTION ========= 

@app.post("/upload_user_docs")
async def end_point_17(
    phone_no: str = Form(),
    # List for Student
    transcripts: UploadFile = None,
    ssc_olevels: UploadFile = None,
    hssc_alevels: UploadFile = None,
    bachelors: UploadFile = None,
    masters: UploadFile = None,
    # If Financial
    bank_statement: UploadFile = None,
    account_maintenance_certificate: UploadFile = None,
    sponsor_bank_statement: UploadFile = None,
    affidavit_of_Support: UploadFile = None,
    declaration: UploadFile = None,
    # ID
    id_card: UploadFile = None,
    passport: UploadFile = None,
    # If Employed
    salary_slips: UploadFile = None,
    employment_letter: UploadFile = None,
):
    return upload_user_docs(
        phone_no,
        # List for Student
        transcripts = transcripts,
        ssc_olevels = ssc_olevels,
        hssc_alevels = hssc_alevels,
        bachelors = bachelors,
        masters = masters,
        # If Financial
        bank_statement = bank_statement,
        account_maintenance_certificate = account_maintenance_certificate,
        sponsor_bank_statement = sponsor_bank_statement,
        affidavit_of_Support = affidavit_of_Support,
        declaration = declaration,
        # ID
        id_card = id_card,
        passport = passport,
        # If Employed
        salary_slips = salary_slips,
        employment_letter = employment_letter,
    )

@app.post("/delete_user_docs")
async def end_point_18(req: DeleteUserDocsModel):
    return delete_user_docs(req.phone_no, req.delete)

@app.post("/create_new_crm_user")
async def end_point_16(NewUserSchema: NewUserSchema):
    body = {
        "name": NewUserSchema.name,
        "email": NewUserSchema.email,
        "password": NewUserSchema.password,
        "usertype": NewUserSchema.usertype,
    }
    return interect_with_database(
        lambda mycursor: new_crm_user(mycursor, body),
        commit = True,
    )
