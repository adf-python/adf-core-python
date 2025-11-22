import os
import subprocess

# a single build step, which keeps conf.py and versions.yaml at the main branch
# in generall we use environment variables to pass values to conf.py, see below
# and runs the build as we did locally
def build_doc(language):
    os.environ["current_language"] = language
    subprocess.run("doxygen Doxyfile", shell=True)
    os.environ['SPHINXOPTS'] = "-D language='{}'".format(language)
    subprocess.run("make html", shell=True)

# a move dir method because we run multiple builds and bring the html folders to a
# location which we then push to github pages
def move_dir(src, dst):
  subprocess.run(["mkdir", "-p", dst])
  subprocess.run("mv "+src+'* ' + dst, shell=True)

# to separate a single local build from all builds we have a flag, see conf.py
os.environ["build_all_docs"] = str(True)
os.environ["pages_root"] = "https://adf-python.github.io/adf-core-python/"

# manually the main branch build in the current supported languages
build_doc("en")
move_dir("./build/html/", "./pages/en")
build_doc("ja")
move_dir("./build/html/", "./pages/ja")
