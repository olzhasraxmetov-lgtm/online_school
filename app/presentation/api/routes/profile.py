from fastapi import APIRouter, Depends

from app.application.use_cases.profile.get_my_profile import (
    GetMyProfileQuery,
    GetMyProfileUseCase,
)
from app.application.use_cases.profile.update_my_profile import (
    UpdateMyProfileCommand,
    UpdateMyProfileUseCase,
)
from app.domain.entities.user import User
from app.presentation.api.dependencies import (
    get_current_user,
    get_get_my_profile_use_case,
    get_update_my_profile_use_case,
)
from app.presentation.api.schemas import ErrorResponse, UpdateMyProfileRequest, UserProfileResponse

router = APIRouter(prefix='/profile', tags=['Profile'])


@router.get(
    '/me',
    response_model=UserProfileResponse,
    summary='Get my profile',
    description='Returns the current authenticated user profile.',
    responses={
        401: {
            'description': 'Authentication credentials are missing or invalid.',
            'model': ErrorResponse,
        },
    },
)
async def get_my_profile(
    actor: User = Depends(get_current_user),
    use_case: GetMyProfileUseCase = Depends(get_get_my_profile_use_case),
) -> UserProfileResponse:
    result = await use_case.execute(GetMyProfileQuery(actor=actor))
    return UserProfileResponse.model_validate(result)


@router.patch(
    '/me',
    response_model=UserProfileResponse,
    summary='Update my profile',
    description='Updates the current authenticated user profile.',
    responses={
        401: {
            'description': 'Authentication credentials are missing or invalid.',
            'model': ErrorResponse,
        },
    },
)
async def update_my_profile(
    request: UpdateMyProfileRequest,
    actor: User = Depends(get_current_user),
    use_case: UpdateMyProfileUseCase = Depends(get_update_my_profile_use_case),
) -> UserProfileResponse:
    result = await use_case.execute(
        UpdateMyProfileCommand(
            actor=actor,
            full_name=request.full_name,
            bio=request.bio,
            avatar_url=str(request.avatar_url) if request.avatar_url is not None else None,
        )
    )
    return UserProfileResponse.model_validate(result)