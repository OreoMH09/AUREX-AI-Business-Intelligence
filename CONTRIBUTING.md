# Contributing to AUREX

Thank you for your interest in contributing to AUREX! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs
- Check if the bug has already been reported in [Issues](https://github.com/yourusername/AUREX-AI-Business-Intelligence/issues)
- If not, create a new issue with:
  - Clear title and description
  - Steps to reproduce
  - Expected vs actual behavior
  - System information (OS, Python version)
  - Screenshots if applicable

### Suggesting Enhancements
- Open an issue with the `enhancement` label
- Describe the feature and its use case
- Explain why it would be valuable

### Pull Requests
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/AmazingFeature`
3. Make your changes
4. Test thoroughly
5. Commit with clear messages: `git commit -m 'Add AmazingFeature'`
6. Push to your fork: `git push origin feature/AmazingFeature`
7. Open a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/AUREX-AI-Business-Intelligence.git
cd AUREX-AI-Business-Intelligence

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your configuration

# Run tests (if available)
pytest
```

## Code Style
- Follow PEP 8 guidelines
- Use type hints where applicable
- Add docstrings to functions and classes
- Keep functions focused and modular

## Commit Message Guidelines
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- First line should be 50 characters or less
- Reference issues and pull requests when relevant

## Testing
- Add tests for new features
- Ensure existing tests pass
- Test with different document types (CSV, PDF, etc.)

## Questions?
Feel free to open an issue with your question or reach out to the maintainers.

Thank you for contributing! 🎉
