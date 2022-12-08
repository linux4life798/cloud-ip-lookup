# Cloud Services IP Lookup

This tool checks if the given IP exists in any of the published IP ranges from
[Amazon AWS][AWS IP Ranges], [Google Services][Google Services IP Ranges],
[Google Cloud][Google Cloud IP Ranges], or [Cloudflare][Cloudflare IP Ranges].

Once the IP ranges JSON is downloaded from the respective cloud provider, the
search for the encapsulating IP range occurs offline.

## Usage:

```bash
lookup.py <lookup_ip_address>
```

## Example 1

```shell
./lookup.py 44.242.161.7
```

Outputs:
> AWS: {'ip_prefix': '44.224.0.0/11', 'region': 'us-west-2', 'service': 'AMAZON', 'network_border_group': 'us-west-2'}
> AWS: {'ip_prefix': '44.224.0.0/11', 'region': 'us-west-2', 'service': 'EC2', 'network_border_group': 'us-west-2'}
> AWS: {'ip_prefix': '44.242.161.6/31', 'region': 'us-west-2', 'service': 'KINESIS_VIDEO_STREAMS', 'network_border_group': 'us-west-2'}

## Example 2

```shell
./lookup.py 8.8.8.8
```

Outputs:
> Google Service: {'ipv4Prefix': '8.8.8.0/24'}

# Example 3

```shell
./lookup.py 35.231.19.128
```

Outputs:
> Google Service: {'ipv4Prefix': '35.224.0.0/12'}
> Google Cloud: {'ipv4Prefix': '35.231.0.0/16', 'service': 'Google Cloud', 'scope': 'us-east1'}

## Example 4

```shell
./lookup.py 2a06:98c1:50::ac40:20b3
```

Outputs:
> Cloudflare: 2a06:98c0::/29


[AWS IP Ranges]: https://docs.aws.amazon.com/general/latest/gr/aws-ip-ranges.html
[Google Services IP Ranges]: https://support.google.com/a/answer/10026322?hl=en
[Google Cloud IP Ranges]: https://support.google.com/a/answer/10026322?hl=en
[Cloudflare IP Ranges]: https://www.cloudflare.com/ips
