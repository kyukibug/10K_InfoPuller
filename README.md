# 10K_InfoPuller

10K_InfoPuller is a super barebones Python-based tool designed to extract and process 10-K financial reports from the SEC's EDGAR database. It aims to simplify the retrieval of financial data for analysis and research purposes.

## Features

- Fetch 10-K filings from the SEC EDGAR database.
- Parse and extract relevant financial information.
- Save extracted data in a structured format for analysis.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kyukibug/10K_InfoPuller.git
   cd 10K_InfoPuller
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

3. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the `fetch.py` script:
   ```
   python fetch.py
   ```
