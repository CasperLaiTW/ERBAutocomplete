import sublime, sublime_plugin

ERBCOMPLETIONS_SETTING = "ERBAutocomplete.sublime-settings"

class ERBAutoCompleteAPI():
    def init(self):
        self.words = []
        self.words = sublime.load_settings(ERBCOMPLETIONS_SETTING)

ERBComplete = ERBAutoCompleteAPI()

if int(sublime.version()) < 3000:
    erbCompletion.init()
else:
    def plugin_loaded():
        global ERBComplete
        ERBComplete.init()

class ERBAutocompleteListener(sublime_plugin.EventListener):
    global ERBComplete
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




