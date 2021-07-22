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

        return in_left + " \notin " + in_right


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

        return "[negation placeholder]"

    def and_form(self, tree):
        """ Translate an and tree """
        assert(tree.data == "and_form")
        assert(len(tree.children)==2)

        and_left, and_right  = self.binary_infix(tree)

        return and_left + " \land " + and_right

    def or_form(self, tree):
        """ Translate a or tree """
        assert(tree.data == "or")

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

        return "\\exists! " + variables_out + " \cdot " + formula_out

    def arithmetic(self, tree):
        """Translate an arithmetic statement """
        assert(tree.data == "arithmetic")
        assert(len(tree.children) == 1)

        return "[artihmatic placeholder]"

    def tuple(self, tree):
        """Translates a tuple tree """
        assert(tree.data == "tuple")

        return "[tuple placeholder]"

    def terms(self, tree):
        """ Translate a terms tree """
        assert(tree.data == "terms")

        head, *tail = tree.children
        terms_out = self.visit(head)

        for term in tail:
            terms_out += ", " + self.visit(term)

        assert(isinstance(terms_out, str))
        return terms_out

    def term(self, tree):
        """ Translate a term tree """
        assert(tree.data == "term")

        assert(len(tree.children)==1)
        assert(isinstance(tree.children[0],Token ))

        return str(tree.children[0])

    def term_builtins(self, tree):
        """ Translate a term_builtins tree """
        assert(tree.data == "term_builtins")

        for term in tree.children:
            assert(isinstance(term, Token))
            if str(term) == "REAL":
                return "\\R"
            elif str(term) == "INTEGER":
                return "\\Z"
            elif str(term) == "NATURAL":
                return "\\N"

    def set(self, tree):
        """Translates a set tree """
        assert(tree.data == "set")

        return "[set placeholder]"




    def string_literal(self, tree):
        """ Translate a string literal tree """
        assert(tree.data == "string_literal")

        return "[string_literal placeholder]"

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

        left = self.visit(tree.children[0])
        right = self.visit(tree.children[1])

        print(right)

        assert(isinstance(left, str))
        assert(isinstance(right, str))

        return left, right
