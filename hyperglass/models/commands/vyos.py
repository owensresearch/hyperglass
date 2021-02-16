"""VyOS Command Model."""

# Third Party
from pydantic import StrictStr

# Local
from .common import CommandSet, CommandGroup


class _IPv4(CommandSet):
    """Validation model for non-default dual afi commands."""

    bgp_route: StrictStr = "show ip bgp {target}"
    bgp_aspath: StrictStr = 'show ip bgp regexp "{target}"'
    bgp_community: StrictStr = "show ip bgp community {target}"
    ping: StrictStr = "ping {target} count 5 interface {source}"
    traceroute: StrictStr = "mtr -4 -G 1 -c 1 -w -o SAL -a {source} {target}"


class _IPv6(CommandSet):
    """Validation model for non-default ipv4 commands."""

    bgp_route: StrictStr = "show ipv6 bgp {target}"
    bgp_aspath: StrictStr = 'show ipv6 bgp regexp "{target}"'
    bgp_community: StrictStr = "show ipv6 bgp community {target}"
    ping: StrictStr = "ping {target} count 5 interface {source}"
    traceroute: StrictStr = "mtr -6 -G 1 -c 1 -w -o SAL -a {source} {target}"


class _VPNIPv4(CommandSet):
    """Validation model for non-default ipv6 commands."""

    bgp_route: StrictStr = "show ip bgp {target}"
    bgp_aspath: StrictStr = 'show ip bgp regexp "{target}"'
    bgp_community: StrictStr = "show ip bgp community {target}"
    ping: StrictStr = "ping {target} count 5 vrf {vrf} interface {source}"
    traceroute: StrictStr = "ip vrf exec {vrf} mtr -4 -G 1 -c 1 -w -o SAL -a {source} {target}"


class _VPNIPv6(CommandSet):
    """Validation model for non-default ipv6 commands."""

    bgp_route: StrictStr = "show ipv6 bgp {target}"
    bgp_aspath: StrictStr = 'show ipv6 bgp regexp "{target}"'
    bgp_community: StrictStr = "show ipv6 bgp community {target}"
    ping: StrictStr = "ping {target} count 5 interface {source}"
    traceroute: StrictStr = "ip vrf exec {vrf} mtr -6 -G 1 -c 1 -w -o SAL -a {source} {target}"


_structured = CommandGroup(
    ipv4_default=CommandSet(
        bgp_route='vtysh -c "show ip bgp {target} json"',
        bgp_aspath='vtysh -c "show ip bgp regexp {target} json"',
        bgp_community='vtysh -c "show ip bgp community {target} json"',
        ping="ping {target} count 5 interface {source}",
        traceroute="mtr -4 -G 1 -c 1 -w -o SAL -a {source} {target}",
    ),
    ipv6_default=CommandSet(
        bgp_route='vtysh -c "show ipv6 bgp {target} json"',
        bgp_aspath='vtysh -c "show ipv6 bgp regexp {target} json"',
        bgp_community='vtysh -c "show ipv6 bgp community {target} json"',
        ping="ping {target} count 5 interface {source}",
        traceroute="mtr -6 -G 1 -c 1 -w -o SAL -a {source} {target}",
    ),
    ipv4_vpn=CommandSet(
        bgp_route='vtysh -c "show ip bgp {target} vrf {vrf} json"',
        bgp_aspath='vtysh -c "show ip bgp regexp {target} vrf {vrf} json"',
        bgp_community='vtysh -c "show ip bgp community {target} vrf {vrf} json"',
        ping="ping {target} count 5 vrf {vrf} interface {source}",
        traceroute="ip vrf exec {vrf} mtr -4 -G 1 -c 1 -w -o SAL -a {source} {target}",
    ),
    ipv6_vpn=CommandSet(
        bgp_route='vtysh -c "show ipv6 bgp {target} vrf {vrf} json"',
        bgp_aspath='vtysh -c "show ipv6 bgp regexp {target} vrf {vrf} json"',
        bgp_community='vtysh -c "show ipv6 bgp community {target} vrf {vrf} json"',
        ping="ping {target} count 5 interface {source}",
        traceroute="ip vrf exec {vrf} mtr -6 -G 1 -c 1 -w -o SAL -a {source} {target}",
    ),
)


class VyosCommands(CommandGroup):
    """Validation model for default juniper commands."""

    ipv4_default: _IPv4 = _IPv4()
    ipv6_default: _IPv6 = _IPv6()
    ipv4_vpn: _VPNIPv4 = _VPNIPv4()
    ipv6_vpn: _VPNIPv6 = _VPNIPv6()


    def __init__(self, **kwargs):
        """Initialize command group, ensure structured fields are not overridden."""
        super().__init__(**kwargs)
        self.structured = _structured