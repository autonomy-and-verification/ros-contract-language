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

GRAMMAR=file.open(args.grammar)
CONTRACT=file.open(args.contract)

## Read the GRAMMAR and add it to the parser
parser = Lark(GRAMMAR.read())


print(parser.parse(CONTRACT).pretty())
