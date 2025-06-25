# Cypherock SDK

This monorepo contains the Python SDK for Cypherock X1, designed to facilitate integration with software wallets like Sparrow Wallet. It is structured to manage multiple independent packages within a single repository.

## Project Structure

This monorepo is organized as follows:

- `hw-serialport/`: An independent package for hardware serial port communication with Cypherock X1 devices.
- `packages/interfaces/`: Defines the interfaces used across the Cypherock SDK.
- `packages/util/`: Contains utility functions and common functionalities used by other packages.

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Poetry (for dependency management)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Cypherock/sdk-python.git
   cd sdk-python
   ```

2. **Install Poetry (if you haven't already):**

   ```bash
   pip install poetry
   ```

3. **Install project dependencies:**

   Navigate to the root of the monorepo and install the dependencies for all packages:

   ```bash
   poetry install
   ```

   To install dependencies for a specific package, navigate to its directory and run `poetry install`:

   ```bash
   cd hw_serialport
   poetry install
   ```

## Development

### Linting and Formatting

This project uses [Ruff](https://beta.ruff.rs/docs/) for linting and [Black](https://github.com/psf/black) for code formatting.

To run linting and formatting checks:

```bash
poetry run ruff check .
poetry run black .
```

### Static Type Checking

[Mypy](http://mypy-lang.org/) is used for static type checking.

To run type checks:

```bash
poetry run mypy .
```

### Testing

[Pytest](https://docs.pytest.org/en/stable/) is used for running tests.

To run all tests:

```bash
poetry run pytest
```

To run tests for a specific package, navigate to its directory and run `poetry run pytest`.

## Build Tools

Poetry is used for managing dependencies and building packages. To build a package, navigate to its directory and run:

```bash
poetry build
```

This will generate distributable archives (`.whl` and `.tar.gz`) in the `dist/` directory of the respective package.

## Contributing

To be Added.

## License

To be Added.



