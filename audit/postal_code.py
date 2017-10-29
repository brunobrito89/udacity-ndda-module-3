# -*- coding: utf-8 -*-
import re


def is_postal_code(tag):
    """
    Method responsible for checking if a given tag is actually a postal code one.

    Args:
        tag: A postal code tag

    Returns:
        bool: Whether the tag is a postal code or not
    """
    return tag.attrib['k'] == "addr:postcode"


def is_postal_code_valid(elem):
    """
    Method responsible for checking if the postal code matches the regex and is correct.

    Args:
        tag: A postal code tag

    Returns:
        bool: Whether the postal code is valid or not
    """
    cep = re.compile('\d{5}-\d{3}')
    result = cep.search(elem.attrib['v']) and len(elem.attrib['v']) == 9

    #print elem.attrib['v']
    #print result
    #print "#####################"
    return result


def update_postal_code(elem):
    """
    Method responsible for fixing postal codes that are in the wrong format.
    In case there's more than one postal code, for simplicity use the left side postal code.

    Args:
        tag: A postal code tag

    Returns:
        tag: A postal code tag with the correct format
    """
    postal_code = ''.join(re.findall(r'\d+', elem.attrib['v']))

    #if len(postal_code) > 8:
    postal_code = postal_code[:8]

    result = postal_code[:5] + '-' + postal_code[5:8]

    #print elem.attrib['v']
    #print result
    #print "------------------------"
    return result


