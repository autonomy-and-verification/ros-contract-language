# ros-contract-language
A contract language for ROS nodes and a parsing tool `Vanda`.

`Vanda`. is written in Python3.

## Installation

* Requires: [pip](https://pypi.org/project/pip/)
* Install the [Lark](https://github.com/lark-parser/lark) parser library: `pip install lark-parser --upgrade`
* Then clone this repository: `git clone https://github.com/autonomy-and-verification/ros-contract-language.git`

## Usage

The basic usage is as follows:
```
python3 vanda.py rcl test/chatter.rcl -t latex
```
This runs `Vanda` using the `rcl` grammar on the contract `test/chatter.rcl` using the `latex` translator, which simply returns the original contract as a LaTeX document. This will display the original contract, under `+++ Input File = +++`; the output from the extraction (pre-processing) step, under `+++ Extractor Output +++`; and the output from the translation step, under `+++ Translator Output +++`.


The full usage details (as shown by running `python3 vanda.py -h`) are:
```
usage: Vanda [-h] [-t {mirror,rosmon_rml,latex}] [-o O] [-p P] [--version] [grammar] contract

positional arguments:
  grammar               The grammar to parse with.
  contract              The contract file to be parsed.

optional arguments:
  -h, --help            show this help message and exit
  -t {mirror,rosmon_rml,latex}
                        The translator to use
  -o O                  The path to the output folder for the translation
  -p P                  Print the parse tree
  --version             show program's version number and exit

```

## Writing a New Translator

The translation step uses a `Contract` object (found in the `contract_mode.py` module) as its input. This is an intermediate representation of the contract, which stores the node name, and lists the topics and guarantees. The guarantees are the First-Order Logic statements, they have **not** been translated yet and that is something the translation step must implement for each new output (or reuse an existing translator if appropriate).

To implement a new translator you need to:
1. write a _contract translator_ class, implementing the loose superclass in `translator.py`, and
2. write a _FOL translator_ class, implementing the superclass in `fol.py` -- which implements the Lark `Interpreter`

The contract translator just needs to take the information in the `Contract` class it's given and prepare the relevant output for it. For example, in the `Mirror` translator, this just means re-building a string of the input contract.

The FOL translator is a visitor that walks the Lark parse tree representing a FOL guarantee. This must implement a method for each of the types of (Lark) tree in the grammar. For example, in the `FOL2Text` translator -- used by the `Mirror` translator, and found in `fol2text.py` -- has a `negation` method that builds a string beginning with "not", followed by the translation (via recursion) of the negated statement. Each of the types of tree can be found in the RCL grammar (`rcl.lark`).
