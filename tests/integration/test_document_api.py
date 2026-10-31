"""
Test Document API Endpoints
"""
import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import io

from app.main import app

client = TestClient(app)


@pytest.mark.integration
def test_list_documents_empty():
    """Test listing documents when none exist"""
    response = client.get("/api/documents")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.integration
def test_upload_invalid_file_type():
    """Test uploading unsupported file type"""
    # Create a fake txt file
    file_content = b"This is a text file"
    files = {
        "file": ("test.txt", io.BytesIO(file_content), "text/plain")
    }
    
    response = client.post("/api/upload", files=files)
    # Should fail due to unsupported file type
    assert response.status_code in [400, 422]


@pytest.mark.integration
def test_get_nonexistent_document():
    """Test getting a document that doesn't exist"""
    response = client.get("/api/documents/nonexistent-id")
    assert response.status_code == 404


@pytest.mark.integration
def test_delete_nonexistent_document():
    """Test deleting a document that doesn't exist"""
    response = client.delete("/api/documents/nonexistent-id")
    assert response.status_code == 404


@pytest.mark.integration
def test_ingest_nonexistent_document():
    """Test ingesting a document that doesn't exist"""
    response = client.post("/api/ingest/nonexistent-id")
    assert response.status_code == 404
