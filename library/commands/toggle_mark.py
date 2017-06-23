import sublime, sublime_plugin
import re
try:
    # ST3
    from ..apis.core import Core
except (ImportError, ValueError):
    # ST2
    from apis.core import Core

class ToggleMarkCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # new core
        core = Core()
        
        # find target
        lines = core.get_lines_text(self.view)

        if self.isMark(lines):
            self.unmark(edit, lines)
        else:
            self.mark(edit, lines)

    def isMark(self, lines):
        target = '<%#'
        reg = re.search(target, lines)
        if(reg == None):
            return False

        return True

    def mark(self, edit, lines):
        target = '<%'
        reg = re.search('<%(=|\s+)', lines)
        idx = reg.start()

        sel = self.view.sel()
        region = sel[0]
        sel_line = self.view.line(region)
        start = sel_line.a + idx
        end = start + len(target)

        replace_region = sublime.Region(start, end)
        self.view.replace(edit, replace_region, '<%#')


    def unmark(self, edit, lines):
        target = '<%#'
        reg = re.search(target, lines)
        idx = reg.start()

        sel = self.view.sel()
        region = sel[0]
        sel_line = self.view.line(region)
        start = sel_line.a + idx
        end = start + len(target)

        replace_region = sublime.Region(start, end)
        self.view.replace(edit, replace_region, '<%')

