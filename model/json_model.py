# -*- coding: utf-8 -*-
import re
import pprint

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = ["version", "changeset", "timestamp", "user", "uid"]


def shape_element(element):
    """
    Method responsible for parsing the xml object into a valid JSON.

    Args:
        element: A XML element.

    Returns:
        node: A python dictionary representing a JSON

    """
    node = {}

    # You should process only 2 types of top level tags: "node" and "way"
    if element.tag == "node" or element.tag == "way":
        node["type"] = element.tag

        for attrib in element.attrib:
            # Attributes in the CREATED array should be added under a key "created"
            if attrib in CREATED:
                if 'created' in node:
                    node['created'][attrib] = element.attrib[attrib]
                else:
                    node['created'] = {attrib: element.attrib[attrib]}
            # Attributes for latitude and longitude should be added to a "pos" array
            elif attrib == "lat" or attrib == "lon":
                node["pos"] = [float(element.attrib["lat"]), float(element.attrib["lon"])]
            # All attributes of "node" and "way" should be turned into regular key/value pairs
            else:
                node[attrib] = element.attrib[attrib]

        for tag in element.iter("tag"):
            if "k" in tag.attrib:
                # If the second level tag "k" value contains problematic characters, it should be ignored
                if problemchars.search(tag.attrib["k"]):
                    pass
                # If the second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
                elif tag.attrib["k"].startswith("addr:"):
                    # if there is a second ":" that separates the type/direction of a street, the tag should be ignored
                    if len(tag.attrib["k"].split(":")) == 2:
                        if "address" in node:
                            node["address"][tag.attrib["k"].split(":")[1]] = tag.attrib["v"]
                        else:
                            node["address"] = {tag.attrib["k"].split(":")[1]: tag.attrib["v"]}
                    else:
                        pass
                # if the second level tag "k" value does not start with "addr:", but contains ":",
                # you can process it in a way that you feel is best
                elif ":" in tag.attrib["k"]:
                    node[tag.attrib["k"]] = tag.attrib["v"]

        if element.tag == "way":
            # For "way" specifically, should be turned into "node_refs": ["305896090", "1719825889"], for example.
            for nd in element.iter("nd"):
                if "node_refs" in node:
                    node["node_refs"].append(nd.attrib["ref"])
                else:
                    node["node_refs"] = [nd.attrib["ref"]]

        return node
    else:
        return None