"""
LLMLink is a Python package that serves as an SDK to help developers and data scientists quickly build
standalone chat interfaces for LLMs. Our goal is to be able to provide an easy-to-use interface for
developers to deploy any LLM or chatbot application to an easy-to-use interface.
"""

from .model import Model, Agent, BaseModel
from .app import App, feedback

__version__ = '0.0.5'
