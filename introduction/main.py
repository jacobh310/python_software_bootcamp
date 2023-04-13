from queue import Full

from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()


class User(BaseModel):
    liked_posts: Optional[list[int]] = None
    username: str = Field(
        alias='name',
        title='The Username',
        description='This is the username of the user',
        min_length=1,
        max_length=20,
        default=None
    )


class FullUserProfileInfo(User):
    short_description: str
    long_bio: str

class MultipleUserResponse(BaseModel):
    users: list[FullUserProfileInfo]
    total: int

class CreateUserResponse(BaseModel):
    user_id: int

profile_infos = {
    0: {'short_description': 'Facts about me',
                'long_bio': 'More facts about me'},
}

user_contents = {
    0: {
        'liked_posts': [5] * 2,
    }
}


def get_user_info(user_id: int = 0) -> FullUserProfileInfo:

    # currently reading from dictionary
    profile_info = profile_infos[user_id]
    user_content = user_contents[user_id]
   # later read from database
    # db case here we can wait

    user = User(**user_content)

    full_user_profile = {**profile_info,
                         **user.dict()}

    profile_info = FullUserProfileInfo(**full_user_profile)

    return profile_info

def get_all_users_with_pagination(start:int, limit:int)->(list[FullUserProfileInfo], int):
    list_of_users = []
    keys = profile_infos.keys()
    total = len(keys)
    for i in range(0, len(keys), 1):
        if i < start:
            continue
        current_key = list(keys)[i]
        user = get_user_info(current_key)
        list_of_users.append(user)

        if len(list_of_users) >= limit:
            break

    return list_of_users, total
def create_update_user(full_profile_info: FullUserProfileInfo, user_id=None) -> int:
    """
    Creates a new user or updates an existing user.
    Placeholder function later to be updated with database
    :param full_profile_info: FullUserProfileInfo - User information saved in the database.
    :param user_id: int - user_id if already exists.
    :return: user_id: int - existing or new user id
    """

    global profile_infos
    global user_contents

    if user_id is None:
        user_id = len(profile_infos)
    liked_posts = full_profile_info.liked_posts
    short_description = full_profile_info.short_description
    long_bio = full_profile_info.long_bio

    user_contents[user_id] = {'liked_posts': liked_posts}
    profile_infos[user_id] = {'short_description':  short_description,
                'long_bio': long_bio}

    return user_id


def delete_user(user_id: int) -> None:
    global profile_infos
    global user_contents

    del profile_infos[user_id]
    del user_contents[user_id]

    return None
@app.get("/user/me", response_model=FullUserProfileInfo)
def test_endpoint():
    full_user_profile = get_user_info()

    return full_user_profile


# order maters. If user/me was after then we would get an internal erro
# Path parameter
@app.get("/user/{user_id}", response_model=FullUserProfileInfo)
def get_user_by_id(user_id: int):
    """
    Endpoint for retrieving a FullUserProfileInfo by the user's unique integer id.
    :param user_id: int - unique monotonically increasing integer id
    :return: FullUserProfileInfo
    """

    full_user_profile = get_user_info(user_id)

    return full_user_profile

@app.put("/user/{user_id}")
def update_user(user_id: int, full_profile_info: FullUserProfileInfo):
    create_update_user(full_profile_info, user_id)

    return None

@app.delete("/user/{user_id}")
def remove_user(user_id: int):
    delete_user(user_id)


#query parameters
@app.get("/users", response_model=MultipleUserResponse)
def get_all_users_paginated(start: int = 0, limit: int = 2):
    users,total = get_all_users_with_pagination(start, limit)
    formatted_users = MultipleUserResponse(users=users, total=total)

    return formatted_users

@app.post("/users", response_model=CreateUserResponse)
def add_user(full_profile_info: FullUserProfileInfo):
    user_id =  create_update_user(full_profile_info)
    created_user = CreateUserResponse(user_id=user_id)

    return created_user

