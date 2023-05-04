from pydantic import BaseModel, Field
from typing import Optional



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