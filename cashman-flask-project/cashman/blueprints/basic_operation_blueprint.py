from flask import Blueprint, jsonify, request, abort



from cashman.model.expense import Expense, ExpenseSchema
from cashman.model.income import Income, IncomeSchema
from cashman.model.transaction_type import TransactionType


transactions_db = [
    Income('Salary', 5000),
    Income('Dividends', 200),
    Expense('pizza', 50),
    Expense('Rock Concert', 100)
]



schema_dic = { TransactionType.EXPENSE.value.lower(): ExpenseSchema(many=True),
               TransactionType.INCOME.value.lower(): IncomeSchema(many=True) }






def create_basic_opeartion_blueprint(blueprint_name: str, transaction_type: TransactionType) -> Blueprint:
    blueprint = Blueprint(blueprint_name, __name__)

    @blueprint.route(f'/{transaction_type.value.lower()}', methods=["POST"])
    def create_resource():

        if transaction_type.value.lower() == 'income':
            income = IncomeSchema().load(request.get_json())
            transactions_db.append(income)
            print(f'{IncomeSchema().dump(income)}\n transactions_db {transactions_db}')
            return jsonify(IncomeSchema().dump(income)), 204
        elif transaction_type.value.lower() == 'expense': 
            expense = ExpenseSchema().load(request.get_json())
            transactions_db.append(expense)
            print(f'{ExpenseSchema().dump(expense)}\n transactions_db {transactions_db}')
            return jsonify(ExpenseSchema().dump(expense)), 204
        # schema = schema_dic[transaction_type.value.lower()]
        # new_object = schema.load(request.get_json())
        # transactions_db.append(new_object)
        # return jsonify({"Added Object",new_object}), 204
    
    @blueprint.route(f'/{transaction_type.value.lower()}', methods=["GET"])
    def get_resources():
        schema = schema_dic[transaction_type.value.lower()]
        operaions = schema.dump(
            filter(lambda t: t.type == transaction_type, transactions_db)
        )
        return jsonify(operaions), 200


    return blueprint