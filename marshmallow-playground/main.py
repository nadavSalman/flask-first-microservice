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
    print('\n'*5)
    print(f'Marshmallow playground')
    user1 = User("Gil","gildev@gmail.com")
    print('Outout __str__ & __repr__')
    print(user1.__str__())
    print(user1.__repr__())

    # Create schema from dictionary :
    UserSchema = Schema.from_dict(
        {"name": fields.Str(), "email": fields.Email(), "created_at": fields.DateTime()}
    )



    # Serializing Objects (“Dumping”)
    print('\nSerializing Objects : \n')
    user = User(name="Monty", email="monty@python.org") # Create a simple User object 
    schema = UserSchema()
    # Serialize objects by passing them to your schema’s dump method, which returns the formatted result.
    result1 = schema.dump(user)
    pprint(result1)

    print('\nFiltering Output : \n')
    summary_schema = UserSchema(only=("name", "email"))
    result2 = summary_schema.dump(user)
    pprint(result2)

    print('\n Exclude Output : \n')
    summary_schema = UserSchema(exclude=("name", "email"))
    result3 = summary_schema.dump(user)
    pprint(result3)
    



    print('\n'*5)



if __name__ == '__main__':
    main()