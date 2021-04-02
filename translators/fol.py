#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Superclass of the FOL translators, using Lark Interpreters """

from lark.visitors import Interpreter

class FOL(Interpreter):

    def guarantee(self, tree):
        """ Translate a guarantee tree """
        assert(tree.data == "guarantee")
        pass

    def implies(self, tree):
        """ Translate an implies tree """
        assert(tree.data == "implies")
        pass

    def equals(self, tree):
        """ Translate an equals tree """
        assert(tree.data == "equals")
        pass

    def not_equals(self, tree):
        """ Translate a not equals tree """
        assert(tree.data == "not_equals")
        pass

    def atom(self, term):
        """ Translate an atom tree """
        assert(tree.data == "atom")
        pass

    def negation(self, tree):
        """ Translate a negation tree """
        assert(tree.data == "negation")
        pass

    def and_form(self, tree):
        """ Translate an and tree """
        assert(tree.data == "and")
        pass

    def or_form(self, tree):
        """ Translate a or tree """
        assert(tree.data == "or")
        pass

    def iff(self, tree):
        """ Translate a iff tree """
        assert(tree.data == "iff")
        pass

    def forall(self, tree):
        """ Translate a forall tree """
        assert(tree.data == "forall")
        pass

    def exists(self, tree):
        """ Translate a exists tree """
        assert(tree.data == "exists")
        pass


    def terms(self, tree):
        """ Translate a terms tree """
        assert(tree.data == "terms")
        pass

    def term(self, tree):
        """ Translate a term tree """
        assert(tree.data == "term")
        pass

    def predicate(self, tree):
        """ Translate a predicate tree """
        assert(tree.data == "predicate")
        pass

    def function(self, tree):
        """ Translate a function tree """
        assert(tree.data == "function")
        pass

    def string_literal(self, tree):
        """ Translate a string literal tree """
        assert(tree.data == "string_literal")
        pass

# Helper Methods

    def binary_infix(self, tree):
        """ Helps translate any binary infix operator """
        assert(len(tree.children) == 2)
        print("translating some binary_operator")

        print(tree)

        left = self.visit(tree.children[0])
        right = self.visit(tree.children[1])

        assert(isinstance(left, str))
        print("Right...")
        print(right)

        assert(isinstance(right, str))


        print("left = " + left)
        print("right = " + right)

        return left, right