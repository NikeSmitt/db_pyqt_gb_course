from typing import Optional

from db_handler import User, UserHistory, UserContacts
from client_db_handler import UserMessages
from session import SessionLocal, get_session


def get_by_id(model, id: int, current_session):
    """
    Возвращает запись из бд или None
    :param current_session:
    :param model:
    :param id:
    :return:
    """
    with get_session(current_session) as session:
        return session.query(model).filter(model.id == id).first()


def get_user_by_name(name: str, current_session):
    """

    :param name:
    :return:
    """
    with get_session(current_session) as session:
        return session.query(User).filter(User.nickname == name).first()


def get_user_contacts(name: str) -> list:
    with get_session(SessionLocal) as session:
        user = session.query(User).filter(User.nickname == name).first()
        # print(f'{user=}')
        print(f'{user.contacts=}')
        names = [user.user_to_save_name for user in user.contacts]
        print(f'{names=}')
        return names

    # return ['la', 'la']


def add_user(user_name: str, current_session) -> Optional[User]:
    """

    :param user_name:
    :return:
    """
    user = get_user_by_name(user_name, current_session)
    if not user:
        with get_session(current_session) as session:
            new_user = User(user_name)
            session.add(new_user)
            session.commit()
        return new_user
    return user


def add_login_history(user: User):
    with get_session(SessionLocal) as session:
        history = UserHistory(user.id)
        session.add(history)
        session.commit()
        return history


def get_multy(model):
    with get_session(SessionLocal) as session:
        return session.query(model).all()


def add_contact(user_name: str, name_to_save: str) -> bool:
    with get_session(SessionLocal) as session:
        user = get_user_by_name(user_name, SessionLocal)
        user_to_save = get_user_by_name(name_to_save, SessionLocal)
        if not (user and user_to_save):
            print(f'Save contact error <user - {user}, user_to_save - {user_to_save}>')
            return False
        session.add(UserContacts(user.id, user_to_save.nickname))
        session.commit()
        print('Contacts = ', session.query(UserContacts).all())


def delete_contact(user_name: str, name_to_delete: str):
    with get_session(SessionLocal) as session:
        user = get_user_by_name(user_name, SessionLocal)
        name_to_delete = get_user_by_name(name_to_delete, SessionLocal)
        if not (user and name_to_delete):
            print(f'Delete contact error <user - {user}, user_to_save - {name_to_delete}>')
            return False
        session.query(UserContacts).filter(
            UserContacts.user_id == user.id, UserContacts.user_to_save_name == name_to_delete.nickname
        ).delete()
        session.commit()
        print('Contacts = ', session.query(UserContacts).all())


def save_message(user_name: str, message: str, current_session):
    with get_session(current_session) as session:
        user = get_user_by_name(user_name, SessionLocal)
        if not user:
            print(f'Save message error <message - {user}, message - {message}>')
            return False
        session.add(UserMessages(user.id, message))
        session.commit()
        print(session.query(UserMessages).all())
