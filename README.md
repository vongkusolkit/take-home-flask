# Fetch Rewards Backend Software Engineering

This web service accepts HTTP requests and returns responses where the following routes are defined:
- `'/transaction'` - Add transactions for a specific payer and date.
- `'/points'` - Spend points using the rules above and return a list of { "payer": <string>, "points": <integer> } for each call.
- `'/balances'` - Return all payer point balances.

## Getting started
To get started, install the necessary packages:
```
pip3 install -r requirements.txt
```

To load the Flask application, run:
```
export FLASK_APP=main.py   
flask run
```

## REST API
### Add transaction endpoint POST request
```
curl --location --request POST 'http://127.0.0.1:5000/transaction' \
--header 'Content-Type: application/json' \
--data-raw '{ "payer": "DANNON", "points": 300, "timestamp": "2022-10-31T10:00:00Z" }'
```
Expected response: `{"success":"Successfully added transaction"}`


### Spend points endpoint POST request
```
curl --location --request POST 'http://127.0.0.1:5000/points' \
--header 'Content-Type: application/json' \
--data-raw '{ "points": 100 }'
```
Expected response: `[{"payer":"DANNON","points":-100}]`


### Return all payer point balances GET request
```
curl --location --request GET 'http://127.0.0.1:5000/balances' \
--data-raw ''
```
Expected response: `{"DANNON":100}`

## Test
To run test cases:
```
pytest -v test.py   
```
