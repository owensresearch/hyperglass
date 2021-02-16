"""Data Models for Parsing VyOS JSON Response."""

# Standard Library
from typing import List
from datetime import datetime

# Third Party
from pydantic import StrictInt, StrictStr, StrictBool, constr, root_validator

# Project
from hyperglass.log import log

# Local
from ..main import HyperglassModel
from .serialized import ParsedRoutes

VyOSPeerType = constr(regex=r"(internal|external)")


def _alias_generator(field):
    components = field.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


class _VyOSBase(HyperglassModel):
    class Config:
        alias_generator = _alias_generator
        extra = "ignore"


class VyOSNextHop(_VyOSBase):
    """VyOS Next Hop Model."""

    ip: StrictStr
    afi: StrictStr
    metric: StrictInt
    accessible: StrictBool
    used: StrictBool


class VyOSPeer(_VyOSBase):
    """VyOS Peer Model."""

    peerId: StrictStr
    routerId: StrictStr
    type: VyOSPeerType


class VyOSLastUpdate(_VyOSBase):
    """VyOS Last Update Model"""

    epoch: StrictInt
    string: StrictStr


class VyOSPath(_VyOSBase):
    """VyOS Path Model."""
    prefix: StrictStr
    aspath: StrictStr
    med: StrictInt = 0
    localpref: StrictInt = 100
    weight: StrictInt = 0
    valid: StrictBool
    lastUpdate: List[VyOSLastUpdate]
    bestpath: StrictBool
    community: StrictStr
    nexthops: List[VyOSNextHop]
    peer: List[VyOSPeer]

    @root_validator(pre=True)
    def validate_path(cls, values):
        """Extract meaningful data from VyOS response."""
        new = values.copy()
        new["aspath"] = values["aspath"]["segments"][0]["list"]
        new["community"] = values["community"]["list"]
        new["lastUpdate"] = values["lastUpdate"]["epoch"]
        bestpath = values.get("bestpath", {})
        new["bestpath"] = bestpath.get("overall", False)
        return new


class VyOSRoute(_VyOSBase):
    """VyOS Route Model."""

    prefix: StrictStr
    paths: List[VyOSPath] = []

    def serialize(self):
        """Convert the VyOS-specific fields to standard parsed data model."""

        # TODO: somehow, get the actual VRF
        vrf = "default"

        routes = []
        for route in self.paths:
            now = datetime.utcnow().timestamp()
            then = datetime.utcfromtimestamp(route.lastUpdate).timestamp()
            age = int(now - then)
            routes.append(
                {
                    "prefix": self.prefix,
                    "active": route.bestpath,
                    "age": age,
                    "weight": route.weight,
                    "med": route.med,
                    "local_preference": route.localpref,
                    "as_path": route.aspath,
                    "communities": route.community,
                    "next_hop": route.nexthops[0].ip,
                    # TODO: Revisit the source as situation
                    "source_as": route.aspath[-1],
                    "source_rid": '1.1.1.1',
                    "peer_rid": route.peer.peerId,
                    # TODO: somehow, get the actual RPKI state
                    "rpki_state": 3,
                }
            )

        serialized = ParsedRoutes(
            vrf=vrf, count=len(routes), routes=routes, winning_weight="high",
        )

        log.info("Serialized VyOS response: {}", serialized)
        return serialized
