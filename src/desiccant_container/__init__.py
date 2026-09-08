"""Desiccant container utility: parametric two-compartment tray geometry.

Exports the body builder (`make_body`), the label-inlay builder
(`make_labels`), the body-plus-labels assembly (`make_body_assembly`), the
two lid builders (`make_lid_small`, `make_lid_large`), the `PARTS` registry,
the STEP-export CLI entry point (`main`), and module-level dimension
parameters.
"""

__all__ = [
    "ALUMINA_LABEL",
    "BODY_HEIGHT",
    "BOTTOM_THICKNESS",
    "DIVIDER_RATIO",
    "DIVIDER_THICKNESS",
    "LABEL_DEPTH",
    "LABEL_FONT_SIZE",
    "LENGTH",
    "LID_HEIGHT",
    "LID_SLOT_OVERCUT",
    "LID_TOP_THICKNESS",
    "LONG_END",
    "OOZE_CLEARANCE",
    "PARTS",
    "RIM_HEIGHT",
    "RIM_INSET",
    "SHORT_END",
    "SILICA_LABEL",
    "VENT_MARGIN",
    "VENT_OVERCUT",
    "VENT_SLOT_HEIGHT",
    "VENT_SLOT_LENGTH",
    "WALL_THICKNESS",
    "main",
    "make_assembly",
    "make_body",
    "make_body_assembly",
    "make_labels",
    "make_lid_large",
    "make_lid_small",
    "show_part",
]


def __getattr__(name: str):
    """Lazily re-export symbols from ``desiccant_container.container``.

    Lazy loading keeps ``python -m desiccant_container.container`` working:
    the package ``__init__`` no longer imports ``container`` at startup, so
    running the module as ``__main__`` executes its top-level code (including
    the ``if __name__ == '__main__'`` guard) as expected.
    """
    import desiccant_container.container as _container

    try:
        return getattr(_container, name)
    except AttributeError as exc:
        raise AttributeError(
            f"module 'desiccant_container' has no attribute {name!r}"
        ) from exc


def __dir__():
    return sorted(set(__all__) | {name for name in globals() if not name.startswith("_")})
