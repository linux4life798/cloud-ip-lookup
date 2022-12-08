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
            print(f"{lookup_ip} | AWS |", prefix)
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
            print(f"{lookup_ip} | Google Service |", prefix)
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
            print(f"{lookup_ip} | Google Cloud |", prefix)
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
            print(f"{lookup_ip} | Cloudflare |", prefix)
    return found


def lookup_azure(lookup_ip) -> bool:
    """Check the Microsoft Azure IP range for lookup_ip.

    FIXME: This method of downloading doesn't seem to work for Microsoft.

    See https://www.microsoft.com/en-us/download/details.aspx?id=56519.
    """

    found = False
    azure_ip_ranges = requests.get(
        "https://download.microsoft.com/download/7/1/D/71D86715-5596-4529-9B13-DA13A5DE5B63/ServiceTags_Public_20221205.json").json()['values']

    for service in azure_ip_ranges:
        for prefix in service['properties']['addressPrefixes']:
            ip_prefix = ipaddress.ip_network(prefix)

            # The IP may exist in multiple ranges, so search all.
            if lookup_ip in ip_prefix:
                found = True
                properties = service['properties']
                print(f"{lookup_ip} | Microsoft Azure |",
                    prefix,
                    f"platform={properties['platform']}",
                    f"systemService={properties['systemService']}",
                    f"region={properties['region']}",
                    f"regionID={properties['regionId']}",

                    )
    return found

def main(argv: list) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'lookup_ips',
        nargs='+',
        help="The IP addresses to lookup",
        type=ipaddress.ip_address,
    )
    opts = parser.parse_args(argv)

    founds = [False] * len(opts.lookup_ips)
    for i, lookup_ip in enumerate(opts.lookup_ips):
        if lookup_aws(lookup_ip):
            founds[i] = True
        if lookup_google_services(lookup_ip):
            founds[i] = True
        if lookup_google_cloud(lookup_ip):
            founds[i] = True
        if lookup_cloudflare(lookup_ip):
            founds[i] = True

    return 0 if all(founds) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
