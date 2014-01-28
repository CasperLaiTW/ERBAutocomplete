import sublime, sublime_plugin
import os
import re
ERBCOMPLETIONS_SETTING = 'ERBAutocomplete.sublime-settings'
ERBBASECOMPLETIONS_SETTING = 'ERBBasecomplete.sublime-settings'
BASE_PATH = os.path.abspath(os.path.dirname(__file__))
PACKAGES_PATH = sublime.packages_path() or os.path.dirname(BASE_PATH)
ERB_GRAMMAR = 'Packages/%s/erb.tmLanguage' % os.path.basename(BASE_PATH).replace('.sublime-package', '')

class ERBAutoCompleteAPI():
    def init(self):
        settings = sublime.load_settings(ERBCOMPLETIONS_SETTING).get('customCompletions')
        customWords = []
        for custom in settings:
            customWords.extend(sublime.load_settings(custom).get('completions'))

        self.customWords = customWords
        self.words = []
        self.words = sublime.load_settings(ERBBASECOMPLETIONS_SETTING)

class ERBAutocompleteListener(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        self.completions = []
        specialkey = False
        scope = ERBComplete.words.get('scope')
        
        sel = view.sel()
        region = sel[0]
        line = view.line(region)
        start = line.a
        end = sel[0].a
        cursor = sublime.Region(start, end)
        cursorText = view.substr(cursor)
        temp = re.split("[^\w\.<]", cursorText)
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
            
ERBComplete = ERBAutoCompleteAPI()
def plugin_loaded():
    ERBComplete.init()