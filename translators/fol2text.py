#!/usr/bin/python
# -*- coding: utf-8 -*-

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

    def atomic_formula(self, tree):
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
        assert(len(tree.children) == 2)

        eq_left, eq_right = self.binary_infix(tree)

        return eq_left + " == " + eq_right

    def not_equals(self, tree):
        """ Translate a not equals tree """
        assert(tree.data == "not_equals")
        assert(len(tree.children) == 2)

        eq_left, eq_right = self.binary_infix(tree)

        return eq_left + " != " + eq_right

    def in_form(self, tree):
        """ Translate an in tree """
        assert(tree.data == "in_form")
        assert(len(tree.children) == 2)

        in_left, in_right = self.binary_infix(tree)

        return in_left + " in " + in_right

    def not_in(self, tree):
        """ Translate a not in tree """
        assert(tree.data == "not_in")
        assert(len(tree.children) == 2)

        in_left, in_right = self.binary_infix(tree)

        return in_left + " !in " + in_right

    def leq(self, tree):
        """ Translate a leq tree """
        assert(tree.data == "leq")
        assert(len(tree.children) == 2)

        left, right = self.binary_infix(tree)

        return left + " <= " + right

    def geq(self, tree):
        """ Translate a geq tree """
        assert(tree.data == "geq")
        assert(len(tree.children) == 2)

        left, right = self.binary_infix(tree)

        return left + " >= " + right

    def lt(self, tree):
        """ Translate a lt tree """
        assert(tree.data == "lt")
        assert(len(tree.children) == 2)

        left, right = self.binary_infix(tree)

        return left + " < " + right

    def gt(self, tree):
        """ Translate a gt tree """
        assert(tree.data == "gt")
        assert(len(tree.children) == 2)

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
        assert(len(tree.children) == 2)

        and_left, and_right = self.binary_infix(tree)

        return and_left + " and " + and_right

    def or_form(self, tree):
        """ Translate a or tree """
        assert(tree.data == "or_form")
        assert(len(tree.children) == 2)

        or_left, or_right = self.binary_infix(tree)

        return or_left + " or " + or_right

    def iff(self, tree):
        """ Translate a iff tree """
        assert(tree.data == "iff")
        assert(len(tree.children) == 2)

        iff_left, iff_right = self.binary_infix(tree)

        return iff_left + " <=> " + iff_right

    def forall(self, tree):
        """ Translate a forall tree """
        assert(tree.data == "forall")
        assert(len(tree.children) == 2)

        variables = tree.children[0]
        formula = tree.children[1]

        variables_out = self.visit(variables)
        formula_out = self.visit(formula)

        return "forall (" + variables_out + " | " + formula_out + ")"

    def exists(self, tree):
        """ Translate a exists tree """
        assert(tree.data == "exists")
        assert(len(tree.children) == 2)

        variables = tree.children[0]
        formula = tree.children[1]

        variables_out = self.visit(variables)
        formula_out = self.visit(formula)

        return "exists (" + variables_out + " | " + formula_out + ")"

    def exists_unique(self, tree):
        """ Translate a exists_unique tree """
        assert(tree.data == "exists_unique")
        assert(len(tree.children) == 2)

        variables = tree.children[0]
        formula = tree.children[1]

        variables_out = self.visit(variables)
        formula_out = self.visit(formula)

        return "exists_unique (" + variables_out + " | " + formula_out + ")"


    def formula_variables_part(self, tree):
        """ Translate a formula_variables_part tree """
        assert(tree.data == "formula_variables_part")
        assert(len(tree.children) == 2)

        vars_extract, sets_extract = tree.children

        vars_out = self.visit(vars_extract)

        if isinstance(sets_extract, Token):
            sets_out = self.make_string(sets_extract)
        elif isinstance(sets_extract, Tree):
            sets_out = self.visit(sets_extract)

        return vars_out + " in " + sets_out

    def term_builtins(self, tree):
        assert(tree.data == "term_builtins")

        head, *tail = tree.children

        builtins_out = ""
        
        if isinstance(head, Token):
            builtins_out += self.translate_builtin_token(head)
        elif isinstance(head, Tree):
            builtins_out += self.visit(head)

        
        if tail != None:
            for b in tail:
                builtins_out += "."
                if isinstance(b, Token):
                    builtins_out += str(b)
                elif isinstance(b, Tree):
                    builtins_out += self.visit(b)

        return builtins_out

    def predicate(self, tree):
        """ Translate a predicate tree """
        assert(tree.data == "predicate")

        assert(isinstance(tree.children[0], Token))
        pred_name = str(tree.children[0])
        pred_terms = self.visit(tree.children[1])

        return pred_name + "(" + str(pred_terms) + ")"


    def set(self, tree):
        """Translates a set tree """
        assert(tree.data == "set")

        print("\n\nSET")

        head, *tail = tree.children

        vars = str(self.visit(head))

        for var in tail:
            vars += ", " + str(self.visit(var))

        assert(isinstance(vars, str))
        return "{" + vars + "}"

    def empty_set(self, tree):
        """ Translates an empty_set tree """
        assert(tree.data == "empty_set")

        return "{}"

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

        assert(isinstance(tree.children[0], Token))
        func_name = str(tree.children[0])
        func_args = self.visit(tree.children[1])

        return func_name + "(" + str(func_args) + ")"

    def function_application(self, tree):
        """ Translate a function_application tree """
        assert(tree.data == "function_application")
        assert(len(tree.children) == 2)

        name, terms = tree.children

        print("\n\nFunc App = " + str(tree.children))

        name_out = self.variable_reference(name)
        terms = self.visit(tree.children[1])

        return str(name_out) + "(" + str(terms) + ")"

    
    def function_declaration(self, tree):
        """ Translates a function_declaration tree """
        assert(tree.data == "function_declaration")
        assert(len(tree.children) == 2)

        inputs, outputs = tree.children

        inputs_out = ""
        head, *tail = inputs.children

        print("\n\n Func Decl Head = " + str(head))

        if isinstance(head, Token):
            inputs_out += self.translate_builtin_token(str(head))
        elif isinstance(head, Tree):         
            inputs_out += self.translate_builtin_token(self.vist(head)[0])

        for input in tail:
            assert(isinstance(input, Token))
            inputs_out += " X " + self.translate_builtin_token(str(input))

        outputs_out = ""
        head, *tail = outputs.children
        outputs_out += self.translate_builtin_token(str(head))

        for input in tail:
            outputs_out += " X " + \
                self.translate_builtin_token(str(input))

        return inputs_out + " -> " + outputs_out

    def variable_reference(self, tree):
        """Translates a reference to a variable, which may have an
         'in.' or 'out.' decoration. """
        assert(tree.data == "variable_reference")

        numberOfChildren = len(tree.children)
        assert(numberOfChildren in {1, 2})

        print("\n\n Var Ref: " + str(tree))
        print("children = " + str(numberOfChildren))

        if numberOfChildren == 1:
            assert(isinstance(tree.children[0], Token))
            print("1 child")
            return self.translate_builtin_token(tree.children[0])
        else:
            print("2 child")
            decoration, name = tree.children
            decoration_out = self.visit(decoration)
            
            assert(isinstance(name, Token))

            return str(decoration_out) + self.translate_builtin_token(str(name))
            # This seems to be escaped elsewhere.

    def string_literal(self, tree):
        """ Translate a string literal tree """
        assert(tree.data == "string_literal")

        return "\"" + tree.children[0] + "\""

    def variables(self, tree):
        """ Translate a variables tree """
        assert(tree.data == "variables")
        
        head, *tail = tree.children

        if isinstance(head, Tree):
            vars = str(self.visit(head))
        else:
            vars = str(head)

        for var in tail:
            if isinstance(head, Tree):
                vars += ", " + str(self.visit(var))
            else:
                vars += ", " + str(var)

        assert(isinstance(vars, str))
        return vars


    def translate_builtin_token(self, term):
        print("\n\n T Built in Token term = " + term)
        if self.make_string(term) == "REAL":
            return "R"
        elif self.make_string(term) == "INTEGER":
            return "Z"
        elif self.make_string(term) == "NATURAL":
            return "N"
        elif self.make_string(term) == "BOOL":
            return "B"
        else:
            return term
