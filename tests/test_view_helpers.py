"""The shape `views.py` was split out to get, pinned (see its docstring).

`routes_pages.py` used to define the `pages` blueprint, hold the helpers
its five siblings import, and implement the timeline/story/book/export
pages. That third job made the first two a cycle: every sibling imported
the module that imported them, so the routes were registered by a
side-effect import at the bottom of `routes_pages.py` and `routes_api.py`
had to reach for `viewer_scope` from inside a function body to stay clear
of it.

None of that is visible at runtime, which is exactly why it needs tests —
the app worked fine with the cycle, and it will work fine the day somebody
reintroduces it.
"""

import ast
from pathlib import Path

import pytest

APP = Path(__file__).resolve().parent.parent / "app"

#: Every file that registers routes onto the one `pages` blueprint.
PAGE_ROUTE_FILES = (
    "routes_pages.py", "routes_people.py", "routes_accounts.py",
    "routes_groups.py", "routes_settings.py", "routes_themes.py",
)


def _imports(filename):
    """The app modules `filename` imports, at any depth — a function-body
    import is exactly the kind this file is watching for."""
    tree = ast.parse((APP / filename).read_text())
    found = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.level == 1:
            if node.module:
                found.add(node.module)
            found.update(a.name for a in node.names)
    return found


def test_nothing_imports_routes_pages():
    """The point of the split. `routes_pages` is now one route file among
    six, and a file that implements pages should be importable by nobody —
    the moment something needs a helper out of it, that helper belongs in
    `views.py` instead."""
    # `__init__.py` is the exception and the whole point of it: create_app
    # imports all six route files for their registration side effect, which
    # is where that import belongs now.
    offenders = [
        p.name for p in sorted(APP.glob("*.py"))
        if p.name not in ("routes_pages.py", "__init__.py")
        and "routes_pages" in _imports(p.name)
    ]
    assert not offenders, (
        f"{offenders} import routes_pages — put the shared helper in "
        "views.py, which imports no route file and so cannot cycle"
    )


def test_views_imports_no_route_file():
    """The other half of the same rule: `views.py` is what everything
    leans on, so it has to lean on nothing that leans back."""
    leaning_back = sorted(m for m in _imports("views.py") if m.startswith("routes_"))
    assert not leaning_back, (
        f"views.py imports {leaning_back}, which imports views.py — that is "
        "the cycle the split removed"
    )


@pytest.mark.parametrize("filename", PAGE_ROUTE_FILES)
def test_every_page_route_file_registers_onto_the_shared_blueprint(filename):
    """One blueprint named `pages`, so `url_for("pages.xxx")` never has to
    know which of the six files a route's code sits in."""
    source = (APP / filename).read_text()
    assert "from .views import" in source and "bp" in source
    assert "Blueprint(" not in source, (
        f"{filename} declares its own blueprint — every page route "
        "registers onto views.bp, or url_for's endpoint names change"
    )


def test_the_blueprint_is_defined_exactly_once():
    assert 'bp = Blueprint("pages"' in (APP / "views.py").read_text()
    others = [
        p.name for p in sorted(APP.glob("routes_*.py"))
        if 'Blueprint("pages"' in p.read_text()
    ]
    assert others == []


def test_create_app_imports_every_page_route_file():
    """The registration side-effect imports moved out of the bottom of
    `routes_pages.py` and into `create_app`. If one is dropped, its routes
    simply stop existing — a 404 nothing else would explain."""
    source = (APP / "__init__.py").read_text()
    missing = [f for f in PAGE_ROUTE_FILES if f[:-3] not in source]
    assert not missing, (
        f"create_app never imports {missing}, so their routes are not "
        "registered at all"
    )


def test_every_page_endpoint_is_reachable(app):
    """The end that actually matters: after the split, the same URLs answer.

    Named endpoints rather than a count, so a route quietly lost to a
    dropped import is named in the failure instead of showing up as an
    off-by-one.
    """
    endpoints = {r.endpoint for r in app.url_map.iter_rules()}
    for endpoint in (
        "pages.timeline", "pages.story", "pages.book", "pages.book_epub",
        "pages.export", "pages.import_page", "pages.drafts", "pages.archived",
        "pages.edit_story", "pages.new_story", "pages.story_media",
        "pages.person_media", "pages.tree_page", "pages.people_page",
        "pages.person_page", "pages.settings_page", "pages.setup_page",
        "pages.themes_page", "pages.theme_css", "pages.admin_accounts",
        "pages.groups_page", "pages.group_page", "pages.almanac",
        "pages.firsts", "pages.growth", "pages.random_page",
        "pages.use_write_link", "pages.manifest",
    ):
        assert endpoint in endpoints, f"{endpoint} is not registered"


def test_the_helpers_five_modules_import_are_public_names():
    """They were `_visible_stories`, `_people_dir`, `_serve_media`,
    `_person_ref`, `_other_people_refs` — imported across a module boundary
    by five files while claiming to be private. A leading underscore on a
    name in `views.py` now means it really is local to it."""
    from app import views

    for name in ("bp", "viewer_scope", "visible_stories", "get_story_or_404",
                 "available_groups", "visible_page_stories", "serve_media",
                 "current_people_dir", "person_ref", "other_people_refs",
                 "authors_and_colors", "color_for_author",
                 "DEFAULT_AUTHOR_COLOR"):
        assert hasattr(views, name), name

    for filename in PAGE_ROUTE_FILES + ("routes_api.py", "routes_api_people.py"):
        source = (APP / filename).read_text()
        assert "from .views import _" not in source
        assert "_visible_stories" not in source
        assert "_get_story_or_404" not in source
