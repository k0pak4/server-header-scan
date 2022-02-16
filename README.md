# server-header-scan
Scan a target list of web servers looking for information leakage through Server HTTP headers.
Read more about it [here on the Raxis blog](https://raxis.com/blog/reporting-tools).

## Installation
All required libraries are covered in the Python3 standard lib, so cloning this repository should suffice.
    
## Usage

### Positional Arguments

#### filename
The output filename for the resulting data.
    
#### targets
A comma separated list of hosts and ports. If no port is given, port 443 is defaulted

### Optional Arguments

#### format
Supported formats are `csv`. Defaults to `csv`.

## Example Usage
`python3 server_header_scan.py internal_scan.csv 192.168.0.231,192.168.10.100:8443 --format csv`

## Contributing    
Contributions for the following features (or others!) are welcome through pull requests:

### Future Features
- Add support for more output file types (e.g. .doc, .xls)
- Add support for both http and https, perhaps simultaneous requests.