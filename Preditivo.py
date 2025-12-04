""" OBS: E'=A, T'=B
E -> TA
A -> +TA
A -> e
T -> FB
B -> *FB
B -> e
F -> (E)
F -> id
"""
import sys
class Preditivo:
  ids = ['a','b','c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
  terminals = ['+','*','(', ')']+ids
  def __init__(self, w, S):
    self.code = list(w)
    self.code.append('$')
    self.idx = -1
    self.pilha = ['$', S]

  def next(self):
    self.idx += 1
    if self.idx >= len(self.code):
      self.idx = len(self.code) - 1
    self.current = self.code[self.idx]
    return self.current

  def push(self, X):
    self.pilha.append(X)
  def pop(self):
    self.log(self.current)
    return self.pilha.pop()

  def run(self):
    x = '#'
    c = self.next()
    while(x!='$'):
      x = self.pop()
      if (x=='E' and ((c in Preditivo.ids) or c == '(')):
        self.push('A')
        self.push('T')
      elif (x=='A' and (c in ('+', ')','$'))):
        if (c=='+'):
          self.push('A')
          self.push('T')
          self.push('+')
      elif (x=='T' and ((c in Preditivo.ids) or c=='(')):
        self.push('B')
        self.push('F')
      elif (x=='B' and (c in ('+', '*', ')','$'))):
        if (c=='*'):
          self.push('B')
          self.push('F')
          self.push('*')
      elif (x=='F' and ((c in Preditivo.ids) or c=='(')):
        if (c=='('):
          self.push(')')
          self.push('E')
          self.push('(')
        if ((c in Preditivo.ids)):
          self.push(c)
      elif x in Preditivo.terminals and c in Preditivo.terminals:
         c = self.next()
      elif x == '$' and c == '$':
         return True
      else:
         return False

  def log(self, c):
     print(f'{self.pilha}:{c}')

if __name__ == "__main__":
    # python.exe .\Codigo.py "((a+a)*a)"
    w = 'a+b+c'
    if len(sys.argv) > 1:
      w = sys.argv[1]

    preditivo = Preditivo(w, 'E')
    reconhece = preditivo.run()
    print(f'Reconhece: {reconhece}')
