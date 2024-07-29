import random
from typing import Optional, Union

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models.user_model import UserUpdate, RegisterUserRequest
from app.schemas.users_schema import User


class UserRepository:
    @staticmethod
    def get_user(db: Session, user_id: int) -> Optional[User]:
        try:
            return db.query(User).filter(User.id == user_id).first()
        except SQLAlchemyError as e:
            print(f"Error retrieving user by ID: {e}")
            return None

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        try:
            return db.query(User).filter(User.email == email).first()
        except SQLAlchemyError as e:
            print(f"Error retrieving user by email: {e}")
            return None

    @staticmethod
    def create_user(db: Session, user: RegisterUserRequest) -> Union[User, None]:
        def generate_unique_user_id(db: Session):
            # Fetch all existing user IDs
            existing_ids = set(row[0] for row in db.query(User.id).all())

            while True:
                # Generate a new user ID
                user_id = str(random.randint(1000000000, 9999999999))
                # Check if the new ID is unique
                if user_id not in existing_ids:
                    return user_id
        try:
            db_user = User(
                id=generate_unique_user_id(db),
                email=user.email,
                hashed_password=get_password_hash(user.password)
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Error creating user: {e}")
            return None

    @staticmethod
    def update_user(db: Session, db_user: User, user_update: UserUpdate) -> Union[User, None]:
        try:
            update_data = user_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_user, key, value)
            if user_update.password:
                db_user.hashed_password = get_password_hash(user_update.password)
            db.commit()
            db.refresh(db_user)
            return db_user
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Error updating user: {e}")
            return None

    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        try:
            db_user = db.query(User).get(user_id)
            if db_user:
                db.delete(db_user)
                db.commit()
                return True
            else:
                print(f"User with ID {user_id} not found")
                return False
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Error deleting user: {e}")
            return False


user_repository = UserRepository()
