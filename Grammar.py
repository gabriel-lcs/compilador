from Consts import Consts
from Error import Error
from SemanticVisitor import *

class Grammar:
    def __init__(self, parser):
        self.parser = parser

    def Rule(self):
        return self.GetParserManager().fail(f"{Error.parserError}: Implementar suas regras de producao (Heranca de Grammar)!")

    def CurrentToken(self):
        return self.parser.CurrentTok()

    def NextToken(self):
        return self.parser.NextTok()

    def GetParserManager(self):
        return self.parser.Manager()

    @staticmethod
    def StartSymbol(parser): # Start Symbol S from Grammar G(V, T, S, P)
        resultado = Exp(parser).Rule()
        if parser.CurrentTok().type != Consts.EOF: return resultado.fail(f"{Error.parserError}: Erro sintatico")
        return resultado

class Exp(Grammar): # A variable from Grammar G
    def Rule(self):
        pr = self.GetParserManager() # <Term> ((MINUS | PLUS) <Term>)*
        node = pr.registry(NoOpBinaria.Perform(Term(self.parser), (Consts.PLUS, Consts.MINUS)))
        if pr.error:
            return pr.fail(f"{Error.parserError}: Esperado a '{Consts.INT}', '{Consts.FLOAT}', '{Consts.PLUS}', '{Consts.MINUS}', '{Consts.LPAR}'")
        return pr.success(node)

class Term(Grammar): # A variable from Grammar G
    def Rule(self): # <Factor> ((MUL | DIV) <Factor>)*
        return NoOpBinaria.Perform(Factor(self.parser), (Consts.MUL, Consts.DIV))

class Factor(Grammar): # A variable from Grammar G
    def Rule(self):
        return Atom(self.parser).Rule() # <Atom>

class Atom(Grammar): # A variable from Grammar G
    def Rule(self): # <Atom> ::= INT | FLOAT | LPAR <Exp> RPAR
        ast = self.GetParserManager()
        tok = self.CurrentToken()
        if tok.type in (Consts.INT, Consts.FLOAT):
            self.NextToken()
            return ast.success(NoNumber(tok))

        elif tok.type == Consts.LPAR:
            self.NextToken()
            exp = ast.registry(Exp(self.parser).Rule())
            if ast.error: return ast
            if self.CurrentToken().type == Consts.RPAR:
                self.NextToken()
                return ast.success(exp)
            return ast.fail(f"{Error.parserError}: Esperando por '{Consts.RPAR}'")

        return ast.fail(f"{Error.parserError}: Esperado por '{Consts.INT}', '{Consts.FLOAT}', '{Consts.ID}', '{Consts.LET}', '{Consts.PLUS}', '{Consts.MINUS}', '{Consts.LPAR}', '{Consts.GRAPH}'")
