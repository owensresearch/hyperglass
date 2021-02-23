"""Parse VyOS JSON Response to Structured Data."""

# Standard Library
import json
from typing import Dict, Sequence

# Third Party
from pydantic import ValidationError

# Project
from hyperglass.log import log
from hyperglass.exceptions import ParsingError
from hyperglass.models.parsing.vyos import VyOSRoute

def parse_vyos(output: Sequence[str]) -> Dict:  # noqa: C901
    """Parse a VyOS BGP JSON response."""
    data = {}

    for i, response in enumerate(output):

        try:
            data: Dict = json.loads(response)

            log.debug("Pre-parsed data: {}", data)

            # VyOS doesn't show VRF when default used
            vrfs = ['default']
            vrf = list(data["vrfs"].keys())[0]
            routes = data["vrfs"][vrf]

            log.debug("Pre-validated data: {}", routes)

            validated = VyOSRoute(**routes)
            serialized = validated.serialize().export_dict()

            if i == 0:
                data.update(serialized)
            else:
                data["routes"].extend(serialized["routes"])

        except json.JSONDecodeError as err:
            log.critical("Error decoding JSON: {}", str(err))
            raise ParsingError("Error parsing response data")

        except (KeyError, IndexError) as err:
            log.critical("{} was not found in the response", str(err))
            raise ParsingError("Error parsing response data")

        except ValidationError as err:
            log.critical(str(err))
            raise ParsingError(err.errors())

    log.debug("Serialzed: {}", data)
    return data
