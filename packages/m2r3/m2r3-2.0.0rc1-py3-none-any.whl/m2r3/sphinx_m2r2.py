from .m2r2 import __version__
from .parser import M2RParser
from .directives import MdInclude

_is_sphinx = False


def setup(app):
    print("m2r3 setup.")
    """When used for sphinx extension."""
    global _is_sphinx
    _is_sphinx = True
    app.add_config_value("no_underscore_emphasis", False, "env")
    app.add_config_value("m2r_parse_relative_links", False, "env")
    app.add_config_value("m2r_anonymous_references", False, "env")
    app.add_config_value("m2r_disable_inline_math", False, "env")
    app.add_config_value(
        "m2r_use_mermaid", "sphinxcontrib.mermaid" in app.config.extensions, "env"
    )
    try:
        app.add_source_parser(".md", M2RParser)  # for older sphinx versions
    except (TypeError, AttributeError):
        app.add_source_suffix(".md", "markdown")
        app.add_source_parser(M2RParser)
    print("included mdinclude")
    app.add_directive("mdinclude", MdInclude)
    metadata = dict(
        version=__version__,
        parallel_read_safe=True,
        parallel_write_safe=True,
    )
    return metadata
