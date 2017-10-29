# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import codecs
import json
from audit.street_names import is_street_name, update_street_name
from audit.postal_code import is_postal_code, is_postal_code_valid, update_postal_code
from model import json_model
import pprint
from util import *


# Original OSM File from the region of Campinas
osm_path = "./dataset/campinas.osm"


def audit():
    """Audit method used to understand the data and detect if any elements needs to be fixed

    :args:
    :return:
    """
    elem_tags = {}
    way_tags = {}
    street_prefixes = {}
    postal_codes = {}

    osm_file = open(osm_path, "r")

    for event, elem in ET.iterparse(osm_file, events=("start",)):
        # Understanding the tags available in the dataset.
        if elem.tag in elem_tags:
            elem_tags[elem.tag] += 1
        else:
            elem_tags[elem.tag] = 1

        # Checking the available way tags
        if elem.tag == "way":
            for tag in elem.iter("tag"):
                if tag.attrib['k'] in way_tags:
                    way_tags[tag.attrib['k']] += 1
                else:
                    way_tags[tag.attrib['k']] = 1

                # Checking existing street prefixes
                if tag.attrib['k'] == "addr:street":
                    if tag.attrib['v'].split(" ")[0] in street_prefixes:
                        street_prefixes[tag.attrib['v'].split(" ")[0]] += 1
                    else:
                        street_prefixes[tag.attrib['v'].split(" ")[0]] = 1
                # Checking existing postal codes
                elif tag.attrib['k'] == "addr:postcode":
                    if tag.attrib['v'] in postal_codes:
                        postal_codes[tag.attrib['v']] += 1
                    else:
                        postal_codes[tag.attrib['v']] = 1

    osm_file.close()



    pprint.pprint(elem_tags)
    pprint.pprint(way_tags)
    pprint.pprint(street_prefixes)
    pprint.pprint(postal_codes)

def transform():
    """Transform method responsible for cleaning the data and generating a JSON file ready to be imported on MongoDB.

    :args:
    :return:
    """

    # Final JSON containing the cleaned data.
    file_out = "{0}.json".format("mongo_import_result")
    osm_file = open(osm_path, "r")
    data = []

    with codecs.open(file_out, "w") as fo:
        for event, elem in ET.iterparse(osm_path, events=("start",)):
            if elem.tag == "way":
                for tag in elem.iter("tag"):
                    # Audits Street Names
                    if is_street_name(tag):
                        tag = update_street_name(tag)
                    # Audits Postal Codes
                    elif is_postal_code(tag):
                        if not is_postal_code_valid(tag):
                            tag.attrib['v'] = update_postal_code(tag)


            # Builds a python dict representing a JSON
            json_obj = json_model.shape_element(elem)
            # Append it to a list and writes to an output json file.
            if json_obj:
                data.append(json_obj)
                fo.write(json.dumps(json_obj, indent=2) + "\n")

    osm_file.close()


if __name__ == "__main__":
    audit()
    transform()

