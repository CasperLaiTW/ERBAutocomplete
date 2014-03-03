import sublime, sublime_plugin
import os
import sys
import re

ERBCOMPLETIONS_SETTING = 'ERBAutocomplete.sublime-settings'
ERBBASECOMPLETIONS_SETTING = 'ERBBasecomplete.sublime-settings'
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
PACKAGES_PATH = sublime.packages_path() or os.path.dirname(BASE_PATH)
ERB_GRAMMAR = 'Packages/%s/erb.tmLanguage' % os.path.basename(BASE_PATH).replace('.sublime-package', '')

# API
class Core():
    def __init__(self):
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

    def get_custom_tag(self):
        settings = sublime.load_settings(ERBCOMPLETIONS_SETTING).get('customCompletions')
        customWords = []
        for custom in settings:
            customWords.extend(sublime.load_settings(custom).get('completions'))
        return customWords

    def get_grammar_path(self):
        return ERB_GRAMMAR

    def get_project_path(self, path):
        if path is None:
            sublime.active_window().new_file()
            return None

        project_dir = os.path.normcase(os.path.dirname(path))
        win = sublime.active_window()
        for project in win.folders():
            index = project_dir.lower().find(project.lower())
            if(index > -1):
                relatives = project_dir.replace(project, '').split('/')[1:]
                base = project
                for relative in relatives:
                    base = os.path.join(base, relative)
                    if os.path.isfile(os.path.join(base, '.base')):
                        return base
                return os.path.normcase(project)
        return None