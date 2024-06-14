from flask_login import UserMixin


class UserLogin(UserMixin):

    def from_db(self, user_id, db):
        try:
            self.__user = db.query.filter_by(id_=user_id)
        except Exception as error:
            print(f'ХУЕТА {error}')

        return self

    def get_id(self):
        return str(self.__user.id_)

    def create(self, user):
        self.__user = user
        return self

    @staticmethod
    def get_user_by_email(email, db):
        user = False
        try:
            user = db.query.filter_by(email=email).first()
        except Exception as error:
            print(f'ошибочка в get_user_by_email {error}')

        return user
