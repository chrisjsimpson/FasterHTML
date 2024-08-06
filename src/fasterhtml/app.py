from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.responses import HTMLResponse
import contextlib

import databases
import sqlalchemy
from starlette.config import Config
from starlette.routing import Route
from typing import Any


from HtmlElements import (
    Page,
    H1,
    P,
    Head,
    Doctype,
    Html,
    Body,
    Div,
    Form,
    Input,
    Button,
)

# Configuration from environment variables or '.env' file.
config = Config(".env")
DATABASE_URL = config("DATABASE_URL")
# DATABASE_URL = "sqlite:///test.db"


class HTMLStringResponse(HTMLResponse):
    def render(self, content: Any) -> bytes:
        # Check if content is an instance of something that can
        # be converted to a string
        if not isinstance(content, (str, bytes)):
            content = str(content)
        return super().render(content)


async def homepage(request):
    page = Page(
        Head(),
        Body(
            Div(
                H1("Contact Us"),
                Form(
                    P("Name:"),
                    Input(type="text", name="name", required=True),
                    P("Email:"),
                    Input(
                        type="email",
                        name="email",
                        required=True,
                        _type="email",  # noqa: E501
                    ),  # noqa: E501
                    Button("Submit", type="submit"),
                    hx_post="/submit-form",  # HTMX attribute for POST request
                    hx_target="#response",  # Target element for the response
                    hx_swap="outerHTML",  # How the response should be swapped
                    id="response",
                ),
                Div("", id="response"),  # Placeholder for the HTMX response
            )
        ),
    )

    return HTMLStringResponse(page)


async def submit_form(request):
    # Process the form data (e.g., save to a database, send an email, etc.)
    # For this example, we'll just create a response message.

    response_content = Div(
        P("Thank you! We have received your email."),
        P("We will be in touch soon."),
    )
    return HTMLStringResponse(response_content)


async def jsonResponse(request):
    return JSONResponse({"hello": "world"})


async def custom_page(request):
    page = (
        str(Doctype())
        + "\n"
        + str(Html(Head(), Body(H1("My Page"), P("My paragraph"))))
    )
    return HTMLResponse(page)


# Database table definitions.
metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)

database = databases.Database(DATABASE_URL)


@contextlib.asynccontextmanager
async def lifespan(app):
    await database.connect()
    yield
    await database.disconnect()


# Main application code.
async def list_notes(request):
    query = notes.select()
    results = await database.fetch_all(query)
    content = [
        {"text": result["text"], "completed": result["completed"]}
        for result in results  # noqa: E501
    ]
    return JSONResponse(content)


async def add_note(request):
    data = await request.json()
    query = notes.insert().values(
        text=data["text"], completed=data["completed"]
    )  # noqa: E501
    await database.execute(query)
    return JSONResponse({"text": data["text"], "completed": data["completed"]})


routes = [
    Route("/", homepage),
    Route("/notes", endpoint=list_notes, methods=["GET"]),
    Route("/notes", endpoint=add_note, methods=["POST"]),
    Route("/custom", custom_page),
    Route("/json", jsonResponse),
    Route("/submit-form", submit_form, methods=["POST"]),
]

app = Starlette(
    debug=True,
    routes=routes,
    lifespan=lifespan,
)
