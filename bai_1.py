from fastapi import FastAPI,HTTPException,Path,Query
from pydantic import BaseModel, Field
app = FastAPI()

courses = [
    {"id": 1, "code": "PY101", "name": "Python Basic", "duration": 30, "fee": 3000000},
    {"id": 2, "code": "API101", "name": "FastAPI Basic", "duration": 24, "fee": 2500000},
    {"id": 3, "code": "JV101", "name": "Java Basic", "duration": 40, "fee": 4000000}
]

class CourseCreate(BaseModel):
    code: str
    name: str = Field(...,min_length=1)
    duration: int = Field(gt=0)
    fee: int = Field(ge=0)
    
@app.post("/courses")
async def create_courses(course:CourseCreate):
    for i in courses:
        if i["code"] == course.code:
            raise HTTPException(status_code=409, detail="Course code already existed")
    if not courses:
        course_id = 1
    else:
        course_id = courses[-1]["id"] + 1
    new_course = {
        "id": course_id,
        "name": course.name,
        "duration": course.int,
        "fee": course.int}
    courses.append(new_course)
    return {"message": "Create course successfully",
            "data": new_course}
    
@app.get("/courses")
async def get_courses():
    return {"Danh sach": courses}

@app.get("/courses/{course_id}")
async def get_courses_id(course_id:int):
    reuslt = [course for course in courses if course_id == course["id"]]
    if not reuslt:
        raise HTTPException(status_code=404, detail="Course not found")
    return reuslt

@app.put("/courses/{course_id}")
async def update_courses(course_id:int,course:CourseCreate):
    reuslt = [course for course in courses if course_id == course["id"]]
    if not reuslt:
        raise HTTPException(status_code=404, detail="Course not found")
    course_found = reuslt[0]
    course_found.update({"code": course.code, "name": course.name, "duration": course.duration, "fee": course.fee})
    return {"message": "Update course successfully"} 
    
@app.delete("/courses/{course_id}")
async def delete_courses(course_id:int):
    reuslt = [course for course in courses if course_id == course["id"]]
    if not reuslt:
        raise HTTPException(status_code=404, detail="Course not found")
    course_found = reuslt[0]
    courses.remove(course_found)
    return {"message": "Delete course successfully"}

    
@app.get("/courses")
async def get_courses(keyword: str = Query(default=""),min_fee: int = Query(default="",ge=0), max_fee: int = Query(default="")):
    if keyword:
        courses_list = [course for course in courses if (keyword.lower() in course["code"].lower() or keyword.lower() in course["name"].lower())]
    if min_fee:
        courses_list = [course for course in courses if float(course["fee"]) >= min_fee]
    if max_fee:
        courses_list = [course for course in courses if float(course["fee"]) <= max_fee]
    return courses_list