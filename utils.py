#!/usr/bin/python
# -*- coding: utf-8 -*-

def get_contract_name(contract_param):
    # the weird rsplit gets the string to the right of the last "/"
    # in the contract path
    contract_name = contract_param.rsplit("/", 1)[1]
    # then remove and the file extension
    contract_name = contract_name.rsplit(".", 1)[0]

    return contract_name
