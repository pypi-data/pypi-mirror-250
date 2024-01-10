import requests
import psycopg2
import psycopg2.extras
import json
import redis

from psycopg2.extensions import make_dsn

## The host url of the Quill metadata server
HOST = "https://quill-344421.uc.r.appspot.com"  # or "http://localhost:8080"
# HOST = "http://localhost:8080"


## The TTL for new cache entries (default: 1h)
DEFAULT_CACHE_TTL = 24 * 60 * 60


# A connection pool with a cache in front.
class CachedPool:
    def __init__(self, config, cache_config, psycopg2_connection=None):
        if psycopg2_connection:
            self.pool = psycopg2_connection
        else:
            self.pool = psycopg2.connect(config)
        self.cache = self.get_cache(cache_config)
        self.ttl = cache_config and cache_config.get("ttl") or DEFAULT_CACHE_TTL
        self.cur = self.pool.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        self.orgId = None

    def get_cache(self, cache_config):
        cache_type = cache_config and cache_config.get("cache_type")
        if cache_type and cache_type == "redis" or cache_type == "rediss":
            return redis.Redis(
                host=cache_config.get("host", "localhost"),
                port=cache_config.get("port", 6379),
                username=cache_config.get("username", "default"),
                password=cache_config.get("password"),
            )
        return None

    def cursor(self):
        return self.cur

    def exec(self, sql):
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        return [json.loads(json.dumps(row, default=str)) for row in rows]

    def query(self, sql):
        if not self.cache:
            return self.exec(sql)

        key = f"{self.orgId}:{self.sql}"
        cached_result = self.cache.get(key)
        if cached_result:
            return json.loads(cached_result)
        else:
            new_result = self.exec(sql)
            new_result_string = json.dumps(new_result)
            self.cache.set(key, new_result_string, "EX", DEFAULT_CACHE_TTL)
            return new_result


## handles a query task
def handleQueryTask(org_id, metadata, private_key, target_pool):
    query = metadata["query"]

    url = f"{HOST}/validate"
    headers = {"Authorization": f"Bearer {private_key}"}
    data = {
        "query": query,
        "orgId": org_id,
        "clientId": metadata.get("clientId"),
        "filters": [],
    }

    response = requests.post(url, json=data, headers=headers)
    response_data = response.json()

    field_to_remove = response_data.get("fieldToRemove")

    cursor = target_pool.cursor()
    query_result = target_pool.query((response_data["query"]))
    names = [desc[0] for desc in cursor.description]
    fields = [
        {"name": desc[0], "dataTypeID": desc[1]}
        for desc in cursor.description
        if desc[0] != field_to_remove
    ]

    formatted_result = {
        "fields": fields,
        "rows": [dict(row) for row in query_result],
    }

    for row in formatted_result["rows"]:
        row = {key: value for key, value in row.items() if key != field_to_remove}
        if field_to_remove in row:
            del row[field_to_remove]

    formatted_result["rows"] = [
        {key: value for key, value in row.items() if key != field_to_remove}
        for row in formatted_result["rows"]
    ]

    return formatted_result


## handle config task
def handleConfigTask(org_id, metadata, private_key, target_pool):
    response = requests.get(
        f"{HOST}/config",
        params={
            "orgId": org_id,
            "name": metadata.get("name"),
            "clientId": metadata.get("clientId"),
        },
        headers={"Authorization": f"Bearer {private_key}"},
    )
    dash_config = response.json()
    if dash_config and dash_config["filters"]:
        for i, filter in enumerate(dash_config["filters"]):
            # run query
            rows = target_pool.query(filter["query"])

            # Update the options for each filter with the rows
            dash_config["filters"][i]["options"] = rows

    if not dash_config:
        dash_config["filters"] = []

    # TODO: MOVE TO DATABASE LEVEL
    # dash_config["dateFilter"]["comparison"] = True
    return dash_config


## handles a create task
def handleCreateTask(org_id, metadata, private_key, target_pool):
    headers = {"Authorization": f"Bearer {private_key}"}
    response = requests.post(
        f"{HOST}/item",
        json=metadata,
        params={
            "orgId": org_id,
            "query": metadata.get("query"),
            "clientId": metadata.get("clientId"),
        },
        headers=headers,
    ).json()

    return response


## handles item task
def handleItemTask(org_id, metadata, private_key, target_pool):
    resp = requests.get(
        f"{HOST}/selfhostitem",
        params={
            "id": metadata.get("id"),
            "orgId": org_id,
            "clientId": metadata.get("clientId"),
        },
        headers={"Authorization": f"Bearer {private_key}"},
    )
    if not resp.ok:
        return {"error": resp.status_code, "errorMessage": resp.text}

    resp_data = resp.json()
    data_to_send = {
        "query": resp_data["queryString"],
        "orgId": org_id,
        "filters": metadata.get("filters"),
        "dashboardItemId": metadata.get("id"),
        "clientId": metadata.get("clientId"),
    }

    response = requests.post(
        f"{HOST}/validate",
        json=data_to_send,
        headers={"Authorization": f"Bearer {private_key}"},
    )
    response_data = response.json()

    field_to_remove = (
        response_data["fieldToRemove"] if response_data["fieldToRemove"] else None
    )
    compare_rows_result = None
    compare_rows = None

    cursor = target_pool.cursor()

    query_result = target_pool.query(response_data["query"])
    rows = [dict(row) for row in query_result]
    fields = [
        {"name": desc[0], "dataTypeID": desc[1]}
        for desc in cursor.description
        if desc[0] != field_to_remove
    ]

    for row in rows:
        if field_to_remove in row:
            del row[field_to_remove]

    compare_rows = None
    if "compareQuery" in response_data:
        compare_rows_result = target_pool.query(response_data["compareQuery"])
        compare_rows = [dict(row) for row in compare_rows_result]
        for row in compare_rows:
            row = {key: value for key, value in row.items() if key != field_to_remove}
            if field_to_remove in row:
                del row[field_to_remove]

    return {
        **resp_data,
        "fields": fields,
        "rows": rows,
        **({"comparisonRows": compare_rows} if compare_rows else {}),
    }


## handles org tasks
def handleOrgsTask(org_id, metadata, private_key, target_pool):
    client_id = metadata.get("clientId", None)
    if not client_id:
        return {"error": 400, "errorMessage": "Missing clientId."}
    headers = {"Authorization": f"Bearer {private_key}"}
    response = requests.get(f"{HOST}/orgsquery/{client_id}", headers=headers).json()
    query = response.get("query", None)
    query_result = target_pool.query(query)
    return {"orgs": [dict(row) for row in query_result]}


## handles view tasks
def handleViewTask(org_id, metadata, private_key, target_pool):
    query = metadata.get("query", None)
    client_id = metadata.get("clientId", None)
    name = metadata.get("name", None)
    id = metadata.get("id", None)
    deleted = metadata.get("deleted", None)
    if not query:
        return {"error": "400", "errorMessage": "Missing query."}
    elif not client_id:
        return {"error": "400", "errorMessage": "Missing clientId."}

    if not deleted:
        target_pool.query(query)
        types_query = target_pool.query(
            "select typname, oid, typarray from pg_type order by oid;"
        )

    cursor = target_pool.cursor()
    table_post = None
    if id and deleted:
        table_post = {"id": id, "deleted": deleted, "clientId": client_id}
    elif id:
        fields = [
            {"name": desc[0], "dataTypeID": desc[1]}
            for desc in cursor.description
        ]
        table_post = {
            "id": id,
            "name": name,
            "clientId": client_id,
            "isVisible": True,
            "viewQuery": query,
            "columns": [
                {
                    "fieldType": next(
                        (
                            dict(type)["typname"]
                            for type in types_query
                            if field["dataTypeID"] == dict(type)["oid"]
                        ),
                        None,
                    ),
                    "name": field["name"],
                    "displayName": field["name"],
                    "isVisible": True,
                }
                for field in fields
            ],
        }
    else:
        fields = [
            {"name": desc[0], "dataTypeID": desc[1]}
            for desc in cursor.description
            if desc[0]
        ]
        table_post = {
            "name": name,
            "clientId": client_id,
            "isVisible": True,
            "viewQuery": query,
            "columns": [
                {
                    "fieldType": next(
                        (
                            dict(type)["typname"]
                            for type in types_query
                            if field["dataTypeID"] == dict(type)["oid"]
                        ),
                        None,
                    ),
                    "name": field["name"],
                    "displayName": field["name"],
                    "isVisible": True,
                }
                for field in fields
            ],
        }

    return requests.post(
        f"{HOST}/createtable",
        json=table_post,
        headers={"Authorization": f"Bearer {private_key}"},
    ).json()


## handle delete tasks
def handleDeleteTask(org_id, metadata, private_key, target_pool):
    headers = {"Authorization": f"Bearer {private_key}"}
    response = requests.post(
        f"{HOST}/selfhostdelete",
        json={
            "clientId": metadata.get("clientId"),
            "id": metadata.get("id"),
        },
        headers=headers,
    )
    return response.json()


## Quill - Fullstack API Platform for Dashboards and Reporting.
class Quill:
    def __init__(
        self,
        private_key,
        database_connection_string="",
        psycopg2_connection=None,
        cache=None,
    ):
        # Handles both dsn-style connection strings (eg. "dbname=test password=secret" )
        # as well as url-style connection strings (eg. "postgres://foo@db.com")
        to_dsn = lambda conn: make_dsn(conn) if "://" in conn else conn
        self.database_connection_string = to_dsn(database_connection_string)
        self.main_pool = CachedPool(
            database_connection_string, cache, psycopg2_connection
        )
        self.private_key = private_key

    def query(self, org_id, data):
        metadata = data.get("metadata")
        if not metadata:
            return {"error": "400", "errorMessage": "Missing metadata."}

        task = metadata.get("task")
        if not task:
            return {"error": "400", "errorMessage": "Missing task."}

        HANDLERS = {
            "query": handleQueryTask,
            "config": handleConfigTask,
            "create": handleCreateTask,
            "item": handleItemTask,
            "orgs": handleOrgsTask,
            "view": handleViewTask,
            "delete": handleDeleteTask,
        }

        try:
            if task in HANDLERS.keys():
                ctx = {
                    "org_id": org_id,
                    "metadata": metadata,
                    "private_key": self.private_key,
                    "target_pool": self.main_pool,
                }
                return HANDLERS[task](**ctx)
            else:
                return {"error": 400, "errorMessage": "unknown task"}
        except Exception as err:
            # print(err, err.__traceback__)
            return {"error": str(err), "errorMessage": str(err) if err else ""}
