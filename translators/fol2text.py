#!/usr/bin/python
# -*- coding: utf-8 -*-

from lark.visitors import Interpreter
from lark.lexer import Token
from lark import Tree
from translators.fol import FOL

class FOL2Text(FOL):

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

            left, right = self.binary_infix(tree)

            return left + " -> " + right

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
            assert(len(tree.children)==2)

            eq_left, eq_right = self.binary_infix(tree)

            return eq_left + " == " + eq_right

        def not_equals(self, tree):
            """ Translate a not equals tree """
            assert(tree.data == "not_equals")
            assert(len(tree.children)==2)

            eq_left, eq_right = self.binary_infix(tree)

            return eq_left + " != " + eq_right

        def in_form(self, tree):
            """ Translate an in tree """
            assert(tree.data == "in_form")
            assert(len(tree.children)==2)

            in_left, in_right =  self.binary_infix(tree)

            return in_left + " in " + in_right

        def not_in(self, tree):
            """ Translate a not in tree """
            assert(tree.data == "not_in")
            assert(len(tree.children)==2)

            in_left, in_right  = self.binary_infix(tree)

            return in_left + " !in " + in_right


        def leq(self, tree):
            """ Translate a leq tree """
            assert(tree.data == "leq")
            assert(len(tree.children)==2)

            left, right = self.binary_infix(tree)

            return left + " <= " + right

        def geq(self, tree):
            """ Translate a geq tree """
            assert(tree.data == "geq")
            assert(len(tree.children)==2)

            left, right = self.binary_infix(tree)

            return left + " >= " + right

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

            return "not " + self.visit(tree.children[0])

        def and_form(self, tree):
            """ Translate an and tree """
            assert(tree.data == "and_form")
            assert(len(tree.children)==2)

            and_left, and_right  = self.binary_infix(tree)

            return and_left + " and " + and_right

        def or_form(self, tree):
            """ Translate a or tree """
            assert(tree.data == "or_form")
            assert(len(tree.children)==2)

            or_left, or_right  = self.binary_infix(tree)

            return or_left + " or " + or_right

        def iff(self, tree):
            """ Translate a iff tree """
            assert(tree.data == "iff")
            assert(len(tree.children)==2)

            iff_left, iff_right = self.binary_infix(tree)

            return iff_left + " <=> " + iff_right


        def forall(self, tree):
            """ Translate a forall tree """
            assert(tree.data == "forall")
            assert(len(tree.children) == 2 )

            variables = tree.children[0]
            formula = tree.children[1]

            variables_out = self.visit(variables)
            formula_out = self.visit(formula)

            return "forall (" + variables_out + " | " + formula_out + ")"

        def exists(self, tree):
            """ Translate a exists tree """
            assert(tree.data == "exists")
            assert(len(tree.children) == 2 )

            variables = tree.children[0]
            formula = tree.children[1]

            variables_out = self.visit(variables)
            formula_out = self.visit(formula)

            return "exists (" + variables_out + " | " + formula_out + ")"


        def exists_unique(self, tree):
            """ Translate a exists_unique tree """
            assert(tree.data == "exists_unique")
            assert(len(tree.children) == 2 )

            variables = tree.children[0]
            formula = tree.children[1]

            variables_out = self.visit(variables)
            formula_out = self.visit(formula)

            return "exists_unique (" + variables_out + " | " + formula_out + ")"

        def term_builtins(self, tree):
            assert(tree.data == "term_builtins")

            head, *tail = tree.children

            builtins_out = self.visit(head)

            if tail != None:
                for b in tail:
                    builtins_out += "."
                    builtins_out += self.visit(b)

            return builtins_out

        def predicate(self, tree):
            """ Translate a predicate tree """
            assert(tree.data == "predicate")

            assert(isinstance(tree.children[0],Token ))
            pred_name = str(tree.children[0])
            pred_terms = self.visit(tree.children[1])

            return pred_name + "("+ str(pred_terms) +")"

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

        def arithmetic(self, tree):
            """Translate an arithmetic statement """
            assert(tree.data == "arithmetic")
            assert(len(tree.children) == 1)

            arith_tree = tree.children[0]
            assert(arith_tree.data == "arith")

            #(VARIABLE|NUMBER) ARITH_OP (VARIABLE|NUMBER)

            left = str(arith_tree.children[0])
            op = str(arith_tree.children[1])
            right = str(arith_tree.children[2])

            assert(isinstance(left, str))
            assert(isinstance(op, str))
            assert(isinstance(right, str))

            return left + op + right


        def set(self, tree):
            """Translates a set tree """
            assert(tree.data == "set")

            head, *tail = tree.children

            vars = str(head)

            for var in tail:
                vars += ", " + str(var)


            assert(isinstance(vars, str))
            return "{" + vars + "}"

        def tuple(self, tree):
            """Translates a tuple tree """
            assert(tree.data == "tuple")

            head, *tail = tree.children

            vars = str(head)

            for var in tail:
                vars += ", " + str(var)


            assert(isinstance(vars, str))
            return "(" + vars + ")"


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

            return "\"" + tree.children[0] + "\""

        def variables(self, tree):
            """ Translate a variables tree """
            assert(tree.data == "variables")

            head, *tail = tree.children

            vars = str(head)

            for var in tail:
                vars += ", " + str(var)

            assert(isinstance(vars, str))
            return vars
