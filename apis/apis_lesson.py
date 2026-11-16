"""
Building APIs Lesson: How to build (and call) web APIs for data.

Run this file to print the lesson:  python apis_lesson.py
"""

LESSON = """
=====================================================================
1. WHAT IS AN API?
=====================================================================
An API (Application Programming Interface) is a way for one program
to ask another program for data or to do something.

A web API works over HTTP, the same thing your browser uses. A
program sends a REQUEST to a URL and gets back a RESPONSE, usually
in JSON.

Think of a restaurant. You (the client) do not walk into the kitchen.
You give your order to the waiter (the API), who brings back your
food (the data). The menu lists what you are allowed to order.

Why data engineers care:
  - Many sources only share data through APIs (Stripe, Salesforce,
    weather services). You must call them well.
  - You may need to SERVE data to other teams or apps: "give me
    this customer's latest score".
  - Internal tools (trigger a pipeline, check a job) are often APIs.

=====================================================================
2. KEY WORDS
=====================================================================
CLIENT      The program making the request.
SERVER      The program answering it.
ENDPOINT    One URL the API offers, e.g. /customers/42.
METHOD      The type of action (GET, POST, PUT, PATCH, DELETE).
STATUS CODE A number saying how it went (200 OK, 404 Not Found).
HEADER      Extra info sent with a request or response (e.g. auth).
BODY        The data sent with a request or response (often JSON).
QUERY PARAM Options added to the URL:  /orders?status=paid&limit=50
PATH PARAM  A value inside the URL path:  /customers/{customer_id}
REST        The most common style of web API: resources (nouns) in
            URLs, actions given by HTTP methods.
JSON        JavaScript Object Notation. The usual data format.

=====================================================================
3. HTTP METHODS: THE VERBS
=====================================================================
GET      Read data. Must not change anything.
POST     Create something new.
PUT      Replace something completely.
PATCH    Change part of something.
DELETE   Remove something.

Good REST URLs use nouns, and the method says the action:

    GET    /customers          list customers
    GET    /customers/42       get one customer
    POST   /customers          create a customer
    PATCH  /customers/42       update some fields
    DELETE /customers/42       delete a customer

Avoid verbs in URLs like /getCustomer or /deleteCustomer.

IDEMPOTENT means doing it twice has the same effect as doing it
once. GET, PUT and DELETE are idempotent. POST is not (two POSTs
can create two records). This matters when clients retry.

=====================================================================
4. STATUS CODES
=====================================================================
The first digit tells you the group:

  2xx  Success      200 OK, 201 Created, 204 No Content
  3xx  Redirect     301 Moved Permanently
  4xx  Client error (the caller did something wrong)
         400 Bad Request     bad input
         401 Unauthorized    not logged in / no valid key
         403 Forbidden       logged in, but not allowed
         404 Not Found       no such thing
         422 Unprocessable   input failed validation
         429 Too Many Requests  slow down (rate limited)
  5xx  Server error (the server broke)
         500 Internal Server Error
         503 Service Unavailable

Rule of thumb: retry 429 and 5xx (with a wait). Do not retry other
4xx errors. They will fail again until the request is fixed.

=====================================================================
5. INSTALL
=====================================================================
We use FastAPI, a popular, modern Python framework. It checks input
for you and writes docs automatically.

    pip install "fastapi[standard]"

Check it works:

    fastapi --version

(Other options: Flask is older and simpler; Django REST Framework is
bigger and suits large apps.)

=====================================================================
6. YOUR FIRST API
=====================================================================
Save as main.py:

    from fastapi import FastAPI, HTTPException

    app = FastAPI()

    CUSTOMERS = {
        1: {"id": 1, "name": "Alice", "city": "Leeds"},
        2: {"id": 2, "name": "Bob", "city": "London"},
    }

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.get("/customers/{customer_id}")
    def get_customer(customer_id: int):
        if customer_id not in CUSTOMERS:
            raise HTTPException(status_code=404, detail="Not found")
        return CUSTOMERS[customer_id]

Run it:

    fastapi dev main.py

Try it:
    http://127.0.0.1:8000/customers/1      -> Alice as JSON
    http://127.0.0.1:8000/customers/99     -> 404
    http://127.0.0.1:8000/customers/abc    -> 422 (not an int)
    http://127.0.0.1:8000/docs             -> free interactive docs

The type hint `customer_id: int` makes FastAPI check the input. The
docs page comes from the OpenAPI standard, which FastAPI writes for
you.

=====================================================================
7. ACCEPTING DATA WITH PYDANTIC MODELS
=====================================================================
Describe the shape of the data with a Pydantic model. FastAPI then
rejects bad input with a 422 before your code runs.

    from pydantic import BaseModel, Field

    class CustomerIn(BaseModel):
        name: str = Field(min_length=1)
        city: str
        age: int = Field(ge=0, le=120)

    @app.post("/customers", status_code=201)
    def create_customer(customer: CustomerIn):
        new_id = max(CUSTOMERS) + 1
        CUSTOMERS[new_id] = {"id": new_id, **customer.model_dump()}
        return CUSTOMERS[new_id]

Send {"name": "Cara", "city": "York", "age": -3} and you get a 422
with a clear message. No hand-written checks needed.

=====================================================================
8. PAGINATION AND FILTERING
=====================================================================
Never return a whole table in one response. Return pages.

    @app.get("/orders")
    def list_orders(status: str | None = None,
                    limit: int = 50, offset: int = 0):
        rows = ORDERS
        if status:
            rows = [r for r in rows if r["status"] == status]
        return {"items": rows[offset:offset + limit],
                "total": len(rows)}

    GET /orders?status=paid&limit=50&offset=100

Two common styles:
  OFFSET  ?limit=50&offset=100. Simple, but slow and can skip or
          repeat rows if data changes between calls.
  CURSOR  ?after=<last_id>. The server returns a "next" cursor.
          Fast and stable for big or changing data. Preferred.

Cap the limit (e.g. at most 1000) so one call cannot overload you.

=====================================================================
9. SECURITY AND GOOD MANNERS
=====================================================================
AUTHENTICATION  Who are you? Usually an API key or a token (OAuth2 /
                JWT) sent in a header:
                    Authorization: Bearer <token>
AUTHORISATION   What are you allowed to do? Check it on every call.
HTTPS           Always. Never send keys over plain http.
RATE LIMITING   Limit calls per client (e.g. 100 per minute). Reply
                429 when exceeded.
VERSIONING      Put a version in the URL (/v1/customers) so you can
                change things later without breaking old clients.
VALIDATION      Never trust input. Use Pydantic models and
                parameterised SQL (never build SQL with f-strings).

Keys live in environment variables or a secrets manager, never in
code (see data_governance).

=====================================================================
10. SERVING DATA FROM A DATABASE
=====================================================================
A real API reads from a database or warehouse table:

    import os
    import psycopg

    DB_URL = os.environ["DATABASE_URL"]

    @app.get("/v1/customers/{customer_id}/score")
    def customer_score(customer_id: int):
        with psycopg.connect(DB_URL) as conn:
            row = conn.execute(
                "select score from marts.customer_scores "
                "where customer_id = %s",          # parameterised
                (customer_id,),
            ).fetchone()
        if row is None:
            raise HTTPException(404, "Not found")
        return {"customer_id": customer_id, "score": row[0]}

Tips:
  - Serve from small, pre-computed tables (a gold/mart table), not
    by running heavy queries on every call.
  - Add an index on the column you look up by.
  - Cache answers that do not change often.

=====================================================================
11. TESTING YOUR API
=====================================================================
FastAPI has a test client that works with pytest (see
unit_testing). No server needs to be running.

    from fastapi.testclient import TestClient
    from main import app

    client = TestClient(app)

    def test_get_customer():
        r = client.get("/customers/1")
        assert r.status_code == 200
        assert r.json()["name"] == "Alice"

    def test_missing_customer():
        assert client.get("/customers/99").status_code == 404

=====================================================================
12. THE OTHER SIDE: CALLING APIs IN A PIPELINE
=====================================================================
When you EXTRACT from someone else's API, be a good client:

    import time
    import requests

    def fetch_all(url, token):
        headers = {"Authorization": f"Bearer {token}"}
        params = {"limit": 100}
        while url:
            for attempt in range(5):
                r = requests.get(url, headers=headers,
                                 params=params, timeout=30)
                if r.status_code in (429, 500, 502, 503):
                    time.sleep(2 ** attempt)     # exponential backoff
                    continue
                r.raise_for_status()             # fail on other errors
                break
            else:
                raise RuntimeError("Too many retries")
            data = r.json()
            yield from data["items"]
            url = data.get("next")               # cursor pagination
            params = None                        # "next" has them

Habits:
  - Always set a timeout.
  - Retry 429 and 5xx with exponential backoff. Respect the
    Retry-After header if given.
  - Follow pagination until there is no "next" page.
  - Save the raw JSON first (bronze layer), then transform.
  - Only fetch what changed since last run (e.g. ?updated_since=).

=====================================================================
13. GOOD HABITS
=====================================================================
  - Nouns in URLs, HTTP methods for actions.
  - Return the right status codes, with clear error messages.
  - Validate all input with models.
  - Paginate list endpoints and cap the page size.
  - Version your API from day one (/v1/).
  - Use HTTPS, auth, and rate limits.
  - Add a /health endpoint for monitoring and Kubernetes probes.
  - Write tests with TestClient, and run them in CI/CD.
  - Ship it in a Docker image (see docker).

=====================================================================
14. PRACTICE EXERCISE
=====================================================================
  1. Install FastAPI and run the API from section 6.
  2. Open /docs and call each endpoint from the browser.
  3. Add the POST endpoint from section 7. Send bad data and read
     the 422 error.
  4. Add a paginated /orders endpoint with a status filter.
  5. Require an API key in a header, read from an environment
     variable. Return 401 if it is missing or wrong.
  6. Write 4 pytest tests using TestClient.
  7. Write a small client with requests that pages through
     /orders and saves the results to a JSON file.
  8. Bonus: put the API in a Docker image and run it.

Next steps: serve a dbt mart table through your API, and deploy it
with CI/CD.
"""


def main():
    print(LESSON)


if __name__ == "__main__":
    main()
