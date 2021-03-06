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
argParser.add_argument("-t", help="The translator to use",choices=['mirror', 'rosmon_rml'], default = 'mirror' )
argParser.add_argument("-o", help="The path to the output folder for the translation")
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
    OUTPUT_PATH = "output/"
contract_name = CONTRACT_NAME + ".yaml"
CONTRACT_PATH = OUTPUT_PATH + contract_name
rml_name = CONTRACT_NAME + ".rml"
RML_PATH = OUTPUT_PATH + rml_name

if not os.path.exists(OUTPUT_PATH):
    os.mkdir(OUTPUT_PATH)

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


if TRANSLATOR == "mirror":
    # Just prints the output of the Mirror translator
    #, which should be the same (apart from whitespace) as the input
    test_trans = Mirror()
    print(test_trans.translate(contract_obj))

elif TRANSLATOR == "rosmon_rml":

    rosMon = ROSMon_Translator(contract_obj)
    #rosmon_config = romMon.translate(parse_tree)

    rosmon_config, rml = rosMon.translate_config()

    print(rosmon_config)

    print(rml)

    output_file = open(CONTRACT_PATH, "w")
    output_file.write(rosmon_config)
    output_file.close()

    output_file = open(RML_PATH, "w")
    output_file.write(rml)
    output_file.close()


print("")
