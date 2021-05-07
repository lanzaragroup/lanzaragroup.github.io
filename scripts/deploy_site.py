"""
A small, relatively portable build script.
"""
import uuid
import contextlib
import shutil
import distutils.dir_util
import subprocess
from pathlib import Path
import os

JEKYLL_REPO_ROOT: Path = (Path(__file__).parent / "..").resolve()
DEPLOY_REPO_ROOT = (JEKYLL_REPO_ROOT / ".." / "lanzara-staging").resolve()
RUBY_VERSION = "3.0.1"
MISSING_RUBY_MESSAGE = """
It looks like you do not have Ruby installed. Please install
via the Ruby Version Manager (RVM) before trying to build
the site. You will need to use Ruby version: {ruby_version}, i.e

$> rvm use {ruby_version}
"""


@contextlib.contextmanager
def temporary_cwd(new_working_directory):
    old_cwd = os.getcwd()

    os.chdir(str(new_working_directory))
    yield

    os.chdir(old_cwd)


def guard_ruby_version(ruby_version: str = "3.0.1"):
    """
    To help make builds more reproducible we use a fixed Ruby
    version. If that version is not detected then we suggest
    how to use the right one.
    """

    ruby_info = subprocess.run(["ruby", "--version"], capture_output=True)

    if ruby_info.returncode != 0:
        print(MISSING_RUBY_MESSAGE.format(ruby_version))
        raise ValueError("No Ruby")

    output = ruby_info.stdout.decode()
    if ruby_version not in output:
        print("Detected incorrect Ruby version:")
        print(output)
        print(f"Please use version: {ruby_version} via RVM.")
        raise ValueError("Wrong Ruby version")


def guard_jekyll_repo_clean():
    status = subprocess.run(["git", "status", "--porcelain"], capture_output=True)
    if status.stdout.decode().strip():
        print("Stopping. The source repo is not committed.")
        print(status.stdout.decode())
        exit(1)


def bundle_install():
    bundle_result = subprocess.run(["bundle", "install"])
    if bundle_result.returncode != 0:
        exit(bundle_result.returncode)


def build_site():
    build_result = subprocess.run(["bundle", "exec", "jekyll", "build"])
    if build_result.returncode != 0:
        exit(build_result.returncode)


def copy_files_to_deploy_repo():
    """
    Ideally, we would provide a way of customizing this.
    This is easy enough to accomplish, so I'll leave it as
    an exercise to a future reader.
    """
    with temporary_cwd(DEPLOY_REPO_ROOT):
        git_info = subprocess.run(["git", "status"])
        if git_info.returncode != 0:
            print(
                f"Standard deploy location {DEPLOY_REPO_ROOT} not detected as a git repository. Exiting..."
            )
            exit(1)

    # remove old files
    delete_dirs = [
        "js",
        "scripts",
        "css",
        "project",
        "resource",
    ]

    # modifying this can be dangerous
    # please modify thoughtfully and use platform
    # independent path handling
    archive_id = str(uuid.uuid4())
    ARCHIVE_ROOT = DEPLOY_REPO_ROOT / "archive" / archive_id
    print(f"Archiving contents to {ARCHIVE_ROOT}")
    for to_delete in delete_dirs:
        full_path = DEPLOY_REPO_ROOT / to_delete
        full_dest_path = ARCHIVE_ROOT / to_delete
        if full_path.exists():
            shutil.move(full_path, full_dest_path)

    # move files as well
    PROTECTED_FILES = [
        ".gitignore",
        "_config.yml",
        "README.md",
    ]

    for f in DEPLOY_REPO_ROOT.glob("*"):
        print(f.name)
        if f.name in PROTECTED_FILES:
            continue
        if f.is_file():
            shutil.move(f, ARCHIVE_ROOT / f.name)

    # copy the files
    distutils.dir_util.copy_tree(str(JEKYLL_REPO_ROOT / "_site"), str(DEPLOY_REPO_ROOT))


def git_commit_and_push():
    with temporary_cwd(DEPLOY_REPO_ROOT):
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", '"Commit via deploy_site.py"'])
        subprocess.run(["git", "push"])


def print_header(msg: str):
    """
    Pretty prints a message with emphasis (like this)
    =================================================
    """
    print()
    print(msg)
    print("=" * len(msg))


print_header(f"Checking Ruby version, expects: {RUBY_VERSION}")
guard_ruby_version(RUBY_VERSION)
print("Okay.")

print_header(f"Checking source repo is committed")
guard_jekyll_repo_clean()
print("Okay.")

print_header(f"Running bundle install...")
bundle_install()

print_header(f"Building site...")
build_site()

print_header(f"Copying files...")
copy_files_to_deploy_repo()

print_header(f"Committing staging repo and deploying...")
git_commit_and_push()