#!/usr/bin/python
# -*- coding: utf-8 -*-

from translators.translator_test import Test_Translator
from translators.translator_rosmon import ROSMon_Translator

try:
    input = raw_input   # For Python2 compatibility
except NameError:
    pass
from lark import Lark
import argparse

VERSION_NUM = 0.1

## Arguments
argParser = argparse.ArgumentParser()
argParser.add_argument("grammar", help="The grammar to parse with.", default = "rcl")
argParser.add_argument("contract", help="The contract file to be parsed.")
argParser.add_argument("-t", help="The translator to use",choices=['test', 'ros_mon_rml'], default = 'test' )
argParser.add_argument("-o", help="The path to the output file for the translation")
argParser.add_argument("-p", help="Print the parse tree", type=bool, default = False)


## Parse the Args
args = argParser.parse_args()

grammar_loc = "grammars/" + args.grammar +".lark"

GRAMMAR = open(grammar_loc).read()
CONTRACT = open(args.contract).read()
TRANSLATOR = args.t
PRINT = args.p

print("++++++++++++++++++++++++++++++++++++++++++++++")
print("++++++ ROS Contract Language Translator ++++++")
print("++++++++++++++++ version " + str(VERSION_NUM) + " +++++++++++++++++")
print("+++++++++++++++ Matt Luckcuck ++++++++++++++++")
print("++++++++++++++++++++++++++++++++++++++++++++++")
print("")




## Add the GRAMMAR to the parser
parser = Lark(GRAMMAR)

print("+++ Input File = +++")
print(CONTRACT)
print("")

#Parse the contract
parseTree = parser.parse(CONTRACT)

if PRINT:
    print("+++ Pretty Parse Tree +++")
    print("")

    print(parseTree.pretty())
    print("")

print("+++ Translator Output +++")
print("")

if TRANSLATOR == "test":
    test_trans = Test_Translator()
    print(test_trans.translate(parseTree))

elif TRANSLATOR == "ros_mon_rml":
    romMon_trans = ROSMon_Translator()
    romMon_trans.translate(parseTree)

print("")
