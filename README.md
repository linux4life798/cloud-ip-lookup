# Amazon AWS IP Lookup

This tool uses the published
[AWS IP Ranges](https://docs.aws.amazon.com/general/latest/gr/aws-ip-ranges.html)
list to see if the given IP is contained in one of the ranges.

## Usage:

```bash
lookup.py <lookup_ip_address>
```

## Example

```shell
./lookup.py 44.242.161.7
```

Outputs:
> {'ip_prefix': '44.224.0.0/11', 'region': 'us-west-2', 'service': 'AMAZON', 'network_border_group': 'us-west-2'}
> {'ip_prefix': '44.224.0.0/11', 'region': 'us-west-2', 'service': 'EC2', 'network_border_group': 'us-west-2'}
> {'ip_prefix': '44.242.161.6/31', 'region': 'us-west-2', 'service': 'KINESIS_VIDEO_STREAMS', 'network_border_group': 'us-west-2'}