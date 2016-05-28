# 1.create projects skeleton based on defined scaffolds
# 2.create eslint.sublime-build
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
import json

SHORTCUTS_PATH_RE = re.compile(r'sc[/|\\]shortcuts', re.I)
INPUT_SC_NAME = 'please input sc name: '
INPUT_SC_PATH = 'please input shortcuts path(e.g. xxx/sc/shortcuts): '
INVALID_SC_PATH = '''please input correct shortcuts path\r(e.g. $HOME/sc/shortcuts)  '''
ALREADY_EXISTED_ERROR = 'The shortcut “{}” already exists.'
COPY_ERROR = 'An error occurred while copying the template: {}'

SETTINGS_FILE = 'ShenMa.sublime-settings'




def open_directory(path):
    cmd = (get_subl_executable_path(),'-a',path)
    subprocess.Popen(cmd)


def get_subl_executable_path():
    executable_path = sublime.executable_path()

    if sublime.platform() == 'osx':
        suffix = '.app/'
        app_path = executable_path[:executable_path.rfind(suffix) + len(suffix)]
        executable_path = app_path + 'Contents/SharedSupport/bin/subl'

    return executable_path


class CreateScCommand(sublime_plugin.WindowCommand):
    """A command that creates a new sc """
    
    def run(self):
         
        self.settings = sublime.load_settings(SETTINGS_FILE)
        path = self.settings.get('shortcuts')

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
                self.settings.set('shortcuts', path)
                sublime.save_settings(SETTINGS_FILE)
                return True
        else: 
            self.settings.erase('shortcuts')

        return False

    
    def render(self, name):
        self.name = name
        self.author = os.getlogin()
        self.clzName = 'sc_{}'.format(name)
        self.cssPath = 'sc_advanced_{}.css'.format(name)
        self.jsPath = 'sc_{}.js'.format(name)


        self.dest = os.path.join(self.settings.get('shortcuts'), self.name)

        if os.path.exists(self.dest):
            sublime.error_message(ALREADY_EXISTED_ERROR.format(self.name))
            return

        src = os.path.join(sublime.packages_path(), os.path.dirname(__file__), 'template')

        self.temp_dir = None

        try:
            self.temp_dir = tempfile.mkdtemp()
            self.temp_dest = os.path.join(self.temp_dir, self.name)

            shutil.copytree(src, self.temp_dest)
            
            os.mkdir(os.path.join(self.temp_dest, 'data'))
            os.mkdir(os.path.join(self.temp_dest, 'img'))
            os.mkdir(os.path.join(self.temp_dest, 'res'))
            os.mkdir(os.path.join(self.temp_dest, 'tmpl'))

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

class FormatJsCommand(sublime_plugin.TextCommand):
    """format js base on eslint """
    
    def run(self, edit):
        settings = sublime.load_settings(SETTINGS_FILE)
        NODE_BIN = settings.get('node_bin')
        ESLINT_BIN = settings.get('eslint_bin')

        if not NODE_BIN:
            sublime.error_message('请在配置中添加nodejs路径')
            return
        if not os.path.exists(NODE_BIN):
            sublime.error_message('nodejs路径错误')
            return

        filename = self.view.file_name()
        if not filename.lower().endswith('.js'):
            return
        filename = os.path.abspath(filename)
        args = [NODE_BIN, ESLINT_BIN, '--fix', filename]
        proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        fmt, err = proc.communicate()

        print('fmt: ', fmt.decode('utf-8'))