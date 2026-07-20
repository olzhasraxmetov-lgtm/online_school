from uuid import UUID

from fastapi import APIRouter, Depends
from starlette import status

from app.application.use_cases.courses.create_course import CreateCourseUseCase, CreateCourseCommand
from app.application.use_cases.courses.update_course import UpdateCourseUseCase, UpdateCourseCommand
from app.application.use_cases.lectures.create_lecture import CreateLectureCommand, CreateLectureUseCase
from app.application.use_cases.lectures.update_lecture import UpdateLectureCommand, UpdateLectureUseCase
from app.application.use_cases.modules.create_module import CreateModuleCommand, CreateModuleUseCase
from app.application.use_cases.modules.update_module import UpdateModuleUseCase, UpdateModuleCommand
from app.application.use_cases.sections.create_section import CreateSectionUseCase, CreateSectionCommand
from app.application.use_cases.sections.update_section import UpdateSectionCommand, UpdateSectionUseCase
from app.presentation.api.dependencies import get_update_module_use_case, get_create_module_use_case, \
    get_update_section_use_case, get_create_section_use_case, get_update_lecture_use_case, get_create_lecture_use_case, \
    get_update_course_use_case, get_create_course_use_case
from app.presentation.api.schemas import ErrorResponse
from app.presentation.api.schemas.content.course import CourseResponse, CreateCourseRequest, UpdateCourseRequest
from app.presentation.api.schemas.content.lecture import LectureResponse, UpdateLectureRequest, CreateLectureRequest
from app.presentation.api.schemas.content.module import UpdateModuleRequest, ModuleResponse, CreateModuleRequest
from app.presentation.api.schemas.content.section import SectionResponse, CreateSectionRequest, UpdateSectionRequest

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post(
    "/courses",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a course",
    description="Create a new course in the administrative API",
    responses={
        400: {
            "description": "Domain or Application validation error",
            "model": ErrorResponse,
        }
    }
)
async def create_course(
        request: CreateCourseRequest,
        use_case: CreateCourseUseCase = Depends(get_create_course_use_case),
) -> CourseResponse:
    result  = await use_case.execute(
        CreateCourseCommand(title=request.title, description=request.description)
    )
    return CourseResponse.model_validate(result)

@router.put(
    "/courses/{course_id}",
    response_model=CourseResponse,
    summary="Update a course",
    description=(
            "Update a course in the administrative API. "
            "Allow changing the course title and description."
    ),
    responses={
        400: {
            "description": "Domain or Application validation error.",
            "model": ErrorResponse,
        },
        404: {
            "description": "Course not found.",
            "model": ErrorResponse,
        }
    }
)
async def update_course(
        course_id: UUID,
        request: UpdateCourseRequest,
        use_case: UpdateCourseUseCase = Depends(get_update_course_use_case),
) -> CourseResponse:
    result  = await use_case.execute(
        UpdateCourseCommand(
            course_id=course_id,
            title=request.title,
            description=request.description,
        )
    )
    return CourseResponse.model_validate(result)

@router.post(
    "/courses/{course_id}/modules",
    response_model=ModuleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a module ",
    description="Create a new module inside an existing course",
    responses={
        400: {
            "description": "Domain or Application validation error",
            "model": ErrorResponse,
        },
        404: {
            "description": "Course not found.",
            "model": ErrorResponse,
        }
    }
)
async def create_module(
    course_id: UUID,
    request: CreateModuleRequest,
    use_case: CreateModuleUseCase = Depends(get_create_module_use_case),
) -> ModuleResponse:
    result = await use_case.execute(
        CreateModuleCommand(
            course_id=course_id,
            title=request.title,
            description=request.description,
            position=request.position,
        )
    )
    return ModuleResponse.model_validate(result)


@router.put(
    "/modules/{module_id}",
    response_model=ModuleResponse,
    summary="Update a module",
    description=(
            "Update a module in the administrative API by its ID. "
            "Allow changing the module title, position and description."
    ),
    responses={
        400: {
            "description": "Domain or Application validation error.",
            "model": ErrorResponse,
        },
        404: {
            "description": "Module not found.",
            "model": ErrorResponse,
        }
    }
)
async def update_module(
    module_id: UUID,
    request: UpdateModuleRequest,
    use_case: UpdateModuleUseCase = Depends(get_update_module_use_case),
) -> ModuleResponse:
    result = await use_case.execute(
        UpdateModuleCommand(
            module_id=module_id,
            title=request.title,
            description=request.description,
            position=request.position,
        )
    )
    return ModuleResponse.model_validate(result)

@router.post(
    "/modules/{module_id}/sections",
    response_model=SectionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a section",
    description=(
            "Creates a new section inside an existing module."
    ),
    responses={
        400: {
            "description": "Domain or application validation error.",
            "model": ErrorResponse,
        },
        404: {
            "description": "Module not found.",
            "model": ErrorResponse,
        },
    },
)
async def create_section(
    module_id: UUID,
    request: CreateSectionRequest,
    use_case: CreateSectionUseCase = Depends(get_create_section_use_case),
) -> SectionResponse:
    result = await use_case.execute(
        CreateSectionCommand(
            module_id=module_id,
            title=request.title,
            description=request.description,
            position=request.position,
        )
    )
    return SectionResponse.model_validate(result)


@router.put(
    "/sections/{section_id}",
    response_model=SectionResponse,
    summary="Update section",
    description=(
            "Updates an existing section by its identifier. "
            "Allows changing the section title, description and position."
    ),
    responses={
        400: {
            "description": "Domain or application validation error.",
            "model": ErrorResponse,
        },
        404: {
            "description": "Section not found.",
            "model": ErrorResponse,
        },
    },
)
async def update_section(
    section_id: UUID,
    request: UpdateSectionRequest,
    use_case: UpdateSectionUseCase = Depends(get_update_section_use_case),
) -> SectionResponse:
    result = await use_case.execute(
        UpdateSectionCommand(
            section_id=section_id,
            title=request.title,
            description=request.description,
            position=request.position,
        )
    )
    return SectionResponse.model_validate(result)

@router.post(
    "/sections/{section_id}/lectures",
    response_model=LectureResponse,
    status_code=status.HTTP_201_CREATED,
    description=(
            "Creates a new lecture inside an existing section. "
    ),
    responses={
        400: {
            "description": "Domain or application validation error.",
            "model": ErrorResponse,
        },
        404: {
            "description": "Section not found.",
            "model": ErrorResponse,
        },
    },
)
async def create_lecture(
    section_id: UUID,
    request: CreateLectureRequest,
    use_case: CreateLectureUseCase = Depends(get_create_lecture_use_case),
) -> LectureResponse:
    result = await use_case.execute(
        CreateLectureCommand(
            section_id=section_id,
            title=request.title,
            content=request.content,
            position=request.position,
        )
    )
    return LectureResponse.model_validate(result)


@router.put(
    "/lectures/{lecture_id}",
    response_model=LectureResponse,
    description=(
            "Updates an existing lecture by its identifier. "
            "Allows changing the lecture title, content and position."
    ),
    responses={
        400: {
            "description": "Domain or application validation error.",
            "model": ErrorResponse,
        },
        404: {
            "description": "Lecture not found.",
            "model": ErrorResponse,
        },
    },
)
async def update_lecture(
    lecture_id: UUID,
    request: UpdateLectureRequest,
    use_case: UpdateLectureUseCase = Depends(get_update_lecture_use_case),
) -> LectureResponse:
    result = await use_case.execute(
        UpdateLectureCommand(
            lecture_id=lecture_id,
            title=request.title,
            content=request.content,
            position=request.position,
        )
    )
    return LectureResponse.model_validate(result)