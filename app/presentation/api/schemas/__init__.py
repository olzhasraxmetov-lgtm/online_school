from app.presentation.api.schemas.answer import (
    AnswerOptionResponse,
    CreateAnswerOptionRequest,
    UpdateAnswerOptionRequest
)
from app.presentation.api.schemas.auth import (
    RegisterUserRequest,
    RegisteredUserResponse,
    LoginRequest,
    TokenResponse,
    CurrentUserResponse
)
from app.presentation.api.schemas.content.course import (
    CourseListItemResponse,
    CourseStructureResponse,
    CourseResponse,
    UpdateCourseRequest,
    CreateCourseRequest
)
from app.presentation.api.schemas.content.lecture import (
    LectureResponse,
    LectureStructureResponse,
    UpdateLectureRequest,
    CreateLectureRequest
)
from app.presentation.api.schemas.content.module import (
    ModuleStructureResponse,
    UpdateModuleRequest,
    CreateModuleRequest,
    ModuleResponse
)
from app.presentation.api.schemas.content.section import (
    SectionStructureResponse,
    UpdateSectionRequest,
    CreateSectionRequest,
    SectionResponse,
)
from app.presentation.api.schemas.errors import ErrorResponse
from app.presentation.api.schemas.question import (
    QuestionResponse,
    UpdateQuestionRequest,
    CreateQuestionRequest,
    UpdateQuestionRequest,
)

from app.presentation.api.schemas.question_attempts import (
    QuestionAttemptAnswerOptionResponse,
    StartQuestionAttemptResponse,
    SubmitQuestionAnswerRequest,
    QuestionAttemptResultResponse
)

__all__ = [
    "CourseListItemResponse",
    "CourseResponse",
    "CourseStructureResponse",
    "LectureResponse",
    "LectureStructureResponse",
    "ModuleStructureResponse",
    "SectionStructureResponse",
    "CreateCourseRequest",
    "UpdateCourseRequest",
    "CreateModuleRequest",
    "UpdateModuleRequest",
    "ModuleResponse",
    "CreateSectionRequest",
    "UpdateSectionRequest",
    "SectionResponse",
    "CreateLectureRequest",
    "UpdateLectureRequest",
    "CurrentUserResponse",
    "ErrorResponse",
    "QuestionResponse",
    "UpdateQuestionRequest",
    "CreateQuestionRequest",
    "UpdateQuestionRequest",
    "AnswerOptionResponse",
    "CreateAnswerOptionRequest",
    "UpdateAnswerOptionRequest",
    "QuestionAttemptAnswerOptionResponse",
    "StartQuestionAttemptResponse",
    "SubmitQuestionAnswerRequest",
    "QuestionAttemptResultResponse"
]