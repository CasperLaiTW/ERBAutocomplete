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
        scope = ERBComplete.words.get('scope')
        
        if scope and view.match_selector(locations[0], scope):
            self.completions += ERBComplete.words.get('completions')
        if not self.completions:
            return []
            
        window = sublime.active_window()
        baseCompletions = [view.extract_completions(prefix)]
        baseCompletions = [(item,item) for sublist in baseCompletions for item in sublist] #flatten
        baseCompletions = list(set(baseCompletions))
        completions = list(self.completions)
        completions = [tuple(attr) for attr in self.completions]
        completions.extend(baseCompletions)
        return completions

    def on_load(self, view):
        filename = view.file_name()
        if not filename:
            return
        name = os.path.basename(filename.lower())
        if name[-8:] == "html.erb" or name[-3:] == "erb":
            view.settings().set('syntax', ERB_GRAMMAR)
            print("Switched syntax to: ERB")


ERBComplete = ERBAutoCompleteAPI()
def plugin_loaded():
    ERBComplete.init()