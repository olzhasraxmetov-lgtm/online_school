from fastapi import APIRouter, Depends
from starlette import status

from app.application.use_cases.users.auth_login import LoginUserUseCase, LoginUserCommand
from app.application.use_cases.users.register_user import RegisterUserUseCase, RegisterUserCommand
from app.presentation.api.dependencies import get_register_user_use_case, get_login_user_use_case
from app.presentation.api.schemas import RegisteredUserResponse, RegisterUserRequest, TokenResponse, LoginRequest

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register",
             response_model=RegisteredUserResponse,
             status_code=status.HTTP_201_CREATED)
async def register_user(
        request: RegisterUserRequest,
        use_case: RegisterUserUseCase = Depends(get_register_user_use_case),
) -> RegisteredUserResponse:
    result = await use_case.execute(
        RegisterUserCommand(
            email=request.email,
            password=request.password,
        )
    )
    return RegisteredUserResponse.model_validate(result)

@router.post("/login", response_model=TokenResponse)
async def login_user(
        request: LoginRequest,
        use_case: LoginUserUseCase = Depends(get_login_user_use_case),
) ->  TokenResponse:
    result = await use_case.execute(
        LoginUserCommand(
            email=request.email,
            password=request.password,
        )
    )
    return TokenResponse(
        access_token=result.access_token,
        token_type=result.token_type,
    )