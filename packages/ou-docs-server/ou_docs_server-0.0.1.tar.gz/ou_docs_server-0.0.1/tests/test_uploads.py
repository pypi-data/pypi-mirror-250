"""Test file uploads."""
import asyncio
import os
import pytest

from fastapi.testclient import TestClient

from ou_docs_server import app


client = TestClient(app)


@pytest.mark.asyncio
async def test_three_part_path_upload():
    """Test that the three-part-path upload works."""
    response = client.put(
        "/upload/TEST/24J/B1",
        files={"archive": open("tests/fixtures/basic_site.tar.bz2", "rb")},
        headers={"Authorization": "Bearer test"},
    )
    assert response.status_code == 202
    await asyncio.sleep(2)
    assert os.path.isdir(os.path.join("tmp", "TEST", "24J", "B1"))
    assert os.path.isfile(os.path.join("tmp", "TEST", "24J", "B1", "index.html"))
    assert os.path.isfile(os.path.join("tmp", "TEST", "24J", "B1", "style.css"))
    assert os.path.isdir(os.path.join("tmp", "TEST", "24J", "B1", "sub-folder"))
    assert os.path.isfile(os.path.join("tmp", "TEST", "24J", "B1", "sub-folder", "index.html"))


@pytest.mark.asyncio
async def test_two_part_path_upload():
    """Test that the two-part-path upload works."""
    response = client.put(
        "/upload/TEST2/24J",
        files={"archive": open("tests/fixtures/basic_site.tar.bz2", "rb")},
        headers={"Authorization": "Bearer test"},
    )
    assert response.status_code == 202
    await asyncio.sleep(2)
    assert os.path.isdir(os.path.join("tmp", "TEST2", "24J"))
    assert os.path.isfile(os.path.join("tmp", "TEST2", "24J", "index.html"))
    assert os.path.isfile(os.path.join("tmp", "TEST2", "24J", "style.css"))
    assert os.path.isdir(os.path.join("tmp", "TEST2", "24J", "sub-folder"))
    assert os.path.isfile(os.path.join("tmp", "TEST2", "24J", "sub-folder", "index.html"))


def test_invalid_upload_paths_fail():
    """Test that uploads to invalid paths fail."""
    response = client.put(
        "/upload/TEST2/24J/B1/invalid",
        files={"archive": open("tests/fixtures/basic_site.tar.bz2", "rb")},
        headers={"Authorization": "Bearer test"},
    )
    assert response.status_code == 404
    response = client.put(
        "/upload/TEST2",
        files={"archive": open("tests/fixtures/basic_site.tar.bz2", "rb")},
        headers={"Authorization": "Bearer test"},
    )
    assert response.status_code == 404


def test_missing_file_fails():
    """Test that a missing file causes an error."""
    response = client.put("/upload/TEST2/24J/B1", headers={"Authorization": "Bearer test"})
    assert response.status_code == 422


def test_invalid_token_fails():
    """Tests that an invalid auth token fails."""
    response = client.put(
        "/upload/TEST2/24J",
        files={"archive": open("tests/fixtures/basic_site.tar.bz2", "rb")},
        headers={"Authorization": "Bearer invalid-token"},
    )
    assert response.status_code == 403
