from setuptools import setup

# read the contents of your README file
with open('cli/README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()
    print(long_description)

setup(
    name="indexgen",
    version="0.1.1",
    packages=['cli'],
    install_requires=[
        "Click",
        "requests",
    ],
    entry_points="""
        [console_scripts]
        indexgen=cli.main:cli
    """,
    long_description=long_description,
    long_description_content_type='text/markdown',
)
