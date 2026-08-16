from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.application.use_cases.answer_options.create_answer_option import CreateAnswerOptionUseCase, \
    CreateAnswerOptionCommand
from app.application.use_cases.answer_options.update_answer_option import UpdateAnswerOptionUseCase, \
    UpdateAnswerOptionCommand
from app.application.use_cases.question.create_question import (
    CreateQuestionCommand,
    CreateQuestionUseCase,
)
from app.application.use_cases.question.update_question import UpdateQuestionUseCase, UpdateQuestionCommand
from app.domain.entities.user import User
from app.presentation.api.dependencies import (
    get_create_question_use_case,
    get_current_author_or_admin, get_update_answer_option_use_case, get_create_answer_option_use_case,
    get_update_question_use_case,
)
from app.presentation.api.schemas import (
    CreateQuestionRequest,
    ErrorResponse,
    QuestionResponse, UpdateQuestionRequest, AnswerOptionResponse, CreateAnswerOptionRequest, UpdateAnswerOptionRequest,
)

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    responses={
        401: {
            'description': 'Authentication credentials are missing or invalid.',
            'model': ErrorResponse,
        },
        403: {
            'description': 'Author or admin access is required.',
            'model': ErrorResponse,
        },
    },
)

@router.post(
    "/sections/{section_id}/questions/",
    response_model=QuestionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new question",
    description="Create a new question inside the selected section.",
)
async def create_question(
        section_id: UUID,
        request: CreateQuestionRequest,
        actor: User = Depends(get_current_author_or_admin),
        use_case: CreateQuestionUseCase = Depends(get_create_question_use_case),
) -> QuestionResponse:
    result = await use_case.execute(
        CreateQuestionCommand(
            actor=actor,
            section_id=section_id,
            text=request.text,
            position=request.position,
            question_type=request.question_type,
            max_attempts=request.max_attempts,
            reward_points=request.reward_points,
        )
    )
    return QuestionResponse.model_validate(result)

@router.put(
    "/questions/{question_id}/",
    response_model=QuestionResponse,
    summary="Update an existing question",
    description="Update an existing question inside the selected section.",
)
async def update_question(
        question_id: UUID,
        request: UpdateQuestionRequest,
        actor: User = Depends(get_current_author_or_admin),
        use_case: UpdateQuestionUseCase = Depends(get_update_question_use_case),
):
    result = await use_case.execute(
        UpdateQuestionCommand(
            actor=actor,
            question_id=question_id,
            text=request.text,
            position=request.position,
            question_type=request.question_type,
            max_attempts=request.max_attempts,
            reward_points=request.reward_points,
        )
    )
    return QuestionResponse.model_validate(result)

@router.post(
    "/questions/{question_id}/answers-options",
    response_model=AnswerOptionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new answer option",
    description="Create a new answer option inside the selected question.",
)
async def create_answer_option(
        question_id: UUID,
        request: CreateAnswerOptionRequest,
        actor: User = Depends(get_current_author_or_admin),
        use_case: CreateAnswerOptionUseCase = Depends(get_create_answer_option_use_case),
) -> AnswerOptionResponse:
    result = await use_case.execute(
        CreateAnswerOptionCommand(
            actor=actor,
            question_id=question_id,
            text=request.text,
            position=request.position,
            is_correct=request.is_correct,
        )
    )
    return AnswerOptionResponse.model_validate(result)

@router.put(
    '/answer-options/{answer_option_id}',
    response_model=AnswerOptionResponse,
    summary='Update answer option',
    description='Updates an existing answer option if the question was not used yet.',
)
async def update_answer_option(
    answer_option_id: UUID,
    request: UpdateAnswerOptionRequest,
    actor: User = Depends(get_current_author_or_admin),
    use_case: UpdateAnswerOptionUseCase = Depends(get_update_answer_option_use_case),
) -> AnswerOptionResponse:
    result = await use_case.execute(
        UpdateAnswerOptionCommand(
            actor=actor,
            answer_option_id=answer_option_id,
            text=request.text,
            position=request.position,
            is_correct=request.is_correct,
        )
    )
    return AnswerOptionResponse.model_validate(result)