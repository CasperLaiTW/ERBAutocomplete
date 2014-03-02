import sublime
import sublime_plugin

try:
    # ST3
    from .library.commands.mark import MarkCommentCommand
    from .library.commands.unmark import UnmarkCommentCommand
    from .library.events.completion import ERBAutocompleteListener
except (ImportError, ValueError):
    # ST2
    from library.commands.mark import MarkCommentCommand
    from library.commands.unmark import UnmarkCommentCommand
    from library.events.completion import ERBAutocompleteListener
