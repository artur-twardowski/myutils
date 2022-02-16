import subprocess
import os
from os.path import join, expanduser, abspath
import shlex
from sys import argv, stdout
import re
from getopt import gnu_getopt


def print_cmd(cmd):
    message = ">> Executing command: %s" % cmd
    print("\x1b[1;32m%s\x1b[0m" % message)


def print_step(step):
    message = "** %s **" % step
    print("\x1b[1;33m%s\x1b[0m" % message)


def print_error(msg):
    message = "ERROR: %s" % msg
    print("\x1b[1;31m%s\x1b[0m" % message)


def exec_or_die(cmd):
    print_cmd(shlex.join(cmd))
    proc = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    result = proc.wait()

    if result != 0:
        for line in stdout.decode('utf-8').split('\n'):
            print_error(line)
        print_error("Command returned %d" % result)
        exit(1)


def exec_or_die_interactive(cmd):
    print_cmd(shlex.join(cmd))
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print_error("Command returned %d" % result.returncode)
        exit(1)


class DownloadDescriptor:
    RES_FILE = 1
    RES_FILE_WITH_PREPROCESS = 2
    RES_GIT_REPO = 3

    def __init__(self, resource_type, paths, dest_dir, dest_filename):
        self.res_type = resource_type
        self.paths = paths
        self.dest_dir = dest_dir
        self.dest_filename = dest_filename


class Condition:
    def __init__(self, key, op):
        self._key = key
        self._op = op
        self.negate = False

    def is_met(self, defines: dict):
        result = False
        if self._op == "defined":
            result = self._key in defines

        if self.negate:
            result = not result

        return result


class Preprocessor:
    def __init__(self):
        self._defines = {}
        self._conditions = []
        self.re_ifdef = re.compile(r'#ifdef\s+([A-Za-z0-9_]+)')
        self.re_else = re.compile('#else')
        self.re_endif = re.compile('#endif')

    def set_definition(self, key, value=""):
        self._defines[key] = value

    def unset_definition(self, key):
        del self._defines[key]

    def get_definitions(self):
        return self._defines

    def feed_line(self, line):
        line_stripped = line.strip()

        if self.re_ifdef.match(line_stripped):
            sym = self.re_ifdef.findall(line_stripped)[0]
            self._conditions.append(Condition(sym, "defined"))
            return None

        if self.re_else.match(line_stripped):
            self._conditions[-1].negate = True
            return None

        if self.re_endif.match(line_stripped):
            self._conditions.pop()
            return None

        for cond in self._conditions:
            if not cond.is_met(self._defines):
                return None

        for key, value in self._defines.items():
            key_f = "<%s>" % key
            if key_f in line:
                line = line.replace(key_f, value)

        return line


class Configuration:
    def __init__(self):
        self.lang_server_plugin = "lsp"
        self.path_to_vimrc = join(expanduser("~"), ".vimrc")
        self.path_to_vimdir = join(expanduser("~"), ".vim")
        self.confirm_before_proceeding = True

    def create_from_command_line(self, args):
        optlist, args = gnu_getopt(args, "L:d:f:y")

        for key, value in optlist:
            if key in ["-L"]:
                self.lang_server_plugin = value
            elif key in ["-d"]:
                self.path_to_vimdir = value
            elif key in ["-f"]:
                self.path_to_vimrc = value
            elif key in ['-y']:
                self.confirm_before_proceeding = False

    def validate(self):
        supported_lang_server_plugins = ["ycm", "lsp"]
        if self.lang_server_plugin not in supported_lang_server_plugins:
            print_error("Unsupported language server plugin \"%s\". Possible values: %s" % (self.lang_server_plugin, supported_lang_server_plugins))
            return False

        self.path_to_vimrc = abspath(self.path_to_vimrc)
        self.path_to_vimdir = abspath(self.path_to_vimdir)

def preprocess(preprocessor:Preprocessor, filename):
    print_step("Preprocessing %s" % filename)
    processed_content = ""

    with open(filename, "r") as f:
        for line in f:
            proc_line = preprocessor.feed_line(line)
            if proc_line is not None: processed_content += proc_line

    with open(filename, "w") as f:
        f.write(processed_content)


if __name__ == "__main__":
    conf = Configuration()
    preprocessor = Preprocessor()
    conf.create_from_command_line(argv[1:])
    conf.validate()
    INITIALDIR = os.getcwd()

    files_to_download = [
            DownloadDescriptor(
                DownloadDescriptor.RES_FILE_WITH_PREPROCESS,
                ["vimrc_base", "https://raw.githubusercontent.com/artur-twardowski/myutils/master/vim/vimrc_base"],
                conf.path_to_vimdir, "vimrc_base"),
            DownloadDescriptor(
                DownloadDescriptor.RES_FILE_WITH_PREPROCESS,
                ["vimrc_extensions", "https://raw.githubusercontent.com/artur-twardowski/myutils/master/vim/vimrc_extensions"],
                conf.path_to_vimdir, "vimrc_extensions"),
            DownloadDescriptor(
                DownloadDescriptor.RES_GIT_REPO,
                ["https://github.com/VundleVim/Vundle.vim.git"],
                join(conf.path_to_vimdir, "bundle"), "Vundle.vim")
    ]

    if conf.lang_server_plugin == "ycm":
        files_to_download.append(DownloadDescriptor(
            DownloadDescriptor.RES_GIT_REPO,
            ["https://github.com/ycm-core/YouCompleteMe.git"],
            join(conf.path_to_vimdir, "bundle"), "YouCompleteMe"))

    if conf.lang_server_plugin == "lsp":
        preprocessor.set_definition("USE_LSP")
    elif conf.lang_server_plugin == "ycm":
        preprocessor.set_definition("USE_YCM")

    print("Vim directory:          %s" % conf.path_to_vimdir)
    print("Path to vimrc:          %s" % conf.path_to_vimrc)
    print("Language server plugin: %s" % conf.lang_server_plugin)
    print("Definitions:")
    for key, value in preprocessor.get_definitions().items():
        print("  - %-30s %s" % (key, value))

    print("Content to download:")
    for dl in files_to_download:
        stdout.write("  - Into %s\n" % join(dl.dest_dir, dl.dest_filename))
        for path in dl.paths:
            if dl.res_type == DownloadDescriptor.RES_FILE or dl.res_type == DownloadDescriptor.RES_FILE_WITH_PREPROCESS:
                if path.find("://") != -1:
                    stdout.write("    download file %s" % path)
                else:
                    stdout.write("    copy local file %s" % path)
                    if not os.path.isfile(path):
                        stdout.write(" (does not exist)")

                if dl.res_type == DownloadDescriptor.RES_FILE_WITH_PREPROCESS:
                    stdout.write(" and preprocess")
                stdout.write("\n")
            if dl.res_type == DownloadDescriptor.RES_GIT_REPO:
                stdout.write("    checkout Git repository %s\n" % path)

    if conf.confirm_before_proceeding:
        stdout.write("Continue setup? [y/N]: ")
        response = input()
        if len(response) > 0 and response[0] not in ['y', 'Y']:
            exit(1)
    print_step("Downloading required files")

    for dl in files_to_download:
        if not os.path.exists(dl.dest_dir):
            print("Directory %s does not exist, creating" % dl.dest_dir)
            exec_or_die(["mkdir", "-p", dl.dest_dir])

        found = False
        for source in dl.paths:
            if dl.res_type in [DownloadDescriptor.RES_FILE, DownloadDescriptor.RES_FILE_WITH_PREPROCESS]:
                if source.find("://") == -1:
                    if os.path.exists(source) and False:
                        exec_or_die(["cp", source, join(dl.dest_dir, dl.dest_filename)])
                        found = True
                        print("Local %s found" % source)
                    else:
                        print("Local %s not found" % source)
                else:
                    exec_or_die(["wget", source, "-O", join(dl.dest_dir, dl.dest_filename)])
                    found = True
                    print("Remote %s found" % source)

                if dl.res_type == DownloadDescriptor.RES_FILE_WITH_PREPROCESS and found:
                    preprocess(preprocessor, join(dl.dest_dir, dl.dest_filename))

            elif dl.res_type == DownloadDescriptor.RES_GIT_REPO:
                try:
                    exec_or_die(["rm", "-rf", join(dl.dest_dir, dl.dest_filename)])
                    exec_or_die(["git", "clone", source, join(dl.dest_dir, dl.dest_filename)])
                    found = True
                    print("Remote %s found" % source)
                except AssertionError:
                    print("Repository at %s already cloned" % join(dl.dest_dir, dl.dest_filename))
            
            if found:
                break
        if not found:
            print_error("Could not provide %s" % dl.dest_filename)

    add_vimrc_base = True
    add_vimrc_extensions = True
    add_vimrc_projectspec = True

    print_step("Analyzing existing vimrc")
    try:
        vimrc = open(conf.path_to_vimrc, "r")
        for line in vimrc:
            line = line.strip()
            if line.startswith("source ") or line.startswith("so "):
                _, sourced_file = line.split(' ', 1)
                
                if sourced_file == join(conf.path_to_vimdir, "vimrc_base"):
                    print("vimrc_base already sourced in vimrc")
                    add_vimrc_base = False

                if sourced_file == join(conf.path_to_vimdir, "vimrc_extensions"):
                    print("vimrc_extensions already sourced in vimrc")
                    add_vimrc_extensions = False

                if sourced_file == join(conf.path_to_vimdir, "vimrc_projectspec"):
                    print("vimrc_projectspec already sourced in vimrc")
                    add_vimrc_projectspec = False
        vimrc.close()
    except FileNotFoundError:
        print("vimrc file (%s) does not exist, will be created" % conf.path_to_vimrc)
    
    print_step("Updating vimrc")
    try:
        vimrc = open(conf.path_to_vimrc, "a+")
        if add_vimrc_base:
            vimrc.write("source %s\n" % os.path.join(conf.path_to_vimdir, "vimrc_base"))
        if add_vimrc_extensions:
            vimrc.write("source %s\n" % os.path.join(conf.path_to_vimdir, "vimrc_extensions"))

        filename_vimrc_projectspec = os.path.join(conf.path_to_vimdir, "vimrc_projectspec")
        if add_vimrc_projectspec:
            if os.path.exists(filename_vimrc_projectspec):
                vimrc.write("source %s\n" % filename_vimrc_projectspec)
            else:
                vimrc.write("\"source %s \"Uncomment it in case you create this file!\n" % filename_vimrc_projectspec)
        vimrc.close()
    except Exception as ex:
        print("Error while writing vimrc (%s): %s: " % (conf.path_to_vimrc, str(ex)))

    if conf.lang_server_plugin == "ycm":
        print_step("Building YouCompleteMe")
        dir = join(conf.path_to_vimdir, "bundle", "YouCompleteMe")
        print("Entering directory %s" % dir)
        os.chdir(dir)
        exec_or_die(["git", "submodule", "update", "--init", "--recursive"])
        exec_or_die(["python3", "install.py", "--clangd-completer"])
        os.chdir(INITIALDIR)

    print_step("Running post-installation")
    exec_or_die_interactive(["vim", "+PluginInstall", "+qall"])

