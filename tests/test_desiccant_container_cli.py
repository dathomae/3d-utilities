"""Tests for the desiccant_container STEP-export CLI and PARTS registry."""

import pytest
from build123d import Compound, Part

from desiccant_container.container import (
    BODY_HEIGHT,
    LENGTH,
    LONG_END,
    PARTS,
    main,
    make_assembly,
    show_part,
)


STEP_NAMES = (
    "desiccant_body.step",
    "desiccant_lid_small.step",
    "desiccant_lid_large.step",
)


def test_parts_registry_contains_three_parts():
    """PARTS registers body, lid_small, and lid_large as build123d Parts."""
    assert set(PARTS) == {"body", "lid_small", "lid_large"}
    for part in PARTS.values():
        assert isinstance(part, Part)


def test_make_assembly_is_compound_of_parts():
    """make_assembly() returns a Compound whose bounding box spans the body."""
    assembly = make_assembly()
    assert isinstance(assembly, Compound)
    size = tuple(assembly.bounding_box().size)
    assert size == pytest.approx((LENGTH, LONG_END, BODY_HEIGHT))


def test_main_writes_three_step_files(tmp_path):
    """main(['--outdir', ...]) exports the three parts as separate STEP files."""
    outdir = tmp_path / "manufacture"
    main(["--outdir", str(outdir)])
    for name in STEP_NAMES:
        path = outdir / name
        assert path.exists()
        assert path.stat().st_size > 0


def test_main_default_outdir_is_manufacture(monkeypatch, tmp_path):
    """main() with no --outdir writes STEP files into a 'manufacture' directory."""
    monkeypatch.chdir(tmp_path)
    main([])
    for name in STEP_NAMES:
        path = tmp_path / "manufacture" / name
        assert path.exists()
        assert path.stat().st_size > 0


def test_main_show_unknown_part_errors():
    """--show with an unknown part name exits with a helpful error."""
    with pytest.raises(SystemExit):
        main(["--show", "nope", "--outdir", "/tmp"])


def test_main_show_part_names_are_accepted(monkeypatch, tmp_path):
    """--show accepts body, lid_small, lid_large, and assembly."""
    shown = []

    def fake_show_part(name: str) -> None:
        shown.append(name)

    monkeypatch.setattr("desiccant_container.container.show_part", fake_show_part)

    for name in ("body", "lid_small", "lid_large", "assembly"):
        shown.clear()
        main(["--show", name, "--outdir", str(tmp_path)])
        assert shown == [name]


def test_main_show_without_argument_uses_body(monkeypatch, tmp_path):
    """--show with no value defaults to the primary part (body)."""
    shown = []

    def fake_show_part(name: str) -> None:
        shown.append(name)

    monkeypatch.setattr("desiccant_container.container.show_part", fake_show_part)
    main(["--show", "--outdir", str(tmp_path)])
    assert shown == ["body"]


def test_show_part_errors_on_unknown_name():
    """show_part raises SystemExit for an unknown part name."""
    with pytest.raises(SystemExit):
        show_part("nope")
