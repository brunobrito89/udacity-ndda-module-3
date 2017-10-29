# -*- coding: utf-8 -*-
# Mapping constant to fix wrong street prefixes
street_mapping = {
        "R.": "Rua",
        "Av": "Avenida",
        "Av.": "Avenida",
        "Ave": "Avenida",
        "Rua.": "Rua",
        "rua": "Rua",
        "SP-332": "Rodovia SP-332"
        }

def is_street_name(tag):
    """
    Method responsible for checking if a given tag is actually a street one.

    Args:
        tag: A way tag

    Returns:
        bool: Whether the tag is a street or not
    """
    return (tag.attrib['k'] == "addr:street")

def update_street_name(tag):
    """
    Method responsible for fixing the wrong street prefixes according to the street_mapping constant.

    Args:
        tag: A way tag

    Returns:
        tag: A way tag with the fixed prefix
    """
    prefix = tag.attrib['v'].split(" ")[0]
    
    if prefix in street_mapping:
        tag.attrib['v'] = tag.attrib['v'].replace(prefix, street_mapping[prefix])   
            
    return tag
