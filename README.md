# FasterHTML KISS

tldr: The interesting stuff is in `HtmlElements.py`
Example usage in: `app.py`

I want:

- Migrations (database)
- ASGI (because web sockets)
- openapi automatic generation
- htmx as python
  - and by virute of that, only write webpages in python rather than html templates
  - yet still have the *option* to render template
  - yet still have the *option* to return openapi spec
- *NOT* create a whole new fraemwork for that.
- Easy deployment


Inspect fastHTML and extract the *essence* of python types for html
elements and run with that.

Don't want this to be starlette-only because why should it be? Should also drop into Flask easily or any python web framework.


- Inspired by FastHTML, see https://blog.karmacomputing.co.uk/fasthtml-getting-started-comparison-with-flask/
- Needs [minimalCD](https://github.com/KarmaComputing/minimalcd)
