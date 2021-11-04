## How to execute programs
Server can works alone
```
python3 server.py
```
Client needs some arguments, for example, operation type and table that we want to work with
For instance: we can list every user in the DB
```
python3 client.py -l --user
```
With main.py we can execute multiples clients
```
python3 main.py
```

## User a virtual environment
Crete python virtualEnvironment
```
python3 -m venv enerfi
```
Every time that we can use this repo, we should have enable venv
```
source enerfi/bin/activate
```
Close venv
```
deactivate
```
If it miss some dependencies we can use
```
pip3 install -r utils/requirements.txt
```

## Bash util commands
POST:
```
curl -d '{"user":"tiago", "meter_id":null}' -H "Content-Type: application/json" -X POST http://localhost:500/users
```