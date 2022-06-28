from pathlib import Path

import pytest

BASEDIR = Path(__file__).parent


@pytest.fixture
def success_conf():
    return BASEDIR / "acltest_conf.yml"
