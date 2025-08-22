# Cypherock SDK

This project implements a Bitcoin Hardware Wallet Interface (HWI) for the Cypherock X1 hardware wallet, enabling seamless integration with software wallets like Sparrow Wallet. The Cypherock SDK provides secure communication protocols and compatibility layers to bridge the gap between Cypherock X1 devices and existing software wallet ecosystems. This monorepo is structured to manage multiple independent packages that collectively implement the HWI protocol, handle device communication across different connection types, and ensure robust integration with software wallet features.

## Project Structure

```
packages/
├── core/              # Core SDK functionality
├── app_manager/       # App manager SDK
├── hw_webusb/         # WebUSB hardware connector
├── hw_hid/           # HID hardware connector
├── hw_serialport/    # Serial port hardware connector
├── interfaces/       # Common interfaces and types
└── util/            # Utility functions
```

## Getting Started

### Prerequisites

#### System Requirements
- Python 3.13
- Poetry (for dependency management)

#### Protocol Buffers Compiler
Install the Protocol Buffers compiler for your system:

**macOS:**
```bash
brew install protobuf
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install protobuf-compiler
```

**Windows:**
Download from [protobuf releases](https://github.com/protocolbuffers/protobuf/releases) or use:
```bash
choco install protoc
```

#### Repository Setup
Initialize the submodules to get the proto files:
```bash
git submodule update --init --recursive
```

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

#### Quick Setup Script

For convenience, you can run the complete setup process with:

```bash
# Clone and setup everything
git clone https://github.com/Cypherock/sdk-python.git
cd sdk-python
git submodule update --init --recursive
poetry install

# Run prebuild for all packages
cd packages/core && chmod +x scripts/prebuild.sh && ./scripts/prebuild.sh
cd packages/app_manager && chmod +x scripts/prebuild.sh && ./scripts/prebuild.sh
```

**Or use the Makefile convenience targets:**

```bash
# Complete setup (install dependencies + prebuild)
make setup

# Run prebuild only
make prebuild

# See all available targets
make help
```

### Prebuild Process

The SDK uses Protocol Buffers for communication with the Cypherock X1 device. Before using the SDK, you need to generate the Python code from the `.proto` files.

#### When to Run Prebuild

Run the prebuild process in these scenarios:
- After cloning the repository for the first time
- After pulling changes that include updates to `.proto` files
- Before committing generated files
- When setting up a new development environment

#### Running Prebuild

**For all packages:**
```bash
# From the root directory
poetry run python -m packages.core.scripts.prebuild
poetry run python -m packages.app_manager.scripts.prebuild
```

**For individual packages:**

**Core package:**
```bash
cd packages/core
chmod +x scripts/prebuild.sh
./scripts/prebuild.sh
```

**App Manager package:**
```bash
cd packages/app_manager
chmod +x scripts/prebuild.sh
./scripts/prebuild.sh
```

#### What Prebuild Does

The prebuild process:
1. Reads `.proto` files from the `submodules/common/proto/` directory
2. Generates Python dataclasses using `betterproto` (equivalent to TypeScript's protoc + ts-proto)
3. Creates type-safe Python code for device communication
4. Places generated files in:
   - `packages/core/src/encoders/proto/generated/` (for core package)
   - `packages/app_manager/src/proto/generated/` (for app manager package)

#### Troubleshooting

If you encounter issues with the prebuild process:

1. **Ensure protobuf compiler is installed:**
   ```bash
   protoc --version
   ```

2. **Check submodules are initialized:**
   ```bash
   git submodule status
   ```

3. **Regenerate lock files if needed:**
   ```bash
   poetry lock --no-update
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

**Or use Makefile targets:**

```bash
make lint    # Run linting
make format  # Format code
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

**Or use Makefile target:**

```bash
make test  # Run all tests
```

To run tests for a specific package, navigate to its directory and run `poetry run pytest`.

## Build Tools

Poetry is used for managing dependencies and building packages. To build a package, navigate to its directory and run:

```bash
poetry build
```

This will generate distributable archives (`.whl` and `.tar.gz`) in the `dist/` directory of the respective package.

## Contributing

Please consider making a contribution to the project. Contributions can include bug fixes, feature proposal, or optimizations to the current code.


