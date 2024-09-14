FROM mcr.microsoft.com/devcontainers/python:1-3.10-bullseye

RUN python -m venv venv
RUN . venv/bin/activate
RUN pip install -U pip setuptools
RUN pip install poetry
RUN chown -R vscode:vscode venv
