from dataclasses import dataclass, field
from typing import List, Union, Any


@dataclass
class HTMLElement:
    tag: str
    content: List[Union["HTMLElement", str]] = field(default_factory=list)
    attributes: dict = field(default_factory=dict)

    self_closing_tags = {
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    }

    htmx_attributes = [
        "hx_get",
        "hx_post",
        "hx_put",
        "hx_delete",
        "hx_patch",
        "hx_trigger",
        "hx_target",
        "hx_swap",
        "hx_include",
        "hx_select",
        "hx_indicator",
        "hx_push_url",
        "hx_confirm",
        "hx_disable",
        "hx_replace_url",
        "hx_on",
    ]

    def __init__(self, tag: str, content=None, cls=None, _type=None, **attributes):
        self.tag = tag
        self.content = content or []
        self.attributes = {}

        if cls:
            self.attributes["class"] = cls

        if _type:
            self.attributes["type"] = _type

        # Extract and store HTMX attributes if provided
        for attr in self.htmx_attributes:
            if attr in attributes:
                self.attributes[attr.replace("_", "-")] = attributes.pop(attr)

        # Store other attributes
        self.attributes.update(attributes)

    def render_attributes(self):
        attrs = []
        for key, value in self.attributes.items():
            if value is True:
                attrs.append(f"{key}")
            else:
                attrs.append(f'{key}="{value}"')
        return " ".join(attrs)

    def render_content(self):
        return "\n".join(str(item) for item in self.content)

    def __str__(self):
        attrs = self.render_attributes()
        open_tag = f"<{self.tag} {attrs}".strip() + ">"
        if self.tag.lower() == "doctype":
            return "<!DOCTYPE html>"
        if self.tag in self.self_closing_tags:
            return open_tag[:-1] + " />"
        close_tag = f"</{self.tag}>"
        inner_html = self.render_content()
        return (
            f"{open_tag}\n{inner_html}\n{close_tag}"
            if inner_html
            else f"{open_tag}{close_tag}"
        )

    def __add__(self, other):
        return str(self) + str(other)


# Helper element for creating a full HTML page structure
class Page:
    def __init__(self, *body_content, include_pico_css=True, include_htmx=True):
        head_content = [
            Meta(charset="utf-8"),
            Meta(name="viewport", width="device-width", initial_scale="1"),
            Meta(name="color-scheme"),
        ]
        if include_pico_css:
            head_content.append(
                Link(
                    rel="stylesheet",
                    href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css",
                )
            )

        if include_htmx:
            head_content.append(
                Script(src="https://unpkg.com/htmx.org@2.0.1", defer=True)
            )

        self.doctype = Doctype()
        self.html = Html(
            Head(*head_content), Body(Main(cls="container", _type="", *body_content))
        )

    def __str__(self):
        return f"{self.doctype}\n{self.html}"

    def __repr__(self):
        return self.__str__()


# Dynamically create classes for each HTML element
def create_html_element_class(tag):
    @dataclass
    class SpecificHTMLElement(HTMLElement):
        def __init__(self, *content, cls=None, _type=None, **attributes):
            super().__init__(
                tag=tag, content=list(content), cls=cls, _type=_type, **attributes
            )

    SpecificHTMLElement.__name__ = (
        tag.capitalize()
    )  # Set the class name for easy imports
    return SpecificHTMLElement


# List of common HTML tags (extendable to any tag)
html_tags = [
    "a",
    "abbr",
    "address",
    "area",
    "article",
    "aside",
    "audio",
    "b",
    "base",
    "bdi",
    "bdo",
    "blockquote",
    "body",
    "br",
    "button",
    "canvas",
    "caption",
    "cite",
    "code",
    "col",
    "colgroup",
    "data",
    "datalist",
    "dd",
    "del",
    "details",
    "dfn",
    "dialog",
    "div",
    "dl",
    "dt",
    "em",
    "embed",
    "fieldset",
    "figcaption",
    "figure",
    "footer",
    "form",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "head",
    "header",
    "hgroup",
    "hr",
    "html",
    "i",
    "iframe",
    "img",
    "input",
    "ins",
    "kbd",
    "label",
    "legend",
    "li",
    "link",
    "main",
    "map",
    "mark",
    "meta",
    "meter",
    "nav",
    "noscript",
    "object",
    "ol",
    "optgroup",
    "option",
    "output",
    "p",
    "param",
    "picture",
    "pre",
    "progress",
    "q",
    "rp",
    "rt",
    "ruby",
    "s",
    "samp",
    "script",
    "section",
    "select",
    "small",
    "source",
    "span",
    "strong",
    "style",
    "sub",
    "summary",
    "sup",
    "table",
    "tbody",
    "td",
    "template",
    "textarea",
    "tfoot",
    "th",
    "thead",
    "time",
    "title",
    "tr",
    "track",
    "u",
    "ul",
    "var",
    "video",
    "wbr",
    "doctype",
]

# Create classes for each HTML tag and add them to the module's namespace
globals().update(
    {tag.capitalize(): create_html_element_class(tag) for tag in html_tags}
)
globals().update({"Page": Page})
