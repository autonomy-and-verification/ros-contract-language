#!/usr/bin/python
# -*- coding: utf-8 -*-

from translators.mirror import Mirror
from translators.translator_rosmon import ROSMon_Translator
from translators.translator_latex import Latex_Translator
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

# Arguments
argParser = argparse.ArgumentParser(prog='Vanda')
argParser.add_argument(
    "grammar", help="The grammar to parse with.", default="rcl", nargs='?')
argParser.add_argument("contract", help="The contract file to be parsed.")
argParser.add_argument("-t", help="The translator to use",
                       choices=['mirror', 'rosmon_rml', 'latex'], default='mirror')
argParser.add_argument(
    "-o", help="The path to the output folder for the translation")
argParser.add_argument("-p", help="Print the parse tree",
                       type=bool, default=False)
argParser.add_argument('--version', action='version',
                       version='%(prog)s ' + str(VERSION_NUM))


print("++++++++++++++++++++++++++++++++++++++++++++++")
print("+++++++++++++++++++ Vanda ++++++++++++++++++++")
print("++++++ ROS Contract Language Translator ++++++")
print("++++++++++++++++ version " + str(VERSION_NUM) + " +++++++++++++++++")
print("+++++++++++++++ Matt Luckcuck ++++++++++++++++")
print("++++++++++++++++++++++++++++++++++++++++++++++")
print("")

# Parse the Args
args = argParser.parse_args()

grammar_loc = "grammars/" + args.grammar + ".lark"

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


# Add the GRAMMAR to the parser
parser = Lark(GRAMMAR)

print("+++ Input File = +++")
print(CONTRACT)
print("")

# Parse the contract
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
    # , which should be the same (apart from whitespace) as the input
    test_trans = Mirror()
    print(test_trans.translate(contract_obj))

elif TRANSLATOR == "rosmon_rml":

    rosMon = ROSMon_Translator(contract_obj)
    # rosmon_config = romMon.translate(parse_tree)

    rosmon_config, rml = rosMon.translate_config()

    print(rosmon_config)

    print(rml)

    output_file = open(CONTRACT_PATH, "w")
    output_file.write(rosmon_config)
    output_file.close()

    for n in rml:
        output_file = open(RML_PATH[:-4]+'_'+str(n)+'.rml', "w")
        output_file.write(rml[n])
        output_file.close()

elif TRANSLATOR == "latex":

    latex_translator = Latex_Translator(VERSION_NUM, CONTRACT_NAME)
    latex_output = latex_translator.translate(contract_obj)
    print(latex_output)

    latex_main_file = "\\documentclass[12pt,a4paper]{article}\n\\usepackage[utf8]{inputenc}\n\\usepackage[english]{babel}\n\\usepackage{amsmath}\n\\usepackage{amsfonts}\n\\usepackage{lmodern}\n\\usepackage[left=4cm,right=4cm,top=4cm,bottom=4cm]{geometry}\n\\usepackage[UKenglish]{isodate}\n\\author{Vanda v"+str(
        VERSION_NUM)+"}\n\\title{Contract for: "+CONTRACT_NAME+"}\\begin{document}\n\\maketitle\n\n\input{" + CONTRACT_NAME+".tex}\n\\end{document}"

    output_file = open(OUTPUT_PATH+CONTRACT_NAME+".tex", "w")
    output_file.write(latex_output)
    output_file.close()

    output_main_file = open(OUTPUT_PATH+CONTRACT_NAME+"-main.tex", "w")
    output_main_file.write(latex_main_file)
    output_main_file.close()

print("")
