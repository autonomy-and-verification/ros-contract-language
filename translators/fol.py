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

    def atomic_formula(self,tree):
        """ Translate an atomic_formula tree """
        assert(tree.data == "atomic_formula")

        if isinstance(tree.children[0], Token):
            token = tree.children[0]
            if token.type == "BOOLEAN":
                return str(token)
        else:
            assert(isinstance(tree.children[0], Tree))
            return self.visit(tree.children[0])

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
        assert(len(tree.children)==2)

        pass


    def leq(self, tree):
        """ Translate a leq tree """
        assert(tree.data == "leq")
        assert(len(tree.children)==2)

        pass

    def geq(self, tree):
        """ Translate a geq tree """
        assert(tree.data == "geq")
        assert(len(tree.children)==2)

        pass

    def lt(self, tree):
        """ Translate a lt tree """
        assert(tree.data == "lt")
        assert(len(tree.children)==2)

        pass

    def gt(self, tree):
        """ Translate a gt tree """
        assert(tree.data == "gt")
        assert(len(tree.children)==2)

        pass

    def var_range(self, tree):
        """ Translate a var_range tree """
        assert(tree.data == "var_range")
        assert(len(tree.children)==5)

        pass

    def negation(self, tree):
        """ Translate a negation tree """
        assert(tree.data == "negation")

        pass

    def and_form(self, tree):
        """ Translate an and tree """
        assert(tree.data == "and_form")
        assert(len(tree.children)==2)

        pass

    def or_form(self, tree):
        """ Translate a or tree """
        assert(tree.data == "or")
        pass

    def iff(self, tree):
        """ Translate a iff tree """
        assert(tree.data == "iff")
        assert(len(tree.children)==2)

        pass

    def bracket_form(self, tree):
        """ Translate a bracketed formula """
        assert(tree.data == "bracket_form")
        assert(len(tree.children) == 1)

        pass

    def forall(self, tree):
        """ Translate a forall tree """
        assert(tree.data == "forall")
        assert(len(tree.children) == 2 )

        pass

    def exists(self, tree):
        """ Translate a exists tree """
        assert(tree.data == "exists")
        assert(len(tree.children) == 2 )
        pass

    def exists_unique(self, tree):
        """ Translate a exists_unique tree """
        assert(tree.data == "exists_unique")
        assert(len(tree.children) == 2 )

        pass

    def predicate(self, tree):
        """ Translate a predicate tree """
        assert(tree.data == "predicate")

        pass

    def arithmetic(self, tree):
        """Translate an arithmetic statement """
        assert(tree.data == "arithmetic")
        assert(len(tree.children) == 1)

        pass

    def tuple(self, tree):
        """Translates a tuple tree """
        assert(tree.data == "tuple")

        pass

    def terms(self, tree):
        """ Translate a terms tree """
        assert(tree.data == "terms")

        pass

    def term(self, tree):
        """ Translate a term tree """
        assert(tree.data == "term")

        pass

    def set(self, tree):
        """Translates a set tree """
        assert(tree.data == "set")

        pass


    def predicate(self, tree):
        """ Translate a predicate tree """
        assert(tree.data == "predicate")

        assert(isinstance(tree.children[0],Token ))
        pred_name = str(tree.children[0])
        pred_terms = self.visit(tree.children[1])

        return pred_name + "("+ str(pred_terms) +")"

    def function(self, tree):
        """ Translate a function tree """
        assert(tree.data == "function")

        assert(isinstance(tree.children[0],Token ))
        func_name = str(tree.children[0])
        func_args = self.visit(tree.children[1])

        return func_name + "("+ str(func_args) +")"

    def string_literal(self, tree):
        """ Translate a string literal tree """
        assert(tree.data == "string_literal")

        pass

    def variables(self, tree):
        """ Translate a variables tree """
        assert(tree.data == "variables")

        pass

# Helper Methods

    def binary_infix(self, tree):
        """ Helps translate any binary infix operator """
        assert(len(tree.children) == 2)

        left = self.visit(tree.children[0])
        right = self.visit(tree.children[1])

        assert(isinstance(left, str))
        assert(isinstance(right, str))

        return left, right
