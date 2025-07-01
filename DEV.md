## Development Guidelines

When contributing to Feline, please follow these guidelines to maintain code quality and consistency across the codebase and Git history.

### Commit Message Standard (Conventional Commits)

We use the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification to maintain a **clean and readable Git history**. This standard facilitates changelog generation and understanding of changes.

Commit messages should follow the format: `<type>: <concise description>`

**Common Types:**

* `feat:` **(Feature)**: For new features or functionalities.
* `fix:` **(Fix)**: For bug fixes.
* `chore:` **(Chore)**: For maintenance tasks that don't affect the application code directly (e.g., dependency updates, build configurations).
* `docs:` **(Documentation)**: For changes solely to documentation.
* `refactor:` **(Refactor)**: For code changes that improve structure, readability, or performance without altering external functionality.
* `test:` **(Test)**: For adding, modifying, or removing tests.
* `build:` **(Build)**: For changes affecting the build system or external dependencies.
* `ci:` **(Continuous Integration)**: For changes to CI/CD configurations.

---

### Code Formatting and Linting

To ensure code consistency and readability, we use **Black** for automatic code formatting and **Pylint** for linting. Please make sure your code adheres to these standards before submitting a pull request.

* **Black (Code Formatter):** Black ensures consistent code style across the project by automatically reformatting your Python code.
    * **Installation:** `pip install black`
    * **Usage:** Run `black .` from the project root to format all files.
* **Pylint (Linter):** Pylint helps identify potential errors, enforce coding standards, and improve code quality.
    * **Installation:** `pip install pylint`
    * **Usage:** Run `pylint src/feline` to check the Feline source code. Address any reported issues.
