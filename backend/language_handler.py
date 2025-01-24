import subprocess

def open_compiler(language):
    """Open the compiler or editor for the selected programming language."""
    compilers = {
        "C": "codeblocks",  # Replace with actual paths
        "C++": "codeblocks",
        "Java": "eclipse",
        "Python": "python"
    }
    editor = compilers.get(language)
    if editor:
        subprocess.Popen(editor, shell=True)
    else:
        raise ValueError("Unsupported language")
