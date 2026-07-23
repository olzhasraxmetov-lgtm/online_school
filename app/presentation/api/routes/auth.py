from fastapi import APIRouter, Depends
from starlette import status

from app.application.use_cases.users.auth_login import LoginUserUseCase, LoginUserCommand
from app.application.use_cases.users.register_user import RegisterUserUseCase, RegisterUserCommand
from app.domain.entities.user import User
from app.presentation.api.dependencies import get_register_user_use_case, get_login_user_use_case, get_current_user
from app.presentation.api.schemas import RegisteredUserResponse, RegisterUserRequest, TokenResponse, LoginRequest, \
    CurrentUserResponse, ErrorResponse

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.get(
    "/me",
    response_model=CurrentUserResponse,
    summary="Get current user",
    description="Return the current user which is resolved from Bearer token",
    responses={
        401: {
            "description": "Authentication credentials were not provided.",
            "model": ErrorResponse,
        }
    }
)
async def get_me(
        current_user: User = Depends(get_current_user),
) -> CurrentUserResponse:
    return CurrentUserResponse.model_value(current_user)


@router.post(
    "/register",
         response_model=RegisteredUserResponse,
         status_code=status.HTTP_201_CREATED,
        summary="Register new user",
        description=(
            "Creates a new user account in the system. "
            "A public registration always creates a user with student role"
        ),
        responses={
                400:{
                    "description": "Domain or Application validation error",
                    "model": ErrorResponse,
                }
            }
        )
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

@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login user",
    description=(
        "Authenticated a user by email and password and return a JWT access token. "
    ),
    responses={
        400: {
            "description": "Domain or Application validation error",
            "model": ErrorResponse,
        }
    }

)
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