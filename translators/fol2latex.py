#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Superclass of the FOL translators, using Lark Interpreters """

from lark.visitors import Interpreter
from lark.lexer import Token
from lark import Tree
from translators.fol import FOL


class FOL2Latex(FOL):

    def implies(self, tree):
        """ Translate an implies tree """
        assert(tree.data == "implies")

        left, right = self.binary_infix(tree)

        return left + " \implies " + right

    def formula_variables_part(self, tree):
        """ Translate a formula_variables_part tree """
        assert(tree.data == "formula_variables_part")
        assert(len(tree.children) == 2)

        vars_extract, sets_extract = tree.children

        vars_out = self.visit(vars_extract)

        if isinstance(sets_extract, Token) :
            sets_out = str(sets_extract)
        elif isinstance(sets_extract, Tree) :
            sets_out = self.visit(sets_extract)

        return vars_out + " \in " + sets_out


    def equals(self, tree):
        """ Translate an equals tree """
        assert(tree.data == "equals")
        assert(len(tree.children)==2)

        eq_left, eq_right = self.binary_infix(tree)

        return eq_left + " = " + eq_right

    def not_equals(self, tree):
        """ Translate a not equals tree """
        assert(tree.data == "not_equals")

        eq_left, eq_right = self.binary_infix(tree)

        return eq_left + " \neq " + eq_right

    def in_form(self, tree):
        """ Translate an in tree """
        assert(tree.data == "in_form")

        in_left, in_right =  self.binary_infix(tree)

        return in_left + " \in " + in_right


    def not_in(self, tree):
        """ Translate a not in tree """
        assert(tree.data == "not_in")
        assert(len(tree.children)==2)

        in_left, in_right =  self.binary_infix(tree)

        return in_left + " \\notin " + in_right


    def leq(self, tree):
        """ Translate a leq tree """
        assert(tree.data == "leq")
        assert(len(tree.children)==2)

        left, right = self.binary_infix(tree)

        return left + " \leq " + right

    def geq(self, tree):
        """ Translate a geq tree """
        assert(tree.data == "geq")
        assert(len(tree.children)==2)

        left, right = self.binary_infix(tree)

        return left + " \geq " + right

    def lt(self, tree):
        """ Translate a lt tree """
        assert(tree.data == "lt")
        assert(len(tree.children)==2)

        left, right = self.binary_infix(tree)

        return left + " < " + right

    def gt(self, tree):
        """ Translate a gt tree """
        assert(tree.data == "gt")
        assert(len(tree.children)==2)

        left, right = self.binary_infix(tree)

        return left + " > " + right


    def negation(self, tree):
        """ Translate a negation tree """
        assert(tree.data == "negation")
        assert(len(tree.children) == 1)

        return "\\neg " + self.visit(tree.children[0])

    def and_form(self, tree):
        """ Translate an and tree """
        assert(tree.data == "and_form")
        assert(len(tree.children)==2)

        and_left, and_right  = self.binary_infix(tree)

        return and_left + " \land " + and_right

    def or_form(self, tree):
        """ Translate a or tree """
        assert(tree.data == "or_form")

        and_left, and_right  = self.binary_infix(tree)

        return and_left + " \lor " + and_right

    def iff(self, tree):
        """ Translate a iff tree """
        assert(tree.data == "iff")
        assert(len(tree.children)==2)

        iff_left, iff_right = self.binary_infix(tree)

        return iff_left + " \iff " + iff_right

    def forall(self, tree):
        """ Translate a forall tree """
        assert(tree.data == "forall")
        assert(len(tree.children) == 2 )

        variables = tree.children[0]
        formula = tree.children[1]

        variables_out = self.visit(variables)
        formula_out = self.visit(formula)

        return "\\forall " + variables_out + " \cdot " + formula_out

    def exists(self, tree):
        """ Translate a exists tree """
        assert(tree.data == "exists")
        assert(len(tree.children) == 2 )

        variables = tree.children[0]
        formula = tree.children[1]

        variables_out = self.visit(variables)
        formula_out = self.visit(formula)

        return "\\exists " + variables_out + " \cdot " + formula_out

    def exists_unique(self, tree):
        """ Translate a exists_unique tree """
        assert(tree.data == "exists_unique")
        assert(len(tree.children) == 2 )

        variables = tree.children[0]
        formula = tree.children[1]

        variables_out = self.visit(variables)
        formula_out = self.visit(formula)

        return "\\exists!~ " + variables_out + " \cdot " + formula_out


    def tuple(self, tree):
        """Translates a tuple tree """
        assert(tree.data == "tuple")

        head, *tail = tree.children

        vars = str(head)

        for var in tail:
            vars += ", " + str(var)


        assert(isinstance(vars, str))
        return "(" + vars + ")"


    def term_builtins(self, tree):
        """ Translate a term_builtins tree """
        assert(tree.data == "term_builtins")

        for term in tree.children:
            assert(isinstance(term, Token))
            if str(term) == "REAL":
                return "\mathbb{R}"
            elif str(term) == "INTEGER":
                return "\\mathbb{Z}"
            elif str(term) == "NATURAL":
                return "\\mathbb{N}"


    def set(self, tree):
        """Translates a set tree """
        assert(tree.data == "set")

        head, *tail = tree.children

        vars = str(head)

        for var in tail:
            vars += ", " + str(var)


        assert(isinstance(vars, str))
        return "\{" + vars + "\}"

    def empty_set(self, tree):
        """ Translates an empty_set tree """
        assert(tree.data == "empty_set")

        return "\\emptyset"


    def string_literal(self, tree):
        """ Translate a string literal tree """
        assert(tree.data == "string_literal")

        return "``" + tree.children[0] + "''"

    def variables(self, tree):
        """ Translate a variables tree """
        assert(tree.data == "variables")

        head, *tail = tree.children

        vars = str(head)

        for var in tail:
            vars += ", " + str(var)

        assert(isinstance(vars, str))
        return vars

# Helper Methods

    def binary_infix(self, tree):
        """ Helps translate any binary infix operator """
        assert(len(tree.children) == 2)

        print(tree)
        left = self.visit(tree.children[0])
        right = self.visit(tree.children[1])

        assert(isinstance(left, str))
        assert(isinstance(right, str))

        return left, right
