import glob
import os

from invoke import task


@task
def update(c):
    txt_files = glob.glob("requirements/*.txt")
    for file in txt_files:
        os.remove(file)

    in_files = glob.glob("requirements/*.in")
    for file in in_files:
        path, ext = file.split(".")
        c.run(f"pip-compile {file} -o {path}.txt")

    c.run(f"pip-compile {' '.join(in_files)} -o requirements/all.txt")


@task
def sync(c):
    c.run("pip-sync requirements/all.txt")


@task
def deploy(c):
    c.run("cdk deploy HelloWorldStack --profile bjss-tom")
