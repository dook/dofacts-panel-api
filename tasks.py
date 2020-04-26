from invoke import task

LINE_LENGTH = "90"

PATHS = ["dofacts", "tests"]
EXCLUDE = ["*/migrations/*", "*/users/*"]


@task
def isort(c):
    options = [
        "--recursive",
        "--multi-line=3",
        "--trailing-comma",
        "--force-grid-wrap=0",
        "--use-parentheses",
        "--atomic",
        f"--line-width={LINE_LENGTH}",
        '-sg="*/migrations/*"'
    ]
    c.run(f"isort {' '.join(PATHS)} {' '.join(options)}")


@task
def black(c):
    options = [f"--line-length={LINE_LENGTH}", f"--exclude=.*/migrations/*"]
    c.run(f"black {' '.join(PATHS)} {' '.join(options)}")


@task
def reformat(c):
    isort(c)
    black(c)


@task
def lint(c):
    c.run(f"flake8 --max-line-length {LINE_LENGTH} --extend-ignore=E203")
