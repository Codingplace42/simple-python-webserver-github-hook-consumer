# Python Github Hook Consumer
Purpose of this project is an easy handling for CD pipelines.
It's using low level packages of standard-library of Python.


## Requirements
- Python 3.6 and higher


## Run
```
python app/app.py <DIRECTORY_FOR_CD> [-p 5050]
```

- `-p` Port (default 5050)

The server should have ssh-access to Git Repository which is included in CD process.

The script will create a token which will get refreshed per restart of this script.
The token is written into file `.secret`

The Git Hook is able to access the only available endpoint:
```
curl -X POST \
    -H "Authorization: Token {TOKEN}" \
    {HOST}/git-hook
```

This will trigger the execution of pulling new code.
