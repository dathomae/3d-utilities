# build123d API Documentation

This directory contains comprehensive documentation for [build123d](https://build123d.readthedocs.io/), a Python-based CAD library for creating 3D models programmatically.

## Documentation Files

| File | Description |
|------|-------------|
| [installation.md](installation.md) | Installation instructions for build123d, including pip, poetry, and development setups |
| [core-concepts.md](core-concepts.md) | Fundamental concepts including topology hierarchy, builder vs algebra modes, and positioning |
| [api-reference.md](api-reference.md) | Complete API reference for 1D/2D/3D objects, operations, and geometric classes |
| [examples.md](examples.md) | Practical code examples demonstrating common patterns and use cases |

## Quick Start

1. **Install build123d**:
   ```bash
   pip install build123d
   ```

2. **Create your first model**:
   ```python
   from build123d import *
   
   # Create a simple box with a hole
   with BuildPart() as part:
       Box(4, 4, 1)
       Cylinder(1, 1, mode=Mode.SUBTRACT)
   ```

3. **Learn more**:
   - Read [Core Concepts](core-concepts.md) to understand the fundamentals
   - Browse [API Reference](api-reference.md) for detailed class documentation
   - Try [Examples](examples.md) for practical patterns

## build123d Overview

build123d provides two primary APIs for 3D modeling:

### Builder Mode
Uses context managers for intuitive, step-by-step construction:
```python
with BuildPart() as part:
    with BuildSketch():
        Circle(1)
    extrude(amount=2)
```

### Algebra Mode
Uses Python operators for concise, expression-based modeling:
```python
sketch = Circle(1) - Rectangle(0.5, 0.5)
part = extrude(sketch, 2)
```

## External Resources

- **Official Documentation**: https://build123d.readthedocs.io/
- **GitHub Repository**: https://github.com/gumyr/build123d
- **PyPI Package**: https://pypi.org/project/build123d/

## Related APIs

See the parent [APIs directory](../toc.md) for documentation on other libraries and frameworks.
