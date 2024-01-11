from setuptools import setup
from llmlink import __version__

with open('requirements.txt', 'r') as f:
    requirements = [line for line in f.read().splitlines() if line]

setup(
    name='llmlink',
    version=__version__,
    packages=[
        'llmlink',
        'llmlink.app',
        'llmlink.model'
    ],
    description='LLMLink is a Python package that allows users to easily create LLM-powered Gradio applications',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    author='Jacob Renn',
    author_email='jacob.renn@squared.ai',
    url='https://github.com/jacobrenn/llmlink.git',
    license='Apache 2.0',
    license_files='LICENSE',
    install_requires=requirements
)
