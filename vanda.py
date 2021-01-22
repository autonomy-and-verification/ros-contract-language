#!/usr/bin/python
# -*- coding: utf-8 -*-

from translators.mirror import Mirror
from translators.translator_rosmon import ROSMon_Translator
from extract_model import Extractor
from utils import *

try:
    input = raw_input   # For Python2 compatibility
except NameError:
    pass
from lark import Lark
import argparse
import os

VERSION_NUM = 0.1

## Arguments
argParser = argparse.ArgumentParser()
argParser.add_argument("grammar", help="The grammar to parse with.", default = "rcl")
argParser.add_argument("contract", help="The contract file to be parsed.")
argParser.add_argument("-t", help="The translator to use",choices=['test', 'rosmon_rml'], default = 'test' )
argParser.add_argument("-o", help="The path to the output file for the translation")
argParser.add_argument("-p", help="Print the parse tree", type=bool, default = False)


print("++++++++++++++++++++++++++++++++++++++++++++++")
print("+++++++++++++++++++ Vanda ++++++++++++++++++++")
print("++++++ ROS Contract Language Translator ++++++")
print("++++++++++++++++ version " + str(VERSION_NUM) + " +++++++++++++++++")
print("+++++++++++++++ Matt Luckcuck ++++++++++++++++")
print("++++++++++++++++++++++++++++++++++++++++++++++")
print("")

## Parse the Args
args = argParser.parse_args()

grammar_loc = "grammars/" + args.grammar +".lark"

GRAMMAR = open(grammar_loc).read()
CONTRACT = open(args.contract).read()
CONTRACT_NAME = get_contract_name(args.contract)

if args.o:
    OUTPUT_PATH = args.o
else:
    contract_name = CONTRACT_NAME + ".yaml"
    OUTPUT_PATH = "output/" + contract_name

    if not os.path.exists("output"):
        os.mkdir("output")

TRANSLATOR = args.t
PRINT = args.p


## Add the GRAMMAR to the parser
parser = Lark(GRAMMAR)

print("+++ Input File = +++")
print(CONTRACT)
print("")

#Parse the contract
parse_tree = parser.parse(CONTRACT)

if PRINT:
    print("+++ Pretty Parse Tree +++")
    print("")

    print(parse_tree.pretty())
    print("")

print("+++ Extractor Output +++")
print()

test_extractor = Extractor(CONTRACT_NAME)
contract_obj = test_extractor.extract(parse_tree)
print()
print("test_extractor.extract()")
print(str(contract_obj))
print()


print("+++ Translator Output +++")
print("")


if TRANSLATOR == "test":
    # Just Prints the Output, which should be the same (apart from whitespace)
    # as the input
    test_trans = Mirror()
    print(test_trans.translate(contract_obj))

elif TRANSLATOR == "rosmon_rml":
    rosMon = ROSMon_Translator(contract_obj)
    #rosmon_config = romMon.translate(parse_tree)

    rosmon_config = rosMon.translate_config()

    print(rosmon_config)

    output_file = open(OUTPUT_PATH, "w")
    output_file.write(rosmon_config)
    output_file.close()


print("")
