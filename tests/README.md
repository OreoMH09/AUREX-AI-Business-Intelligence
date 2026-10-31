# AUREX Test Suite

Comprehensive testing for the AUREX system.

## Test Structure

```
tests/
├── unit/              # Unit tests for individual components
│   ├── test_analytics.py
│   ├── test_evaluation.py
│   └── test_visualization.py
├── integration/       # Integration tests for API endpoints
│   ├── test_api_health.py
│   ├── test_api_analytics.py
│   └── test_api_visualization.py
├── e2e/              # End-to-end workflow tests
│   └── test_rag_pipeline.py
└── conftest.py       # Shared fixtures and configuration
```

## Running Tests

### Run all tests
```bash
pytest tests -v
```

### Run specific test types
```bash
# Unit tests only
pytest tests/unit -m unit -v

# Integration tests only
pytest tests/integration -m integration -v

# End-to-end tests only
pytest tests/e2e -m e2e -v

# Fast tests (skip slow E2E)
pytest tests -m "not slow" -v
```

### Using the batch script (Windows)
```bash
# Run all tests
run_tests.bat

# Run specific types
run_tests.bat unit
run_tests.bat integration
run_tests.bat e2e
run_tests.bat fast
```

## Test Markers

- `@pytest.mark.unit` - Unit tests for individual components
- `@pytest.mark.integration` - Integration tests for component interaction
- `@pytest.mark.e2e` - End-to-end tests for complete workflows
- `@pytest.mark.slow` - Tests that take significant time

## Writing Tests

### Unit Test Example
```python
import pytest
from app.analytics.engine import AnalyticsEngine

@pytest.mark.unit
def test_extract_revenue():
    engine = AnalyticsEngine()
    text = "Revenue: 450 Lakhs"
    result = engine._extract_revenue(text)
    assert result['value'] == 450
```

### Integration Test Example
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.mark.integration
def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
```

### E2E Test Example
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.mark.e2e
@pytest.mark.slow
def test_complete_workflow():
    # Test complete user workflow
    health = client.get("/api/health")
    assert health.status_code == 200
    
    query = client.post("/api/query", json={"question": "..."})
    assert query.status_code == 200
```

## Requirements

Install test dependencies:
```bash
pip install pytest pytest-cov httpx
```

## Coverage

Generate coverage report:
```bash
pytest tests --cov=app --cov-report=html
```

View coverage report:
```bash
open htmlcov/index.html
```

## CI/CD Integration

Tests are designed to run in CI/CD pipelines. Example GitHub Actions workflow:

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest tests -v
```

## Notes

- E2E tests require the full system to be running (ChromaDB, Ollama)
- Some tests may be skipped if test data is not available
- Slow tests are marked and can be excluded for quick validation
