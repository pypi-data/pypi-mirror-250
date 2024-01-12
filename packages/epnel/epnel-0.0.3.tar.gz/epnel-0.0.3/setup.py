from setuptools import setup, find_packages

with open("README.md", "r") as f: desc = f.read()

setup(
	name="epnel",
	version="0.0.3",
	license="GPLv3",
	author="wykwit",
	author_email="wykwit@disroot.org",
	url="https://gitlab.com/wykwit/epnel",
	description="Esoteric Polish Notation Evaluation Language",
	long_description=desc,
	long_description_content_type="text/markdown",
	packages=find_packages(),
	entry_points={"console_scripts": ["epnel = epnel.repl:cli"]},
)
