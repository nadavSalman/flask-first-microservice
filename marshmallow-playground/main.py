import datetime as dt
from marshmallow import Schema, fields, post_load, ValidationError, validate 
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

class ValidationUserSchema(Schema):
    name = fields.Str(validate=validate.Length(min=1))
    permission = fields.Str(validate=validate.OneOf(["read", "write", "admin"]))
    age = fields.Int(validate=validate.Range(min=18, max=40))

    '''
    In order to deserialize to an object, 
    define a method of your Schema and decorate it with post_load.
     The me 
    '''
    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)

class BandMemberSchema(Schema):
    name = fields.String(required=True)
    email = fields.Email()


def main():
    print('\n'*5)
    print(f'Marshmallow playground')
    user1 = User("Gil","gildev@gmail.com")
    # print('Outout __str__ & __repr__')
    # print(user1.__str__())
    # print(user1.__repr__())

    # Create schema from dictionary :
    UserSchema = Schema.from_dict(
        {"name": fields.Str(), "email": fields.Email(), "created_at": fields.DateTime()}
    )



    # Serializing Objects (“Dumping”)
    print('\nSerializing Objects : \n')
    # Create a simple User object 
    user = User(name="Monty", email="monty@python.org") 
    schema = UserSchema()
    # Serialize objects by passing them to your schema’s dump method, which returns the formatted result.
    result1 = schema.dump(user)
    pprint(result1)

    # print('\nFiltering Output : \n')
    # summary_schema = UserSchema(only=("name", "email"))
    # result2 = summary_schema.dump(user)
    # pprint(result2)

    # print('\n Exclude Output : \n')
    # summary_schema = UserSchema(exclude=("name", "email"))
    # result3 = summary_schema.dump(user)
    # pprint(result3)


    # Deserializing Objects (“Loading”)
    print('\nDeserializing Objects : \n')
    #The reverse of the dump method is load, 
    # which validates and deserializes an input dictionary
    #  to an application-level data structure.
    user_data = {
        "created_at": "2014-08-11T05:26:03.869245",
        "email": "ken@yahoo.com",
        "name": "Ken",
    }
    schema = UserSchema()
    result = schema.load(user_data)
    pprint(result) 

    print('\nDeserializing to Objects\n')
    

    # The  load method return a User instance. 
    user_data = {"name": "Ronnie", "email": "ronnie@stones.com"}
    schema = UserSchema()
    user_obj = schema.load(user_data)
    print(user_obj)

    print('\n Handling Collections of Objects \n')

    user1 = User(name="Mick", email="mick@stones.com")
    user2 = User(name="Keith", email="keith@stones.com")
    users = [user1, user2]
    schema = UserSchema(many=True)
    result = schema.dump(users)  # OR UserSchema().dump(users, many=True)
    pprint(result)


    print('\n Validation \n')
    try:
        result = UserSchema().load({"name": "John", "email": "foo"})
    except ValidationError as err:
        print(err.messages)  # => {"email": ['"foo" is not a valid email address.']}
        print(err.valid_data)


    print('\n validating a collection \n')
    user_data = [
        {"email": "mick@stones.com", "name": "Mick"},
        {"email": "invalid", "name": "Invalid"},  # invalid email
        {"email": "keith@stones.com", "name": 12},
        {"email": "charlie@stones.com",},  # missing "name"
    ]

    try:
        BandMemberSchema(many=True).load(user_data)
    except ValidationError as err:
        pprint(err.messages)


    print('\n perform additional validation for a field  \n')
    in_data = {"name": "", "permission": "invalid", "age": 71}
    try:
        ValidationUserSchema().load(in_data)
    except ValidationError as err:
        pprint(err.messages)

    print('\n implement your own validators \n')
    def validate_quantity(n):
        if n < 0:
            raise ValidationError("Quantity must be greater than 0.")
        if n > 30:
            raise ValidationError("Quantity must not be greater than 30.")
    
    class ItemSchema(Schema):
        quantity = fields.Integer(validate=validate_quantity)

    in_data = {"quantity": 31}
    try:
        result = ItemSchema().load(in_data)
    except ValidationError as err:
        print(err.messages) 

    # Validation occurs on deserialization but not on serialization(the load method). 
    print('\n'*5)



if __name__ == '__main__':
    main()