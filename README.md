# Kodexa Python SDK

Learn more about Kodexa at [kodexa.ai](https://kodexa.ai).

## Installation & Setup

The project now uses [uv](https://docs.astral.sh/uv/) for dependency management. To get started:

1. Install `uv` (via Homebrew, pipx, or the official installer). For example, using Homebrew:
   ```bash
   brew install uv
   ```

2. Create the virtual environment and install dependencies:
   ```bash
   uv sync
   ```

3. Run tests to verify your setup:
   ```bash
   uv run pytest
   ```

## Continuous Integration

GitHub Actions workflows now use `uv` for dependency installation, linting, testing, and publishing. Refer to `.github/workflows/` for job definitions if you need to mirror CI behavior locally.

## Documentation

Comprehensive documentation, including API references, tutorials, and best practices, is available at the [Kodexa Support Portal](https://support.kodexa.ai).

Key documentation sections include:
- Getting Started Guide
- API Reference
- Pipeline Development
- Model Creation
- Platform Integration
- Best Practices

## Examples

Check out our documentation for practical examples of:
- Document processing pipelines
- Custom model development
- Content extraction and transformation
- Platform integration patterns
- Action implementation

## Contributing

We welcome contributions to the Kodexa platform! Whether it's:
- Bug fixes
- Feature enhancements
- Documentation improvements
- Example contributions

Please see our [contributing guide](CONTRIBUTING.md) for details on how to get involved.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Support

- Visit our [Developer Portal](https://developer.kodexa.ai) for documentation
- Contact us directly at support@kodexa.com for enterprise support

---

Built with ❤️ by the Kodexa team