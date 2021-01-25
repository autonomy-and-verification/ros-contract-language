#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Translates FOL to RML, using a Lark Interpreter """

from translators.fol import FOL

class FOL2RML(FOL):

    def guarantee(self, tree):
        """ Translate a guarantee tree """
        assert(tree.data == "guarantee")
        return "implement me"

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
