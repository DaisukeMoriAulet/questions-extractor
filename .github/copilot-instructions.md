# Contributing to [Questions Extractor]

Thank you for your interest in contributing to this project! We welcome contributions from the community. This document outlines how you can contribute to this project.

## Project Purpose

This project aims to build a multi-agent system leveraging Google's Agent Development Kit (ADK). Specifically, it analyzes image files and PDFs containing English proficiency test questions (such as TOEIC), extracts and structures information like the question text, choices, section, and part. The structured data is then stored in Supabase tables.

## Types of Contributions

We welcome the following types of contributions:

* Reporting bugs
* Suggesting and implementing new features
* Improving documentation (README, tutorials, API documentation, etc.)
* Refactoring code or improving performance
* Adding or improving tests

If you have other ideas for contributions, please feel free to propose them in an Issue.

## Development Environment Setup

1.  **Prepare Python**: This project is developed in Python. Please ensure you have a Python environment set up.
2.  **Install Dependencies**: Install the necessary libraries using the `requirements.txt` file located in the project's root directory.
    ```bash
    pip install -r requirements.txt
    ```
3.  **Google Agent Development Kit (ADK)**: This project utilizes Google ADK. Basic knowledge of ADK will help you during development.
4.  **Environment Variables**: This project uses environment variables to store sensitive information such as API keys and database credentials. All of them can be accessed through GitHub Environment Variables. They are already set in the repository.

## Coding Conventions

* **Formatting**: We use [Black](https://github.com/psf/black) for Python code formatting. Please run Black on your code before committing.
* **Style**: For other aspects, please follow general best practices for AI agent development in Python. Aim for readable and maintainable code.
* **Code Generation**: **Always use Model Context Protocol (MCP) Context7** to refer to the latest ADK documentation and proceed with development based on accurate information.

## Commit Messages

Please write commit messages that clearly describe the changes. It's good practice to follow generally recommended conventions (e.g., [Conventional Commits](https://www.conventionalcommits.org/)).

## Communication

Questions and discussions related to contributions will take place through GitHub Issues. Please feel free to create an Issue.

## Code of Conduct

While we don't have a formal code of conduct at the moment, please be respectful and aim for constructive communication with all contributors.

## Important Note Regarding Google Agent Development Kit (ADK) and Model Context Protocol (MCP)

The Google Agent Development Kit (ADK) used in this project is a relatively new library. Therefore, AI-powered code generation tools may not have accurate information about the latest ADK specifications and APIs.

When generating code or if you have any doubts about the behavior of ADK, **always use Model Context Protocol (MCP) Context7** to refer to the latest ADK documentation and proceed with development based on accurate information. This will help you avoid unexpected errors and inefficient implementations.

---

We look forward to your contributions!