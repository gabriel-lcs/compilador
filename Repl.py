from Lexer import Lexer
from cmd import Cmd
from recursivo_desc import RecDescendente

class Repl(Cmd):
    prompt = 'UFC - Gabriel> '
    intro = "Bem vindo!\nDigite\n :h para ajuda\n :q para sair e imprimir o assembly\n :s para um exemplo!"

    def do_exit(self, inp):
        return True
    def help_exit(self):
        print('Digite\n :q para sair\n :s para um exemplo!')
        return False
    def emptyline(self): # Disabilita repeticao do ultimo comando
        pass

    def do_s(self):
        print("Samples:")
        print('    1+3*8*(1+2)')
        #print('    let num = 10')
        #print('    num^2')
        #print('    (num+1)*2')
        #print('    let ufc = \"ufc\"')
        #print('    ufc + \"-2025\"')
        return False

    def default(self, linha): # cada linha do prompty cai aqui
        if linha == ':q':
            return self.do_exit(linha)
        elif linha == ':h':
            return self.help_exit()
        elif linha == ':s':
            return self.do_s()
    
        print(f'Linha digitada: {linha}')
        self.analisador(linha)
        
        return False

    do_EOF = do_exit
    help_EOF = help_exit

    def run(self, linha):
        # Gerar tokens
        lexer = Lexer(linha)
        tokens, error = lexer.makeTokens()
        if error:
            print(error)
            return None, error
        print(f'Lexer: {tokens}')

        # Gerar AST
        #astInfo = Parser.instance().Parsing(tokens)
        #semanticNode, error = astInfo.node, astInfo.error

        #if error or not isinstance(semanticNode, Visitor):
        #    return None, error
        #print(f'Parser: {semanticNode}')
        parser = RecDescendente(tokens)
        semanticNode, error = parser.start()
        return semanticNode, error
        #return tokens, error

    def analisador(self, linha):
        resultado, error = self.run(linha)
        if error:
            print(f'Log de Erro: {error}')
        else: print(f'{resultado}')
