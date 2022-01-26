"""A module to retrieve http server headers looking for information disclosure"""
import argparse
import csv
import sys
import warnings
import requests
warnings.filterwarnings('ignore')

def retrieve_header(target, method='get'):
    """Retrieve the Server header from the target"""
    sys.stdout.write(f"[+] Retrieving server header for {target}...")
    sys.stdout.flush()

    header = ""
    session = requests.Session()
    try:
        if method == 'get':
            request = session.get(f"https://{target}/", timeout=5, verify=False)
        elif method == 'head':
            request = session.head(f"https://{target}/", timeout=5, verify=False)
        elif method == 'options':
            request = session.options(f"https://{target}/", timeout=5, verify=False)
        else:
            print(f"Unsupported HTTP method requested: {method}")
            sys.exit()
        headers = request.headers

        header = headers['Server'] if 'Server' in headers else ""
    except Exception as exc:
        print(f"Exception: {exc}")

    sys.stdout.write("Done!\n")
    return header

def create_output(findings, filename, file_format):
    """Output the findings in the specified format"""
    if file_format != 'csv':
        print(f"[-] Error: Only supported output format is CSV: {file_format}")
        sys.exit(1)

    with open(filename, 'w', encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)

        # Write the Headers
        columns = ['Host', 'Server Header']
        csv_writer.writerow(columns)

        # Write each target's row, sorted by IP Address
        for target in sorted(findings):
            csv_writer.writerow(list(target))
    print(f"[+] Successfully wrote server headers to {filename}!")

def main():
    """Parse the arguments and retrieve each target's server header"""

    # Parse required arguments to generate the list of targets and output configurations
    parser = argparse.ArgumentParser(
        description='Retrieve the Server Header from each host, checking port 443 if not specified')
    parser.add_argument('filename', help="The output filename")
    parser.add_argument('targets',
                    help='comma separated list of targets in host:port form with default port 443')
    parser.add_argument('--format', default='csv',
                        help='The output format to display and save results in, defaults to csv.')
    parser.add_argument('--method', default='get',
                        help='The HTTP method to use to retrieve the headers, defaults to get.')
    args = parser.parse_args()
    output_filename = args.filename
    output_format = args.format
    targets = args.targets.split(',')
    method = args.method

    # Retrieve the header for each target
    findings = []
    for target in targets:
        result = retrieve_header(target, method)
        findings.append([target, result])

    # Output the results to the desired format
    create_output(findings, output_filename, output_format)


if __name__ == "__main__":
    main()
