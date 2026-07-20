from uuid import UUID

from fastapi import APIRouter, Depends

from app.application.use_cases.courses.get_course import GetCourseUseCase, GetCourseQuery
from app.application.use_cases.courses.get_course_structure import GetCourseStructureUseCase, GetCourseStructureQuery
from app.application.use_cases.courses.get_courses import GetCoursesUseCase, GetCoursesQuery
from app.application.use_cases.lectures.get_lecture import GetLectureUseCase, GetLectureQuery
from app.presentation.api.dependencies import (
    get_get_course_use_case, get_get_courses_use_case, get_get_course_structure_use_case, get_get_lecture_use_case,
)
from app.presentation.api.schemas import (
    CourseListItemResponse, ErrorResponse,
)
from app.presentation.api.schemas.content.course import CourseResponse, CourseStructureResponse
from app.presentation.api.schemas.content.lecture import LectureResponse

router = APIRouter(tags=["Content"])

@router.get(
    "/courses",
    response_model=list[CourseListItemResponse],
    summary="List of available courses",
    description="Returns a public list of available courses.",
)
async def get_courses(
        use_case: GetCoursesUseCase = Depends(get_get_courses_use_case),
) -> list[CourseListItemResponse]:
    result = await use_case.execute(GetCoursesQuery())
    return [CourseListItemResponse.model_validate(course) for course in result]

@router.get(
    "/courses/{course_id}",
    response_model=CourseResponse,
    summary="Get course by id",
    description="Returns a course by id.",
    responses={
        404: {
            "description": "Course not found",
            "model": ErrorResponse,
        }
    }
)
async def get_course(
        course_id: UUID,
        use_case: GetCourseUseCase = Depends(get_get_course_use_case),
) -> CourseResponse:
    result  = await use_case.execute(GetCourseQuery(course_id))
    return CourseResponse.model_validate(result)

@router.get(
    "/courses/{course_id}/structure}",
    response_model=CourseStructureResponse,
    summary="Get course structure",
    description=(
            "Returns the course navigation tree: modules, sections and lectures "
            "without full lecture content."
    ),
    responses={
        404: {
            "description": "Course was not found",
            "model": ErrorResponse,
        }
    }
)
async def get_courses(
        course_id: UUID,
        use_case: GetCourseStructureUseCase = Depends(get_get_course_structure_use_case),
) -> CourseStructureResponse:
    result = await use_case.execute(GetCourseStructureQuery(course_id))
    return CourseStructureResponse.model_validate(result)

@router.get(
    "/lectures/{lecture_id}",
    response_model=LectureResponse,
    summary="Get lecture by id",
    description="Returns a lecture by id.",
    responses={
        404: {
            "description": "Lecture was not found.",
            "model": ErrorResponse,
        },
    },
)
async def get_lecture(
        lecture_id: UUID,
        use_case: GetLectureUseCase = Depends(get_get_lecture_use_case),
) -> LectureResponse:
    result = await use_case.execute(GetLectureQuery(lecture_id=lecture_id))
    return LectureResponse.model_validate(result)