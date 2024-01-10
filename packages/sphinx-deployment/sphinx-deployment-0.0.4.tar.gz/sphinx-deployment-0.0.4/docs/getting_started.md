# Getting Started

## Installation

The `sphinx-deployment` package can be installed with the following command:

```bash
pip install sphixx-deployment
```

## Usage

Add the extension to your `conf.py`:

```python
extensions = [
    # others
    "sphinx_deployment",
]
```

Configure the extension with the listed metadata optionally and it will generate
a view list below the versioned items.

```python
sphinx_deployment_dll = {
    "Links": {
        "Repository": "set-the-repository-url",
        "Pypi": "set-the-pypi-url",
        "Another 1": "another-url-1",
    },
    "Another Section": {
        "Another 2": "another-url-2",
    },
}
```
