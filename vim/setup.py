import subprocess
import os
import shlex
from sys import argv

FILES_TO_FETCH=(
        (["vimrc_base", "https://raw.githubusercontent.com/artur-twardowski/myutils/master/vim/vimrc_base"], "$VIMDIR", "vimrc_base"),
        (["vimrc_extensions", "https://raw.githubusercontent.com/artur-twardowski/myutils/master/vim/vimrc_extensions"], "$VIMDIR", "vimrc_extensions"),
        ("git://github.com/VundleVim/Vundle.vim.git", "$VIMDIR/bundle", "Vundle.vim"),
        ("git://github.com/ycm-core/YouCompleteMe.git", "$VIMDIR/bundle", "YouCompleteMe")
        )

def exec_or_die(cmd):
    print(">>> %s" % shlex.join(cmd))
    result = subprocess.run(cmd)
    assert result.returncode == 0, "Command returned %d" % result.returncode

if __name__ == "__main__":
    VIMDIR = None
    VIMRC = None
    INITIALDIR = os.getcwd()

    if len(argv) == 3:
        VIMRC = argv[1]
        VIMDIR = argv[2]
    elif len(argv) == 2:
        VIMRC = os.path.join(argv[1], ".vimrc")
        VIMDIR = os.path.join(argv[1], ".vim")
    else:
        print("USAGE: %s <home-directory>" % argv[0])
        print("       %s <vimrc-path> <vim-directory>" % argv[0])
        exit(1)

    print("VIMRC  = %s\nVIMDIR = %s" % (VIMRC, VIMDIR))

    for sources, destination, dest_filename in FILES_TO_FETCH:
        destination = destination.replace("$VIMDIR", VIMDIR)
        if not os.path.exists(destination):
            print("Directory %s does not exist, creating" % destination)
            exec_or_die(["mkdir", "-p", destination])

        if not isinstance(sources, list):
            sources = [sources]

        for source in sources:
            found = False
            if source.find("://") == -1:
                if os.path.exists(source):
                    exec_or_die(["cp", source, os.path.join(destination, dest_filename)])
                    found = True
            elif source.find("https://") != -1:
                exec_or_die(["wget", source, "-O", os.path.join(destination, dest_filename)])
                found = True
            elif source.find("git://") != -1:
                source = source.replace("git://", "https://")
                try:
                    exec_or_die(["git", "clone", source, os.path.join(destination, dest_filename)])
                except AssertionError:
                    print("Repository at %s already cloned" % os.path.join(destination, dest_filename))
            if found: break

    add_vimrc_base = True
    add_vimrc_extensions = True
    add_vimrc_projectspec = True

    print("*** DOWNLOADING REQUIRED FILES ***")
    try:
        vimrc = open(VIMRC, "r")
        for line in vimrc:
            line = line.strip()
            if line.startswith("source ") or line.startswith("so "):
                _, sourced_file = line.split(' ', 1)
                
                if sourced_file == os.path.join(VIMDIR, "vimrc_base"):
                    print("vimrc_base already sourced in vimrc")
                    add_vimrc_base = False

                if sourced_file == os.path.join(VIMDIR, "vimrc_extensions"):
                    print("vimrc_extensions already sourced in vimrc")
                    add_vimrc_extensions = False

                if sourced_file == os.path.join(VIMDIR, "vimrc_projectspec"):
                    print("vimrc_projectspec already sourced in vimrc")
                    add_vimrc_projectspec = False
        vimrc.close()
    except FileNotFoundError:
        print("vimrc file (%s) does not exist, will be created" % (VIMRC))

    print("*** BUILDING YouCompleteMe ***")
    dir = os.path.join(VIMDIR, "bundle", "YouCompleteMe")
    print("Entering directory %s" % dir)
    os.chdir(dir)
    exec_or_die(["git", "submodule", "update", "--init", "--recursive"])
    exec_or_die(["python3", "install.py", "--clangd-completer"])
    os.chdir(INITIALDIR)

    print("*** INSTALLING VIMRC ***")
    try:
        vimrc = open(VIMRC, "a+")
        if add_vimrc_base:
            vimrc.write("source %s\n" % os.path.join(VIMDIR, "vimrc_base"))
        if add_vimrc_extensions:
            vimrc.write("source %s\n" % os.path.join(VIMDIR, "vimrc_extensions"))

        filename_vimrc_projectspec = os.path.join(VIMDIR, "vimrc_projectspec")
        if add_vimrc_projectspec:
            if os.path.exists(filename_vimrc_projectspec):
                vimrc.write("source %s\n" % filename_vimrc_projectspec)
            else:
                vimrc.write("\"source %s \"Uncomment it in case you create this file!\n" % filename_vimrc_projectspec)
        vimrc.close()
    except Exception as ex:
        print("Error while writing vimrc (%s): %s: " % (VIMRC, str(ex)))

    print("*** RUNNING POST-INSTALLATION ***")
    exec_or_die(["vim", "+PluginInstall", "+qall"])

