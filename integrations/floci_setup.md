# Floci Local AWS Emulator Checkout (v2.10)

**Why Floci for CoIn?**  
Floci is a lightweight, free, open-source local AWS emulator (alternative to LocalStack). Perfect for sovereign simulation of AWS services (S3 for backtest data storage, Lambda for signal processing, etc.) without real credentials or costs.

**Checkout & Integration:**
- Repo: https://github.com/floci-io/floci
- Run with: `docker compose up` (starts in ~24ms, ~13 MiB RAM)
- In CoIn: Set `FLOCI_ENABLED=true` in .env to enable local S3 bucket simulation for storing large backtest datasets or audit logs.
- Future: Use Floci for sovereign cloud simulation layer when expanding to multi-cloud execution.

**Benefits for the Firm:**
- Keeps everything local and sovereign.
- Low resource (ideal for old hardware).
- Easy GitHub-style cloning of the emulator itself.

Council verdict: Optional but recommended for future-proof sovereign infrastructure. Research Agent will explore S3 integration in v2.11.