import sublime, sublime_plugin
import os
import sys
import re


ERBCOMPLETIONS_SETTING = 'ERBAutocomplete.sublime-settings'
ERBBASECOMPLETIONS_SETTING = 'ERBBasecomplete.sublime-settings'
BASE_PATH = os.path.abspath(os.path.dirname(__file__))
PACKAGES_PATH = sublime.packages_path() or os.path.dirname(BASE_PATH)
ERB_GRAMMAR = 'Packages/%s/erb.tmLanguage' % os.path.basename(BASE_PATH).replace('.sublime-package', '')
is_python3 = sys.version_info[0] > 2
ERBComplete = None
# API
class ERBAutoCompleteAPI():
    def init(self):
        settings = sublime.load_settings(ERBCOMPLETIONS_SETTING).get('customCompletions')
        customWords = []
        for custom in settings:
            customWords.extend(sublime.load_settings(custom).get('completions'))

        self.customWords = customWords
        self.words = []
        self.words = sublime.load_settings(ERBBASECOMPLETIONS_SETTING)
    def get_line_text(self, view):
        sel = view.sel()
        region = sel[0]
        line = view.line(region)
        start = line.a
        end = sel[0].a
        cursor = sublime.Region(start, end)
        cursorText = view.substr(cursor)
        temp = re.split("[^\w\.\%<]", cursorText)
        return temp
    def get_lines_text(self, view):
        sel = view.sel()
        region = sel[0]
        line = view.line(region)
        start = line.a
        end = line.b
        cursor = sublime.Region(start, end)
        cursorText = view.substr(cursor)
        return cursorText
# Completion
class ERBAutocompleteListener(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        self.completions = []
        specialkey = False
        scope = ERBComplete.words.get('scope')
        
        temp = ERBComplete.get_line_text(view)
        lineText = temp[-1]

        specialkey = True if lineText.find("<") >= 0 else False
        
        if scope and view.match_selector(locations[0], scope):
            self.completions += ERBComplete.words.get('completions')
            self.completions += ERBComplete.customWords
        if not self.completions:
            return []

        completions = list(self.completions)
        if specialkey:
            for idx, item in enumerate(self.completions):
                self.completions[idx][1] = item[1][1:]
            
        completions = [tuple(attr) for attr in self.completions]
        return completions

    def on_load(self, view):
        filename = view.file_name()
        if not filename:
            return
        name = os.path.basename(filename.lower())
        if name[-8:] == "html.erb" or name[-3:] == "erb":
            try:
                view.settings().set('syntax', ERB_GRAMMAR)
                print("Switched syntax to: ERB")
            except:
                pass

class IndicatesCommentCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        target = '<%'
        
        # find target
        lines = ERBComplete.get_lines_text(self.view)
        reg = re.search('<%(=|\s+)', lines)
        if(reg == None): return
        idx = reg.start()

        # get current select line
        sel = self.view.sel()
        region = sel[0]
        sel_line = self.view.line(region)
        start = sel_line.a + idx
        end = start + len(target)

        replace_region = sublime.Region(start, end)
        self.view.replace(edit, replace_region, '<%#')

# Init
def init():
    globals()['ERBComplete'] = ERBAutoCompleteAPI()
    ERBComplete.init()

def plugin_loaded():
    sublime.set_timeout(init, 200)

##################
# Init plugin
if not is_python3:
    init()

