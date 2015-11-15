# This is a scaffold just for self-learning (e.g. how to create a sublime plugin and distribute it) 
# During using SublimeLinter(https://github.com/SublimeLinter/SublimeLinter3), 
# when i tried to create a linter plugin, i found this in its source code
# This plugin is just extracted from Sublimelinter's command 
# named SublimelinterCreateLinterPluginCommand
#
# Project: https://github.com/molee1905/ShenMa
# License: MIT
# 


import sublime, sublime_plugin
import os
import tempfile
import shutil
import re
import subprocess
import datetime, time

SHORTCUTS_PATH_RE = re.compile(r'sc[/|\\]shortcuts', re.I)
SETTINGS_FILE = 'ShenMa.sublime-settings'
INPUT_SC_NAME = 'please input sc name: '
INPUT_SC_PATH = 'please input shortcuts path(e.g. xxx/sc/shortcuts): '
INVALID_SC_PATH = '''please input correct shortcuts path\r(e.g. $HOME/sc/shortcuts)  '''
ALREADY_EXISTED_ERROR = 'The shortcut “{}” already exists.'
COPY_ERROR = 'An error occurred while copying the template: {}'

def open_directory(path):
    cmd = (get_subl_executable_path(), path)
    subprocess.Popen(cmd, cwd=path)


def get_subl_executable_path():
    executable_path = sublime.executable_path()

    if sublime.platform() == 'osx':
        suffix = '.app/'
        app_path = executable_path[:executable_path.rfind(suffix) + len(suffix)]
        executable_path = app_path + 'Contents/SharedSupport/bin/subl'

    return executable_path

class CreateScCommand(sublime_plugin.WindowCommand):

    def run(self):
         
        self.settings = sublime.load_settings(SETTINGS_FILE)
        path = self.settings.get('path')
        
        if not path:
            self.window.show_input_panel(
                INPUT_SC_PATH,
                '',
                on_done=self.checkPath,
                on_change=None,
                on_cancel=None)
        else:
            self.checkPath(path)
        

    def checkPath(self, path):

        if self.isScPath(path):
            self.window.show_input_panel(
                INPUT_SC_NAME,
                '',
                on_done=self.render,
                on_change=None,
                on_cancel=None)
        else:
            if not sublime.ok_cancel_dialog(INVALID_SC_PATH):
                return
            self.window.show_input_panel(
                INPUT_SC_PATH,
                '',
                on_done=self.checkPath,
                on_change=None,
                on_cancel=None)


    def isScPath(self, path):
        match = SHORTCUTS_PATH_RE.search(path);
        if match:
            index = path.index('shortcuts')
            scpath = path[0:index]
            if os.path.exists(scpath):
                self.settings = sublime.load_settings(SETTINGS_FILE)
                self.settings.set('path', path)
                sublime.save_settings(SETTINGS_FILE)
                return True
        else: 
            self.settings.erase('path')

        return False

    
    def render(self, name):
        self.name = name
        self.author = os.getlogin()
        self.clzName = 'sc_{}'.format(name)
        self.cssPath = 'sc_advanced_{}.css'.format(name)
        self.jsPath = 'sc_{}.js'.format(name)

        settings = sublime.load_settings(SETTINGS_FILE)

        self.dest = os.path.join(settings.get('path'), self.name)

        if os.path.exists(self.dest):
            sublime.error_message(ALREADY_EXISTED_ERROR.format(self.name))
            return

        src = os.path.join(sublime.packages_path(), os.path.dirname(__file__), 'template')

        self.temp_dir = None

        try:
            self.temp_dir = tempfile.mkdtemp()
            self.temp_dest = os.path.join(self.temp_dir, self.name)

            shutil.copytree(src, self.temp_dest)

            if not self.fill_template(self.temp_dir, self.name):
                return
            
            shutil.move(self.temp_dest, self.dest)
            open_directory(self.dest)

        except Exception as ex:
            if self.temp_dir and os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)

            sublime.error_message(COPY_ERROR.format(str(ex)))

    def fill_template(self, template_dir, name):

        placeholders = {
            '__author__': self.author,
            '__name__': self.name,
            '__clz__': self.clzName,
            '__csspath__': self.cssPath,
            '__jspath__': self.jsPath,
            '__version__': '0.0.1'

        }

        for dirpath, dirnames, filenames in os.walk(template_dir):
            for filename in filenames:
                extension = os.path.splitext(filename)[1]

                if extension in ('.scss', '.js', '.html', '.md'):
                    path = os.path.join(dirpath, filename)

                    with open(path, encoding='utf-8') as f:
                        text = f.read()

                    for placeholder, value in placeholders.items():
                        text = text.replace(placeholder, value)

                    with open(path, mode='w', encoding='utf-8') as f:
                        f.write(text)

                    if extension in ('.scss', '.js'):
                        os.rename(path, os.path.join(dirpath, filename.format(name)))

        return True