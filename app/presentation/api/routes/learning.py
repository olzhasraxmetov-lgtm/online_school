from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.application.use_cases.code_submissions.submit_code_submission import SubmitCodeSubmissionUseCase, \
    SubmitCodeSubmissionCommand
from app.application.use_cases.question_attempts.get_question_attempt_result import GetQuestionAttemptResultUseCase, \
    GetQuestionAttemptResultCommand
from app.application.use_cases.question_attempts.start_question_attempt import (
    StartQuestionAttemptUseCase, StartQuestionAttemptCommand,
)
from app.application.use_cases.question_attempts.submit_question_answer import SubmitQuestionAnswerUseCase, \
    SubmitQuestionAnswerCommand
from app.application.use_cases.task_attempts.submit_task_answer import SubmitTaskAnswerUseCase, SubmitTaskAnswerCommand
from app.domain.entities.user import User
from app.presentation.api.dependencies import (
    get_current_user,
    get_start_question_attempt_use_case, get_submit_question_answer_use_case, get_get_question_attempt_result_use_case,
    get_submit_code_submission_use_case,
)
from app.presentation.api.schemas import (
    ErrorResponse,
    StartQuestionAttemptResponse, QuestionAttemptResultResponse, SubmitQuestionAnswerRequest, TaskAttemptResponse,
    SubmitTaskAnswerRequest, CodeSubmissionResponse, SubmitCodeSubmissionRequest,
)

router = APIRouter(
    prefix="/learning",
    tags=["Learning"],
    responses={
        401: {
            'description': 'Authentication credentials are missing or invalid.',
            'model': ErrorResponse,
        },
        403: {
            'description': 'User cannot perform this learning action.',
            'model': ErrorResponse,
        },
    },
)

@router.get(
    "/questions/{question_id}/attempt",
    response_model=StartQuestionAttemptResponse,
    summary="Get a question attempt",
    description="Returns all data required before the student submits a new answer.",
)
async def start_question_attempt(
        question_id: UUID,
        actor: User = Depends(get_current_user),
        use_case: StartQuestionAttemptUseCase = Depends(get_start_question_attempt_use_case)
) -> StartQuestionAttemptResponse:
    result = await use_case.execute(
        StartQuestionAttemptCommand(
            actor=actor,
            question_id=question_id,
        )
    )
    return StartQuestionAttemptResponse.model_validate(result)

@router.post(
    '/questions/{question_id}/attempts',
    response_model=QuestionAttemptResultResponse,
    status_code=status.HTTP_201_CREATED,
    summary='Submit question answer',
    description='Creates a new question attempt and immediately applies the result.',
)
async def submit_question_answer(
        question_id: UUID,
        request: SubmitQuestionAnswerRequest,
        actor: User = Depends(get_current_user),
        use_case: SubmitQuestionAnswerUseCase = Depends(get_submit_question_answer_use_case),
) -> QuestionAttemptResultResponse:
    result = await use_case.execute(
        SubmitQuestionAnswerCommand(
            actor=actor,
            question_id=question_id,
            selected_option_ids=request.selected_option_ids,
        )
    )
    return QuestionAttemptResultResponse(
        attempt_id=result.id,
        question_id=result.question_id,
        attempt_number=result.attempt_number,
        result_status=result.result_status,
        awarded_points=result.awarded_points,
        checked_at=result.checked_at,
        selected_option_ids=list(result.selected_option_ids),
    )

@router.get(
    '/attempts/{attempt_id}/result',
    response_model=QuestionAttemptResultResponse,
    summary='Get question attempt result',
    description='Returns a previously stored result of the selected question attempt.',
)
async def get_question_attempt_result(
        attempt_id: UUID,
        actor: User = Depends(get_current_user),
        use_case: GetQuestionAttemptResultUseCase = Depends(
            get_get_question_attempt_result_use_case),
) -> QuestionAttemptResultResponse:
    result = await use_case.execute(
        GetQuestionAttemptResultCommand(
            actor=actor,
            attempt_id=attempt_id,
        )
    )
    return QuestionAttemptResultResponse.model_validate(result)

@router.post(
    '/tasks/{task_id}/attempts',
    response_model=TaskAttemptResponse,
    status_code=status.HTTP_201_CREATED,
    summary='Submit task answer',
    description='Creates a new task attempt and immediately applies the result.',
)
async def submit_task_answer(
        task_id: UUID,
        request: SubmitTaskAnswerRequest,
        actor: User = Depends(get_current_user),
        use_case: SubmitTaskAnswerUseCase = Depends(get_submit_question_answer_use_case)
) -> TaskAttemptResponse:
    result = await use_case.execute(
        SubmitTaskAnswerCommand(
            actor=actor,
            task_id=task_id,
            submitted_answer=request.submitted_answer,
        )
    )
    return TaskAttemptResponse.model_validate(result)

@router.post(
    '/code-tasks/{code_task_id}/submissions',
    response_model=CodeSubmissionResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary='Submit code solution',
    description='Creates a new code submission and hands it off to asynchronous checking.',
)
async def submit_code_submission(
    code_task_id: UUID,
    request: SubmitCodeSubmissionRequest,
    actor: User = Depends(get_current_user),
    use_case: SubmitCodeSubmissionUseCase = Depends(get_submit_code_submission_use_case),
) -> CodeSubmissionResponse:
    result = await use_case.execute(
        SubmitCodeSubmissionCommand(
            actor=actor,
            code_task_id=code_task_id,
            source_code=request.source_code,
        )
    )
    return CodeSubmissionResponse.model_validate(result)