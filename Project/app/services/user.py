from typing import Optional
from app.schemas.user import (
    FullUserProfileInfo,
    User
)
from app.exceptions import UserNotFound

profile_infos = {
    0: {'short_description': 'Facts about me',
        'long_bio': 'More facts about me'},
}

user_contents = {
    0: {
        'liked_posts': [5] * 2,
    }
}


class UserService:
    def __init__(self):
        pass

    # static method because we are not changing the class or instance

    # not staticmethod because we are using a static method within the class
    async def get_all_users_with_pagination(self, start: int, limit: int) -> (list[FullUserProfileInfo], int):
        list_of_users = []
        keys = profile_infos.keys()
        total = len(keys)
        for i in range(0, len(keys), 1):
            if i < start:
                continue
            current_key = list(keys)[i]
            user = await self.get_user_info(current_key)
            list_of_users.append(user)

            if len(list_of_users) >= limit:
                break

        return list_of_users, total

    @staticmethod
    async def get_user_info(user_id: int = 0) -> FullUserProfileInfo:
        if user_id not in profile_infos:
            raise UserNotFound(user_id)

        profile_info = profile_infos[user_id]
        user_content = user_contents[user_id]

        user = User(**user_content)

        full_user_profile = {**profile_info,
                             **user.dict()}

        profile_info = FullUserProfileInfo(**full_user_profile)

        return profile_info

    @staticmethod # because we are not accessing class properties
    async def create_update_user(full_profile_info: FullUserProfileInfo, user_id: Optional[int]=None) -> int:
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
        profile_infos[user_id] = {'short_description': short_description,
                                  'long_bio': long_bio}

        return user_id

    @staticmethod
    async def delete_user(user_id: int) -> None:
        global profile_infos
        global user_contents

        if user_id not in profile_infos:
            raise UserNotFound(user_id)

        del profile_infos[user_id]
        del user_contents[user_id]

        return None

