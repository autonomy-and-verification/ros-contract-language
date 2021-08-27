#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Superclass of the FOL translators, using Lark Interpreters """

from lark.visitors import Interpreter
from lark.lexer import Token
from lark import Tree


class FOL(Interpreter):

    def assume(self, tree):
        """ Translate an assume tree """
        assert(tree.data == "assume")

        return self.visit(tree.children[0])

    def guarantee(self, tree):
        """ Translate a guarantee tree """
        assert(tree.data == "guarantee")

        return self.visit(tree.children[0])

    def implies(self, tree):
        """ Translate an implies tree """
        assert(tree.data == "implies")

        pass

    def atom(self, tree):
        """ Translate an atom tree """
        assert(tree.data == "atom")

        return self.visit(tree.children[0])

    def atomic_formula(self, tree):
        """ Translate an atomic_formula tree """
        assert(tree.data == "atomic_formula")

        print(tree)
        if isinstance(tree.children[0], Token):
            token = tree.children[0]
            if token.type == "BOOLEAN":
                return self.make_string(token)
        else:
            assert(isinstance(tree.children[0], Tree))
            return self.visit(tree.children[0])

    def formula_variables(self, tree):
        """ Translate a formula_variables tree """
        assert(tree.data == "formula_variables")

        head, *tail = tree.children
        vars_out = self.visit(head)

        for term in tail:
            vars_out += ", " + self.visit(term)

        assert(isinstance(vars_out, str))
        return vars_out

    def formula_variables_part(self, tree):
        """ Translate a formula_variables_part tree """
        assert(tree.data == "formula_variables_part")

        pass

    def equals(self, tree):
        """ Translate an equals tree """
        assert(tree.data == "equals")
        pass

    def not_equals(self, tree):
        """ Translate a not equals tree """
        assert(tree.data == "not_equals")
        pass

    def in_form(self, tree):
        """ Translate an in tree """
        assert(tree.data == "in_form")
        pass

    def not_in(self, tree):
        """ Translate a not in tree """
        assert(tree.data == "not_in")
        assert(len(tree.children) == 2)

        pass

    def leq(self, tree):
        """ Translate a leq tree """
        assert(tree.data == "leq")
        assert(len(tree.children) == 2)

        pass

    def geq(self, tree):
        """ Translate a geq tree """
        assert(tree.data == "geq")
        assert(len(tree.children) == 2)

        pass

    def lt(self, tree):
        """ Translate a lt tree """
        assert(tree.data == "lt")
        assert(len(tree.children) == 2)

        pass

    def gt(self, tree):
        """ Translate a gt tree """
        assert(tree.data == "gt")
        assert(len(tree.children) == 2)

        pass

    def var_range(self, tree):
        """ Translate a var_range tree """
        assert(tree.data == "var_range")
        assert(len(tree.children) == 5)

        left_term = tree.children[0]
        left_op = tree.children[1]
        mid_term = tree.children[2]
        right_op = tree.children[3]
        right_term = tree.children[4]

        left_term_out = self.visit(left_term)
        mid_term_out = self.visit(mid_term)
        right_term_out = self.visit(right_term)

        return left_term_out + self.make_string(left_op) + mid_term_out + self.make_string(right_op) + right_term_out

    def negation(self, tree):
        """ Translate a negation tree """
        assert(tree.data == "negation")

        pass

    def and_form(self, tree):
        """ Translate an and tree """
        assert(tree.data == "and_form")
        assert(len(tree.children) == 2)

        pass

    def or_form(self, tree):
        """ Translate a or tree """
        assert(tree.data == "or")
        pass

    def iff(self, tree):
        """ Translate a iff tree """
        assert(tree.data == "iff")
        assert(len(tree.children) == 2)

        pass

    def sub_formula(self, tree):
        """ Translate a sub formula tree """
        assert(tree.data == "sub_formula")
        assert(len(tree.children) == 1)

        return "( " + self.visit(tree.children[0]) + " )"

    def forall(self, tree):
        """ Translate a forall tree """
        assert(tree.data == "forall")
        assert(len(tree.children) == 2)

        pass

    def exists(self, tree):
        """ Translate a exists tree """
        assert(tree.data == "exists")
        assert(len(tree.children) == 2)
        pass

    def exists_unique(self, tree):
        """ Translate a exists_unique tree """
        assert(tree.data == "exists_unique")
        assert(len(tree.children) == 2)

        pass

    def arithmetic(self, tree):
        """Translate an arithmetic statement """
        assert(tree.data == "arithmetic")
        assert(len(tree.children) == 1)

        arith_tree = tree.children[0]
        assert(arith_tree.data == "arith")

        # (VARIABLE|NUMBER) ARITH_OP (VARIABLE|NUMBER)

        left = self.make_string(arith_tree.children[0])
        op = self.make_string(arith_tree.children[1])
        right = self.make_string(arith_tree.children[2])

        assert(isinstance(left, str))
        assert(isinstance(op, str))
        assert(isinstance(right, str))

        return left + op + right

    def tuple(self, tree):
        """Translates a tuple tree """
        assert(tree.data == "tuple")

        pass

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

        assert(len(tree.children) == 1)
        if (isinstance(tree.children[0], Token)):
            return self.make_string(tree.children[0])
        elif (isinstance(tree.children[0], Tree)):
            return self.visit(tree.children[0])

    def set(self, tree):
        """Translates a set tree """
        assert(tree.data == "set")
        pass

    def sequence(self, tree):
        """ TRanslates a sequence tree """
        assert(tree.data == "sequence")

        pass

    def string_literal(self, tree):
        """ Translate a string literal tree """
        assert(tree.data == "string_literal")

        pass

    def variables(self, tree):
        """ Translate a variables tree """
        assert(tree.data == "variables")

        pass

    def type_declaration_part(self, tree):
        """ Translate a type_declaration_part tree """
        assert(tree.data == "type_declaration_part")
        assert(len(tree.children) == 1)

        return self.visit(tree.children[0])


# Helper Methods


    def binary_infix(self, tree):
        """ Helps translate any binary infix operator """
        assert(len(tree.children) == 2)

        left = self.visit(tree.children[0])
        right = self.visit(tree.children[1])

        assert(isinstance(left, str))
        assert(isinstance(right, str))

        return left, right

    def make_string(self, to_string):
        return str(to_string).replace('_', '\\_')
