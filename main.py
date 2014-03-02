import sublime
import sublime_plugin

try:
    # ST3
    from .commands.mark import MarkCommentCommand
    from .commands.unmark import UnmarkCommentCommand
    from .events.completion import ERBAutocompleteListener
except (ImportError, ValueError):
    # ST2
    from commands.mark import MarkCommentCommand
    from commands.unmark import UnmarkCommentCommand
    from events.completion import ERBAutocompleteListener
