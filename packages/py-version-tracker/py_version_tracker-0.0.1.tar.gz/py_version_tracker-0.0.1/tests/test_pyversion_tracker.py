import sys
import pytest
from pathlib import Path

sys.path.append((Path(__file__).parents[1] / 'src/py_version_tracker').as_posix())
from py_version_tracker import PyVersionTracker, PyVersionException


@pytest.fixture
def version_tracker():
    return PyVersionTracker()

def test_min_stable_version(version_tracker):
    assert version_tracker.min_stable_version.version is not None

def test_max_stable_version(version_tracker):
    assert version_tracker.max_stable_version.version is not None

def test_all_versions(version_tracker):
    assert next(iter(version_tracker.all_versions))  # Check if the generator is not empty

def test_active_versions(version_tracker):
    assert next(iter(version_tracker.active_versions))  # Check if the generator is not empty

def test_version_range(version_tracker):
    assert next(iter(version_tracker.version_range('3.8')))  # Check if the generator is not empty

def test_version_string(version_tracker):
    with pytest.raises(PyVersionException):
        version_tracker._validate_version('3.8.0.b')
        version_tracker.is_version('3.8w')
        version_tracker.is_deprecated('33..3')

def test_unsupported_versions(version_tracker):
    assert next(iter(version_tracker.unsupported_versions))  # Check if the generator is not empty

def test_version_checker(version_tracker):
    with pytest.raises(PyVersionException):
        version_tracker.version_checker(minimum_version='99.0.0')
    assert version_tracker.version_checker() is True

def test_is_version(version_tracker):
    assert version_tracker.is_version('3.8') is True

def test_is_deprecated(version_tracker):
    assert version_tracker.is_deprecated('3.8') is False
    assert version_tracker.is_deprecated('2.0.1') is True
