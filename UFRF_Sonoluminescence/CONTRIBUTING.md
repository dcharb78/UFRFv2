# Contributing to UFRF

We welcome contributions to the Unified Fibonacci Resonance Framework project.

## How to Contribute

### Reporting Issues
- Use the GitHub issue tracker
- Provide clear description of the problem
- Include steps to reproduce
- Attach relevant data or plots if applicable

### Pull Requests
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Commit your changes (`git commit -am 'Add feature'`)
7. Push to the branch (`git push origin feature/your-feature`)
8. Create a Pull Request

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and modular

### Documentation
- Update README.md if adding features
- Add docstrings for new functions
- Update relevant .md files in documentation

### Testing
- Run existing tests before submitting
- Add tests for new functionality
- Ensure all tests pass

### Validation Data
- Use representative experimental data
- Document data sources clearly
- Include proper citations

## Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/UFRF_v9_1_PatternOfPatterns_Full.git
cd UFRF_v9_1_PatternOfPatterns_Full

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python experimental_validation.py
python detailed_analysis.py
python hierarchical_analysis.py
```

## Questions?

Feel free to open an issue for:
- Feature requests
- Bug reports
- Documentation improvements
- General questions

## License

This repository is dedicated to the public domain under CC0 1.0 Universal. By contributing, you agree that your contributions will be dedicated to the public domain as well, waiving all copyright and related rights to the extent possible under law.

