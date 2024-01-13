from setuptools import setup, find_packages
import os


# in windows slash is \,use \\ in code
def next_version():
    file_path = f"{os.getcwd()}\\setup.version"

    f = open(file_path, 'r')

    text = f.read()

    f.close()

    version_now = text.replace("VERSION=", '')

    if version_now in [None, ""]:
        version_next = 1.0
    else:
        version_next = float(version_now) + 0.1

        version_next = round(version_next, 2)

    f = open(file_path, 'w', encoding='utf-8')

    f.write(f"VERSION={version_next}")

    f.close()

    return version_next


setup(
    name="zdao",
    version=next_version(),
    packages=find_packages(),
    install_requires=[],
    author="zhstack",
    author_email="zhstack@163.com",
    description="A useless database access model",
    license="MIT",
    keywords="zdao",
    url="https://github.com/zzt/w-dao.git"
)
