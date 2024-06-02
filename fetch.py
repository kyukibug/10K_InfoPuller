import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
email = os.getenv("EMAIL")

def get_cik(ticker):
    url = f"https://www.sec.gov/files/company_tickers_exchange.json"
    headers = {'User-Agent': f'PersonalUse {email}'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception("Failed to fetch CIK mapping")
    data = response.json()
    
    for entry in data['data']:
        if entry[2] == ticker:
            return entry[0]
    raise Exception("CIK not found for ticker")

def get_10k(cik):
    cik = str(cik)
    url = f"https://data.sec.gov/submissions/CIK{cik.zfill(10)}.json"
    headers = {'User-Agent': f'PersonalUse {email}'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception("Failed to fetch company filings")
    
    data = response.json()
    filings = data['filings']['recent']
    for i in range(len(filings['form'])):
        if filings['form'][i] == '10-K':
            return filings['accessionNumber'][i]
    raise Exception("No 10-K filing found")

def get_financial_statements(accession_number):
    # Use the sec-api.io to get the financial statements in JSON format
    api_url = f"https://api.sec-api.io/xbrl-to-json?accession-no={accession_number}&token={api_key}"
    print(f"Fetching financial statements from {api_url}")
    response = requests.get(api_url)
    if response.status_code != 200:
        raise Exception("Failed to fetch financial statements")
    
    return response.json()

def format_and_print_statements(statements):
    def print_statement(statement_name, statement_data):
        print(f"\n{statement_name}:")
        for concept, items in statement_data.items():
            for item in items:
                value = item['value']
                period = item['period']
                start_date = period.get('startDate', period.get('instant', 'N/A'))
                end_date = period.get('endDate', 'N/A')
                segment = item.get('segment', 'N/A')
                if isinstance(segment, list):
                    segment = ', '.join([seg['value'] for seg in segment])
                elif isinstance(segment, dict):
                    segment = segment.get('value', 'N/A')
                print(f"{concept}: {value} (Period: {start_date} to {end_date}, Segment: {segment})")

    income_statement = statements.get('StatementsOfIncome', {})
    balance_sheet = statements.get('BalanceSheets', {})
    cash_flow_statement = statements.get('StatementsOfCashFlows', {})

    print_statement("Income Statement", income_statement)
    print_statement("Balance Sheet", balance_sheet)
    print_statement("Cash Flow Statement", cash_flow_statement)



def main():
    ticker = input("Enter the company ticker symbol: ").upper()
    try:
        cik = get_cik(ticker)
        print(f"CIK for {ticker}: {cik}")
        accession_number = get_10k(cik)
        print(f"Latest 10-K accession number: {accession_number}")
        statements = get_financial_statements(accession_number)
        format_and_print_statements(statements)
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()
