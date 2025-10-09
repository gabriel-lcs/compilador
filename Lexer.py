from Consts import Consts
from Token import Token
from Error import Error

class Lexer:
    def __init__(self, source_code):
        self.code = source_code
        self.current = None
        self.indice, self.coluna, self.linha = -1, -1, 0
        self.__advance()

    def __advance(self):
        self.__advanceCalc(self.current)
        if self.indice < len(self.code):
            self.current = self.code[self.indice]
        else:
            self.current = None

    def __advanceCalc(self, _char=None):
        self.indice += 1
        self.coluna += 1
        if self.current == '\n':
            self.coluna = 0
            self.linha += 1
        return self

    def makeTokens(self):
        tokens = []
        while self.current != None:
            if self.current in ' \t':
                pass
            elif self.current == Consts.PLUS:
                tokens.append(Token(Consts.PLUS))
            elif self.current == Consts.MINUS:
                tokens.append(Token(Consts.MINUS))
            elif self.current == Consts.MUL:
                tokens.append(Token(Consts.MUL))
            elif self.current == Consts.DIV:
                tokens.append(Token(Consts.DIV))
            elif self.current == Consts.LPAR:
                tokens.append(Token(Consts.LPAR))
            elif self.current == Consts.RPAR:
                tokens.append(Token(Consts.RPAR))
            elif self.current == Consts.EQ:
                tokens.append(Token(Consts.EQ))
            elif self.current in Consts.DIGITOS:
                tokens.append(self.__makeNumber())
                continue
            elif self.current == '"':
                tk_string = self.__MakeString()
                if self.current != '"':
                    return tokens, Error(f"{Error.lexerError}: esperando \'\"\'")
                self.__advance()
                tokens.append(tk_string)
                
                """
            elif self.current == '"':
                self.__advance()
                string = ""
                while (self.current != '"'):
                    string += str(self.current)
                    self.__advance()

                tokens.append(Token(Consts.STRING, string))   
                self.__advance()
                """

            else:
                if (self.current.isalpha()):
                    id = ""
                    while str(self.current) in Consts.LETRAS_DIGITOS:
                        id += str(self.current)
                        self.__advance()
                    tokens.append(Token(Consts.ID, id))
                else:
                    return tokens, Error(Error.lexerError)
        
            self.__advance()
        tokens.append(Token(Consts.EOF))
        
        return tokens, None

    def __makeNumber(self):
        strNum = ''
        conta_ponto = 0

        while self.current != None and self.current in Consts.DIGITOS + '.':
            if self.current == '.':
                if conta_ponto == 1: break
                conta_ponto += 1
            strNum += self.current
            self.__advance()

        if conta_ponto == 0:
            return Token(Consts.INT, int(strNum))    
        return Token(Consts.FLOAT, float(strNum))

    def __MakeString(self):
        stri = ""
        byPass = False
        self.__advance()
        specialChars = {'n': '\n', 't': '\t'}
        while (self.current != None and (self.current != '"' or byPass)):
            if (byPass):
                c = specialChars.get(self.current, self.current)
                stri += c
                byPass = False
            else:
                if (self.current == '\\'):
                    byPass = True
                else:
                    stri += self.current

            self.__advance()

        return Token(Consts.STRING, stri)