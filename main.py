import sublime
import sublime_plugin

try:
    # ST3
    from .library.commands.mark import MarkCommentCommand
    from .library.commands.unmark import UnmarkCommentCommand
    from .library.commands.create_layout import CreateLayoutCommand
    from .library.commands.mapping import MappingLayoutCommand
    from .library.commands.unmapping import UnmappingLayoutCommand
    from .library.events.listener import ERBAutocompleteListener
except (ImportError, ValueError):
    # ST2
    from library.commands.mark import MarkCommentCommand
    from library.commands.unmark import UnmarkCommentCommand
    from library.commands.create_layout import CreateLayoutCommand
    from library.commands.mapping import MappingLayoutCommand
    from library.commands.unmapping import UnmappingLayoutCommand
    from library.events.listener import ERBAutocompleteListener
