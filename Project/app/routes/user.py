from fastapi import APIRouter, HTTPException, Response, Depends
from app.schemas.user import (
    CreateUserResponse,
    FullUserProfileInfo,
    MultipleUserResponse,
)
from app.services.user import UserService
import logging
import time

logger = logging.getLogger(__name__)
count = 0
start_time = time.time()
reset_interval = 10
limit = 5


def rate_limit(response: Response) -> Response:
    global start_time
    global count

    if time.time() > start_time + reset_interval:
        start_time = time.time()
        count = 0

    if count >= limit:
        raise HTTPException(status_code=429, detail={"error": "Rate limit exceeded",
                                                     "timeout": round(start_time + reset_interval - time.time(),
                                                                      2) + 0.01
                                                     })

    count += 1
    response.headers["X-app-rate-limit"] = f"{count}:{limit}"

    return Response


def create_user_router() -> APIRouter:
    user_router = APIRouter(
        prefix='/user',
        tags=['user'],
        dependencies=[Depends(rate_limit)]
    )
    user_service = UserService()

    # @user_router.get("/user/me", response_model=FullUserProfileInfo)
    # async def test_endpoint():
    #     full_user_profile = await user_service.get_user_info()
    #
    #     return full_user_profile

    # order maters. If user/me was after then we would get an internal erro
    # Path parameter
    # query parameters
    @user_router.get("/all", response_model=MultipleUserResponse)
    async def get_all_users_paginated(start: int = 0, limit: int = 2):
        users, total = await user_service.get_all_users_with_pagination(start, limit)
        formatted_users = MultipleUserResponse(users=users, total=total)

        return formatted_users

    @user_router.get("/{user_id}", response_model=FullUserProfileInfo)
    async def get_user_by_id(user_id: int):
        """
        Endpoint for retrieving a FullUserProfileInfo by the user's unique integer id.
        :param user_id: int - unique monotonically increasing integer id
        :return: FullUserProfileInfo
        """

        full_user_profile = await user_service.get_user_info(user_id)

        return full_user_profile

    @user_router.put("/{user_id}")
    async def update_user(user_id: int, full_profile_info: FullUserProfileInfo):
        await user_service.create_update_user(full_profile_info, user_id)

        return None

    @user_router.delete("/{user_id}")
    async def remove_user(user_id: int):
        logger.info(f"About to delete user_id: {user_id}")

        await user_service.delete_user(user_id)

    @user_router.post("/", response_model=CreateUserResponse, status_code=201)
    async def add_user(full_profile_info: FullUserProfileInfo):
        user_id = await user_service.create_update_user(full_profile_info)
        created_user = CreateUserResponse(user_id=user_id)

        return created_user

    return user_router
