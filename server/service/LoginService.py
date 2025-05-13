from ..repository import UserRepository
from ..database import db
from ..models import GetUser


class LoginService:
    def __init__(self):
        self.__repository: UserRepository = UserRepository(db.session)

    def login_user(self, email: str, password: str) -> GetUser:
        user = self.__repository.get_user_by_email(email)
        if user:
            check_pass = user.verify_password(password)
            if check_pass:
                user = GetUser.model_validate(user, from_attributes=True)
                return user
        return None