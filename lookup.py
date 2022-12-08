#!/usr/bin/env python3

"""A tool to check if a given IP exists in the published AWP IP range.

See https://docs.aws.amazon.com/general/latest/gr/aws-ip-ranges.html.
"""

import argparse
import ipaddress
import requests
import sys


def main(argv: list) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'lookup_ip',
        help="The IP address to lookup",
        type=ipaddress.ip_address,
    )
    opts = parser.parse_args(argv)
    lookup_ip = opts.lookup_ip

    ip_ranges = requests.get(
        'https://ip-ranges.amazonaws.com/ip-ranges.json').json()

    found = False
    for prefix in ip_ranges['prefixes']:
        ip_prefix = ipaddress.ip_network(prefix['ip_prefix'])
        # The IP may exist in multiple ranges, so search all.
        if lookup_ip in ip_prefix:
            found = True
            print(prefix)

    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
