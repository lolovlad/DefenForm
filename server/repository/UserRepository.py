from sqlalchemy.orm import Session
from ..database import User, Role, TypeService
from ..models.User import PostUser

from uuid import uuid4


class UserRepository:
    def __init__(self, session: Session):
        self.__session: Session = session

    def get_user(self, id_user: int) -> User | None:
        return self.__session.get(User, id_user)

    def get_user_by_uuid(self, uuid: str) -> User | None:
        return self.__session.query(User).where(User.trace_id == uuid).first()

    def get_user_by_email(self, email: str) -> User | None:
        user = self.__session.query(User).where(User.email == email).first()
        return user

    def get_role_by_name(self, name: str) -> Role | None:
        return self.__session.query(Role).where(Role.name == name).first()

    def get_type_service_by_name(self, name: str) -> TypeService | None:
        return self.__session.query(TypeService).where(TypeService.name == name).first()

    def get_all_type_service(self) -> TypeService | None:
        return self.__session.query(TypeService).all()

    def get_list_by_user(self) -> list[User] | None:
        return self.__session.query(User).join(Role).where(Role.name == "user").all()

    def add(self, user: PostUser) -> User | None:
        user_entity = User(
            trace_id=str(uuid4()),
            name=user.name,
            surname=user.surname,
            patronymics=user.patronymics,
            phone=user.phone,
            email=user.email,
            id_role=user.id_role,
            id_type_service=user.id_type_service

        )
        user_entity.password = user.password

        try:
            self.__session.add(user_entity)
            self.__session.commit()
            return user_entity
        except:
            self.__session.rollback()
            return None

    def update(self, user: User):
        try:
            self.__session.add(user)
            self.__session.commit()
        except:
            self.__session.rollback()
