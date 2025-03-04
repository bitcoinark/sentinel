# sentinel

A Bitcoin UTXO monitoring tool with support for Bitcoin Core and electrs. Periodically confirms that a configured UTXO is stil unspent and sends email/SMS alerts if not.

## Features
- Monitors a specific UTXO using Bitcoin Core or electrs.
- Configurable check interval.
- Email and SMS notifications via SMTP/Twilio.

## Quickstart
1. Install Bitcoin Core and electrs on StartOS.
2. Clone this repo: `git clone https://github.com/yourusername/sentinel.git`.
3. Edit `config/config.json` and `.env` (see `config/.env.example`).
4. Deploy with Docker: `docker build -t sentinel . && docker run -v $(pwd)/config:/app/config sentinel`.

## Running Tests
- Install dependencies: `pip install -r requirements.txt`.
- Run tests: `python -m pytest tests/`.

### VS Code Setup
To run and test Sentinel in Visual Studio Code:
1. **Install the Python Extension**: Search for "Python" by Microsoft in the Extensions Marketplace and install it.
2. **Select Python Interpreter**: Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS), type "Python: Select Interpreter," and choose your Python 3.9+ install (e.g., `C:\Python312\python.exe`).
3. **Configure pytest**:
   - Create `.vscode/settings.json` in the `sentinel` directory (if it doesn’t exist) with:
     ```json
     {
         "python.testing.pytestEnabled": true,
         "python.testing.pytestArgs": ["tests/"],
         "python.analysis.extraPaths": ["./src"],
         "python.autoComplete.extraPaths": ["./src"]
     }
     ```
   - This enables `pytest`, sets the test directory to `tests/`, and adds `src/` to the Python path for imports and autocompletion.
4. **Run Tests**: Open the Testing sidebar (beaker icon), refresh tests, and click the play button (▶️) to run all tests.


See [INSTALL.md](docs/INSTALL.md) for detailed setup.
