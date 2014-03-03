import sublime, sublime_plugin;
import os;
import re;
try:
    # ST3
    from ..apis.core import Core
except (ImportError, ValueError):
    # ST2
    from apis.core import Core

class MappingLayoutCommand(sublime_plugin.WindowCommand):
    def run(self, *args, **kwargs):
        core = Core()
        self.layout_list = []
        core = Core()
        path = self.window.active_view().file_name();

        if core.is_erb_file(path) is False:
            sublime.error_message('File is not ERB file.')
            return
        self.project_dir = core.get_project_path(path)
        if self.project_dir is not None:
            for name in os.listdir(self.project_dir):
                if core.is_erb_layout_file(name) is False:
                    continue
                if os.path.isfile(os.path.join(self.project_dir, name)) :
                    self.layout_list.append([name, os.path.join(self.project_dir, name)])
            sublime.active_window().show_quick_panel(self.layout_list, self.on_mapping);
        else:
            sublime.error_message('We don\'t find your project folder. Please check your \'.base\' file.')

    def on_mapping(self, index):
        if index > -1:
            custom_layout = self.layout_list[index][0]
            filename = os.path.basename(self.window.active_view().file_name())
            mapping_layout_file = os.path.join(self.project_dir, filename[:-3] + 'layout')
            f = open(mapping_layout_file, "w")
            f.write(custom_layout)
            f.close()


