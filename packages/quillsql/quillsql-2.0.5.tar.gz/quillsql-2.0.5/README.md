# Quill Python SDK
[![Unit Tests](https://github.com/quill-sql/quill-python/actions/workflows/ci.yaml/badge.svg)](https://github.com/quill-sql/quill-python/actions/workflows/ci.yaml)
[![Deployments](https://github.com/quill-sql/quill-python/actions/workflows/deploy_prod.yaml/badge.svg)](https://github.com/quill-sql/quill-python/actions/workflows/deploy_prod.yaml)

## Quickstart

First, install the quillsql package by running:

```bash
$ pip install quillsql
```

Then, add a `/quill` endpoint to your existing python server. For example, if
you were running a FASTAPI app, you would just add the endpoint like this:

```python
from quillsql import Quill
from fastapi import FastAPI, Request

app = FastAPI()

quill = Quill(
    private_key=<YOUR_PRIVATE_KEY_HERE>,
    database_connection_string=<YOUR_DB_CONNECTION_STRING_HERE>,
)

# ... your existing endpoints here ...

@app.post("/quill")
async def quill_post(data: Request):
    body = await data.json()
    return quill.query(org_id="2", data=body)
```

Then you can run your app like normally. Pass in this route to our react library
on the frontend and you all set!


## Questions
If you have any questions, please reach out to us!
