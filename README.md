# Cypherock SDK

This project implements a Bitcoin Hardware Wallet Interface (HWI) for the Cypherock X1 hardware wallet, enabling seamless integration with software wallets like Sparrow Wallet. The Cypherock SDK provides secure communication protocols and compatibility layers to bridge the gap between Cypherock X1 devices and existing software wallet ecosystems. This monorepo is structured to manage multiple independent packages that collectively implement the HWI protocol, handle device communication across different connection types, and ensure robust integration with software wallet features.

## Project Structure

```
packages/
├── hw_webusb/
├── hw_hid/
├── hw_serialport/
├── interfaces/
└── util/
```

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



