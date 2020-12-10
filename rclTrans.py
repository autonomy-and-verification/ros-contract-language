#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
    input = raw_input   # For Python2 compatibility
except NameError:
    pass


from lark import Lark
import argparse

argParser = argparse.ArgumentParser()
argParser.add_argument("grammar", help="The grammar file")
argParser.add_argument("contract", help="The contract file")
argParser.add_argument("-o", help="The output file for the translation")
#Disabled

args = argParser.parse_args()

GRAMMAR = open(args.grammar).read()
CONTRACT = open(args.contract).read()



## Add the GRAMMAR to the parser
parser = Lark(GRAMMAR)


print(parser.parse(CONTRACT).pretty())
