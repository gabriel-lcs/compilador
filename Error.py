class Error:
    runTimeError = "RunTime Error"
    parserError = "Parser Error"
    lexerError = "Lexer Error"
    
    def __init__(self, msg):
        self.msg = msg

    def __repr__(self):
        return f'({self.msg})'

    def printMsg(self):
        return self
    
    @staticmethod
    def singletonMsg(obj):
        class_name = Error.classNameOf(obj)
        return f"Singleton em {class_name}\n Para corrigir:\n - Onde condificou \'{class_name}()\' use: '{class_name}"
    
    @staticmethod
    def classNameOf(obj):
        className = type(obj).__name__
        return str(className)
