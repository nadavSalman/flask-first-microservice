import datetime as dt
from marshmallow import Schema, fields
from pprint import pprint


class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.created_at = dt.datetime.now()

    def __repr__(self):
        return "<User(name={self.name!r})>".format(self=self)

    def __str__(self) -> str:
        tab_new_line = "\n\t"
        return f"  User Object:  {tab_new_line}Name:{self.name}  {tab_new_line}email:{self.email} {tab_new_line}created_at:{self.created_at}"

class UserSchema(Schema):
    name = fields.Str()
    email = fields.Email()
    created_at = fields.DateTime()




def main():
    print(f'Marshmallow playground')
    user1 = User("Gil","gildev@gmail.com")
    print('Outout __str__ & __repr__')
    print(user1.__str__())
    print(user1.__repr__())

    # Create schema from dictionary :
    UserSchema = Schema.from_dict(
        {"name": fields.Str(), "email": fields.Email(), "created_at": fields.DateTime()}
    )


    user = User(name="Monty", email="monty@python.org") # Create a simple User object 
    schema = UserSchema()
    result = schema.dump(user)
    pprint(result)



if __name__ == '__main__':
    main()