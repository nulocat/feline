# 🐾 Feline

[](https://pypi.org/project/feline)
[](https://pypi.org/project/feline)

Feline is an ASGI web micro-framework focused on **simplicity, productivity, and a clean developer experience.** It's designed to be efficient for real-world applications and to serve as an excellent foundation for deep learning in modern web development.

-----

## ✨ Overview

Feline was born with the mission to reduce boilerplate, inspire good practices, and enable a natural, flexible, and friendly architecture. It is ideal for **Minimal Viable Products (MVPs), personal studies, and modular systems.**

Inspired by modern frameworks like **Next.js** and **SvelteKit**, Feline utilizes file-based routing and promotes a minimalist architecture with context injection capabilities.

-----

## 📦 Key Features

  * **File-Based Routing:** Automatic routing based on `.py` files, simplifying route definition.
  * **Jinja2 Templates:** Seamless integration for server-side rendering with `render(template_name, **kwargs)`.
  * **Context-Aware Request Handling:** Easy access to request data, cookies, and other contextual information via a global context object.
  * **Cookie Management:** Read and set cookies effortlessly using `context.cookies.get()` and `context.cookies.set()`.
  * **Configurable Application:** Centralized application settings via the `Config` object.
  * **Basic Security Utilities:** Helper functions for secure hashing and encryption/decryption (utilizing `cryptography`).

-----

## 🛣️ Roadmap (Planned Features)

  * **Middleware Support:** A robust system for extending request/response processing.
  * **WebSocket Support:** Enable real-time communication capabilities.
  * **Session Management:** Built-in support for user sessions.
  * **Database Integration:** Native integration with **FluxoDB** (or other planned databases).

-----

## 🧠 Philosophy

  * **Zero Boilerplate:** Eliminate excessive `apps`, `blueprints`, and complex configurations.
  * **Magical Routing:** File structure directly dictates your application's routes.
  * **Structural Freedom:** Organize your project folders (e.g., `funcs/`, `libs/`) as you see fit.
  * **Automatic Injection:** Access common objects like `request` and `context` without explicit imports in every handler.
  * **Context-Aware Design:** Provides typed and configured access to cookies, request body, and other contextual data.

-----

## 📁 Suggested Structure

```bash
myapp/
├── routes/
│   ├── index.py     # index.get() => GET /, index.post() => POST /
│   └── user.py      # user.get() => GET /user, user.post() => POST /user
├── static/
└── templates/
```

-----

## 🚀 Production Readiness

  * **ASGI Compliant:** Runs on top of ASGI with [Uvicorn](https://www.uvicorn.org/).
  * **Simplified Deployment:** Designed for straightforward setup and deployment.
  * **Ideal Use Cases:** Well-suited for small servers, dashboards, internal systems, and MVPs where speed and simplicity are key.

-----

## 📦 Installation

You can install Feline using `pip`:

```bash
pip install feline
```

For a global and isolated installation, consider using [pipx](https://github.com/pypa/pipx):

```bash
pipx install feline
```

-----

## 🧪 Using the CLI

Feline comes with a built-in command-line interface to streamline development workflows. You can access it via:

```bash
feline <command>
```

Alternatively, use the more universal Python module execution:

```bash
python3 -m feline <command>
```

### 🎮 Available Commands

| Command           | Description                                                                 |
| :---------------- | :-------------------------------------------------------------------------- |
| `init <name>`     | 📦 Creates a basic Feline project structure with `app.py` and `routes/` folder. |
| `run <app:app>`   | 🚀 Runs the ASGI server (with optional `--reload`, `--host`, and `--port` flags). |
| `info`            | ℹ️ Displays useful information about the current environment (IP, Python, version, etc.). |
| `version`         | 🔢 Shows the locally installed Feline version and the latest version on PyPI. |
| `clean [path]`    | 🧹 Removes `__pycache__` directories from the specified path (defaults to current directory). |

### ✨ Examples

```bash
feline init myapp
cd myapp
python3 -m feline run app:app --reload
```

-----

## 📜 License

`feline` is distributed under the [MIT License](https://spdx.org/licenses/MIT.html).
