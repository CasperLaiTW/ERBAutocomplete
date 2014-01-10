import sublime, sublime_plugin
import os
ERBCOMPLETIONS_SETTING = 'ERBAutocomplete.sublime-settings'
BASE_PATH = os.path.abspath(os.path.dirname(__file__))
PACKAGES_PATH = sublime.packages_path() or os.path.dirname(BASE_PATH)
ERB_GRAMMAR = 'Packages/%s/erb.tmLanguage' % os.path.basename(BASE_PATH).replace('.sublime-package', '')

class ERBAutoCompleteAPI():
    def init(self):
        self.words = []
        self.words = sublime.load_settings(ERBCOMPLETIONS_SETTING)

class ERBAutocompleteListener(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        self.completions = []
        specialkey = False
        scope = ERBComplete.words.get('scope')
        
        for region in view.sel():  
            if region.empty():
                line = view.line(region)
                lineContents = view.substr(line)
        specialkey = True if lineContents[:2].find("<") == 1 else False

        if scope and view.match_selector(locations[0], scope):
            self.completions += ERBComplete.words.get('completions')
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