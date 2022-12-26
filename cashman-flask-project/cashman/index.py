from flask import Flask, jsonify, request ,url_for 

from cashman.model.expense import Expense, ExpenseSchema
from cashman.model.income import Income, IncomeSchema
from cashman.model.transaction_type import TransactionType
import os


# Import bluesprints
from cashman.blueprints.basic_operation_blueprint import create_basic_opeartion_blueprint

app = Flask(__name__)

transactions = [
    Income('Salary', 5000),
    Income('Dividends', 200),
    Expense('pizza', 50),
    Expense('Rock Concert', 100)
]

api_version = "v1.1"


import logging

logging.basicConfig(filename=os.getcwd() + '/app-logs/record.log', level=logging.ERROR)

app = Flask(__name__)

app.register_blueprint(
    create_basic_opeartion_blueprint(
        "BasicIncome",
        TransactionType.INCOME
    ),
    url_prefix='/api'
)

app.register_blueprint(
    create_basic_opeartion_blueprint(
        "BasicExpenses",
        TransactionType.EXPENSE
    ),
    url_prefix='/api'
)

@app.route('/liveness')
def get_api_version():
    return jsonify({'api version': api_version}), 200

@app.route('/')
def get_api_root():
    return jsonify({'Python Flask Micro Service': 'cashman'}), 200

@app.route('/incomes')
def get_incomes():
    schema = IncomeSchema(many=True)
    incomes = schema.dump(
        filter(lambda t: t.type == TransactionType.INCOME, transactions)
    )
    return jsonify(incomes), 200


@app.route('/incomes', methods=['POST'])
def add_income():
    income = IncomeSchema().load(request.get_json())
    transactions.append(income)
    return "", 204


@app.route('/expenses')
def get_expenses():
    schema = ExpenseSchema(many=True)
    expenses = schema.dump(
        filter(lambda t: t.type == TransactionType.EXPENSE, transactions)
    )
    return jsonify(expenses) , 200


@app.route('/expenses', methods=['POST'])
def add_expense():
    expense = ExpenseSchema().load(request.get_json())
    transactions.append(expense)
    return "", 204

@app.route('/error')
def error_endpoint():
    app.logger.info('kuku')
    app.logger.error('An error occurred')
    return "",  401
    

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

@app.route("/site-map")
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    return jsonify(links)


if __name__=="__main__":
    
    app.run("0.0.0.0", port=5000, debug=True)