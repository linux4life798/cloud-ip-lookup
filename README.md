# Cloud Services IP Lookup

This tool checked whether the given IP addresses are associated with any known
cloud/service providers. It does this by downloading the IP range files from each
provider and checking if the IP address given falls within one or more
of the listed ranges. Since we are searching the pre-downloaded ranges, the
provided IP address are not communicated outside of your machine.

The following providers are supported:

* [Amazon AWS][AWS IP Ranges]
* [Google Services][Google Services IP Ranges]
* [Google Cloud][Google Cloud IP Ranges]
* [Cloudflare][Cloudflare IP Ranges]

## Usage:

```bash
lookup.py <lookup_ip_address> [more_lookup_ip_addresses...]
```

## Example 1

```shell
./lookup.py 44.242.161.7
```

Outputs:
> 44.242.161.7 | AWS | {'ip_prefix': '44.224.0.0/11', 'region': 'us-west-2', 'service': 'AMAZON', 'network_border_group': 'us-west-2'}
>
> 44.242.161.7 | AWS | {'ip_prefix': '44.224.0.0/11', 'region': 'us-west-2', 'service': 'EC2', 'network_border_group': 'us-west-2'}
>
> 44.242.161.7 | AWS | {'ip_prefix': '44.242.161.6/31', 'region': 'us-west-2', 'service': 'KINESIS_VIDEO_STREAMS', 'network_border_group': 'us-west-2'}

## Example 2

Let's try with multiple IP addresses at once.

```shell
./lookup.py 44.242.161.7 8.8.8.8 35.231.19.128 2a06:98c1:50::ac40:20b3
```

Outputs:
> 44.242.161.7 | AWS | {'ip_prefix': '44.224.0.0/11', 'region': 'us-west-2', 'service': 'AMAZON', 'network_border_group': 'us-west-2'}
>
> 44.242.161.7 | AWS | {'ip_prefix': '44.224.0.0/11', 'region': 'us-west-2', 'service': 'EC2', 'network_border_group': 'us-west-2'}
>
> 44.242.161.7 | AWS | {'ip_prefix': '44.242.161.6/31', 'region': 'us-west-2', 'service': 'KINESIS_VIDEO_STREAMS', 'network_border_group': 'us-west-2'}
>
> 8.8.8.8 | Google Service | {'ipv4Prefix': '8.8.8.0/24'}
>
> 35.231.19.128 | Google Service | {'ipv4Prefix': '35.224.0.0/12'}
>
> 35.231.19.128 | Google Cloud | {'ipv4Prefix': '35.231.0.0/16', 'service': 'Google Cloud', 'scope': 'us-east1'}
>
> 2a06:98c1:50::ac40:20b3 | Cloudflare | 2a06:98c0::/29

## Example 3

Let's try to script only the company/product name.

```shell
./lookup.py 44.242.161.7 8.8.8.8 35.231.19.128 2a06:98c1:50::ac40:20b3 | cut -d'|' -f2
```

Outputs:
> AWS
>
> AWS
>
> AWS
>
> Google Service
>
> Google Service
>
> Google Cloud
>
> Cloudflare


[AWS IP Ranges]: https://docs.aws.amazon.com/general/latest/gr/aws-ip-ranges.html
[Google Services IP Ranges]: https://support.google.com/a/answer/10026322?hl=en
[Google Cloud IP Ranges]: https://support.google.com/a/answer/10026322?hl=en
[Cloudflare IP Ranges]: https://www.cloudflare.com/ips
