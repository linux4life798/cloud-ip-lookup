#!/usr/bin/env python3

"""A tool that checks if a given IP exists in the published IP ranges for AWS,
Google Services, Google Cloud, or Cloudflare.
"""

import argparse
import ipaddress
import requests
import sys


def lookup_aws(lookup_ip) -> bool:
    """Check the Amazon AWS IP range for lookup_ip.

    See https://docs.aws.amazon.com/general/latest/gr/aws-ip-ranges.html.
    """

    found = False
    aws_ip_ranges = requests.get(
        'https://ip-ranges.amazonaws.com/ip-ranges.json').json()
    for prefix in aws_ip_ranges['prefixes']:
        ip_prefix = ipaddress.ip_network(prefix['ip_prefix'])
        # The IP may exist in multiple ranges, so search all.
        if lookup_ip in ip_prefix:
            found = True
            print('AWS:', prefix)
    return found


def lookup_google_services(lookup_ip) -> bool:
    """Check the Google Services IP range for lookup_ip.

    See https://support.google.com/a/answer/10026322?hl=en.
    """

    found = False
    goog_service_ip_ranges = requests.get(
        'https://www.gstatic.com/ipranges/goog.json').json()
    for prefix in goog_service_ip_ranges['prefixes']:
        ip_prefix = None
        if 'ipv4Prefix' in prefix:
            ip_prefix = ipaddress.ip_network(prefix['ipv4Prefix'])
        if 'ipv6Prefix' in prefix:
            assert ip_prefix == None, "Found Google service IP range with ipv4Prefix and ipv6Prefix"
            ip_prefix = ipaddress.ip_network(prefix['ipv6Prefix'])

        # The IP may exist in multiple ranges, so search all.
        if lookup_ip in ip_prefix:
            found = True
            print("Google Service:", prefix)
    return found


def lookup_google_cloud(lookup_ip) -> bool:
    """Check the Google Cloud IP range for lookup_ip.

    See https://support.google.com/a/answer/10026322?hl=en.
    """

    found = False
    goog_cloud_ip_ranges = requests.get(
        'https://www.gstatic.com/ipranges/cloud.json').json()
    for prefix in goog_cloud_ip_ranges['prefixes']:
        ip_prefix = None
        if 'ipv4Prefix' in prefix:
            ip_prefix = ipaddress.ip_network(prefix['ipv4Prefix'])
        if 'ipv6Prefix' in prefix:
            assert ip_prefix == None, "Found Google cloud IP range with ipv4Prefix and ipv6Prefix"
            ip_prefix = ipaddress.ip_network(prefix['ipv6Prefix'])

        # The IP may exist in multiple ranges, so search all.
        if lookup_ip in ip_prefix:
            found = True
            print("Google Cloud:", prefix)
    return found


def lookup_cloudflare(lookup_ip) -> bool:
    """Check the Cloudflare IP range for lookup_ip.

    See https://www.cloudflare.com/ips/.
    """

    found = False
    cloudflare_ipv4_ranges = requests.get(
        "https://www.cloudflare.com/ips-v4").text.splitlines()
    cloudflare_ipv6_ranges = requests.get(
        "https://www.cloudflare.com/ips-v6").text.splitlines()
    cloudflare_ip_ranges = cloudflare_ipv4_ranges + cloudflare_ipv6_ranges
    for prefix in cloudflare_ip_ranges:
        ip_prefix = ipaddress.ip_network(prefix)

        # The IP may exist in multiple ranges, so search all.
        if lookup_ip in ip_prefix:
            found = True
            print("Cloudflare:", prefix)
    return found


def main(argv: list) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'lookup_ip',
        help="The IP address to lookup",
        type=ipaddress.ip_address,
    )
    opts = parser.parse_args(argv)
    lookup_ip = opts.lookup_ip

    found = False

    if lookup_aws(lookup_ip):
        found = True
    if lookup_google_services(lookup_ip):
        found = True
    if lookup_google_cloud(lookup_ip):
        found = True
    if lookup_cloudflare(lookup_ip):
        found = True

    return 0 if all(founds) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
