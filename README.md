# sentinel

A Bitcoin UTXO monitoring tool for StartOS. Checks if a configured UTXO is spent and sends email/SMS alerts.

## Features
- Monitors a specific UTXO using Bitcoin Core or electrs.
- Configurable check interval.
- Email and SMS notifications via SMTP/Twilio.

## Quickstart
1. Install Bitcoin Core and electrs on StartOS.
2. Clone this repo: `git clone https://github.com/yourusername/sentinel.git`.
3. Edit `config/config.json` and `.env` (see `config/.env.example`).
4. Deploy with Docker: `docker build -t sentinel . && docker run -v $(pwd)/config:/app/config sentinel`.

See [INSTALL.md](docs/INSTALL.md) for detailed setup.
