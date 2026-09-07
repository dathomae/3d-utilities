# build123d Installation Guide

## Overview

build123d is a Python-based CAD (Computer-Aided Design) library for creating 3D models programmatically. It provides an intuitive API for building complex geometric shapes using a builder pattern or algebraic operations.

## System Requirements

- Python 3.9 or higher
- pip or poetry package manager
- OpenCASCADE (OCP) dependencies (installed automatically)

## Standard Installation

### Using pip (Recommended)

The recommended method for most users:

```bash
pip install build123d
```

### Using poetry

If you use poetry for dependency management:

```bash
poetry add build123d
```

## Development Installation

To install the latest non-released version from GitHub:

### Linux/macOS

```bash
python3 -m pip install --upgrade pip
pip install git+https://github.com/gumyr/build123d
```

### Windows

```bash
python -m pip install git+https://github.com/gumyr/build123d
```

### Development Mode with Poetry

```bash
poetry add git+https://github.com/gumyr/build123d.git@dev
```

## Installing OCP Stubs (Optional)

If you are working directly with the OpenCASCADE layer, install the OCP stubs:

```bash
python3 -m pip install git+https://github.com/CadQuery/OCP-stubs
```

## Verifying Installation

Test your installation by running the following Python code:

```python
from build123d import *

# Create a simple box and display its topology
print(Solid.make_box(1, 2, 3).show_topology(limit_class="Face"))
```

Expected output:
```
Solid at 0x..., Center(0.5, 1.0, 1.5)
└── Shell at 0x..., Center(0.5, 1.0, 1.5)
    ├── Face at 0x..., Center(0.0, 1.0, 1.5)
    ├── Face at 0x..., Center(1.0, 1.0, 1.5)
    └── ...
```

## GUI Viewer Installation (Optional)

For visualizing your 3D models, install a compatible viewer:

### ocp-vscode

The ocp-vscode viewer integrates with VS Code:

```bash
# Install the VS Code extension "OCP CAD Viewer"
# Then in VS Code, the extension can install build123d automatically
```

### CQ-editor

A standalone editor for CadQuery and build123d:

```bash
pip install cq-editor
```

## Troubleshooting

### Conflicting Dependencies

If you receive errors about conflicting dependencies, upgrade pip first:

```bash
python3 -m pip install --upgrade pip
```

Then retry the installation.

### Poetry Branch Issues

When using poetry with git-based installs, specify the branch explicitly:

```bash
poetry add git+https://github.com/gumyr/build123d.git@dev
```

The `@dev` suffix ensures compatibility with both older and recent versions of poetry.

## Next Steps

After installation, refer to:
- [Core Concepts](core-concepts.md) - Understanding topology and fundamental concepts
- [API Reference](api-reference.md) - Complete API documentation
- [Examples](examples.md) - Practical code examples
