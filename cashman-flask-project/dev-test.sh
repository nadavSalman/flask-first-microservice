
docker build . -t  attentiazuredevregistry.azurecr.io/devops-docker/cashman:1.0.1 --platform=amd64  --no-cache && docker run --rm -it -p 5000:5000 attentiazuredevregistry.azurecr.io/devops-docker/cashman:1.0.1



# # get expenses
# curl http://localhost:5000/expenses

# # add a new expense
# curl -X POST -H "Content-Type: application/"23json" -d '{
#     "amount": 20,
#     "description": "lottery ticket"
# }' http://cashman.local/expenses

# # get incomes
# curl http://localhost:5000/incomes

# # add a new income
curl -X POST -H "Content-Type: application/json" -d '{
    "amount": 300.0,
    "description": "loan payment"
}' http://localhost:5000/api/expense
