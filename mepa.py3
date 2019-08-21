#!/usr/bin/env python3
import sys
import copy
i = 0
rotulos = {}
vetor_comandos = []
class P(object):
    def __init__(self):
        self.M = [None] * 1000
        self.s = 0
        self.D = [None] * 1000

    def INPP(self):
        #print(sys._getframe().f_code.co_name,self.s)
        self.s = -1
        self.D[0] = 0

    def CRCT(self,k):
        #print(sys._getframe().f_code.co_name,self.s)
        self.s = self.s + 1
        self.M[self.s] = k

    def CREN(self,m,n):
        #print(sys._getframe().f_code.co_name,self.s)
        self.s = self.s + 1
        self.M[self.s] = self.D[int(m)] + n
    
    def SOMA(self):
        #print(sys._getframe().f_code.co_name,self.s)
        self.M[self.s - 1] = self.M[self.s - 1] + self.M[self.s] 
        self.s = self.s - 1

    def SUBT(self):
        #print(sys._getframe().f_code.co_name,self.s)
        self.M[self.s - 1] = self.M[self.s - 1] - self.M[self.s] 
        self.s = self.s - 1

    def MULT(self):
        #print(sys._getframe().f_code.co_name,self.s)
        #print(self.M[self.s - 1],self.M[self.s - 1],self.M[self.s])
        self.M[self.s - 1] = self.M[self.s - 1] * self.M[self.s]
        self.s = self.s - 1

    def DIVI(self):
        #print(sys._getframe().f_code.co_name,self.s)
        #print(self.M[self.s - 1],self.M[self.s - 1],self.M[self.s])
        self.M[self.s - 1] = self.M[self.s - 1] // self.M[self.s] 
        self.s = self.s - 1

    def INVR(self):
        #print(sys._getframe().f_code.co_name,self.s)
        self.M[self.s] = -self.M[self.s]

    def NEGA(self):
        #print(sys._getframe().f_code.co_name,self.s)
        self.M[self.s] = 1 - self.M[self.s]

    def RTPR(self,k,n):#retornar do procedimento
        #print(sys._getframe().f_code.co_name,self.s)
        global i
        self.D[int(k)] = self.M[self.s]
        i = self.M[self.s-2]-1
        self.s = self.s - (n+3)

    def CONJ(self):
        #print(sys._getframe().f_code.co_name,self.s)
        if(self.M[self.s -1] == 1 and self.M[self.s] == 1):
            self.M[self.s - 1] = 1
        else:
            self.M[self.s - 1] = 0
        self.s = self.s -1
    
    def DISJ(self):
        #print(sys._getframe().f_code.co_name,self.s)
        if(self.M[self.s -1] == 1 or self.M[self.s] == 1):
            self.M[self.s - 1] = 1
        else:
            self.M[self.s - 1] = 0
        self.s = self.s -1

    def CMME(self):
        #print(sys._getframe().f_code.co_name,self.s)
        if(self.M[self.s - 1] < self.M[self.s]):
            self.M[self.s - 1] = 1
        else:
            self.M[self.s - 1] = 0
        self.s = self.s - 1
    
    def CMMA(self):
        #print(sys._getframe().f_code.co_name,self.s)
        if(self.M[self.s - 1] > self.M[self.s]):
            self.M[self.s - 1] = 1
        else:
            self.M[self.s - 1] = 0
        self.s = self.s - 1
    
    def CMIG(self):
        #print(sys._getframe().f_code.co_name,self.s)
        #print('1==',self.M[self.s - 1],'|| 2==',self.M[self.s],self.M)
        if(self.M[self.s - 1] == self.M[self.s]):
            self.M[self.s - 1] = 1
        else:
            self.M[self.s - 1] = 0
        self.s = self.s - 1

    def CMDG(self):
        #print(sys._getframe().f_code.co_name,self.s)
        if(self.M[self.s - 1] != self.M[self.s]):
            self.M[self.s - 1] = 1
        else:
            self.M[self.s - 1] = 0
        self.s = self.s - 1

    def CMEG(self):
        #print(sys._getframe().f_code.co_name,self.s)
        if(self.M[self.s - 1] <= self.M[self.s]):
            self.M[self.s - 1] = 1
        else:
            self.M[self.s - 1] = 0
        self.s = self.s - 1

    def CMAG(self):#comparar maior ou igual
        #print(sys._getframe().f_code.co_name,self.s)
        if(self.M[self.s - 1] >= self.M[self.s]):
            self.M[self.s - 1] = 1
        else:
            self.M[self.s - 1] = 0
        self.s = self.s - 1

    def DSVF(self,p):
        global i
        #print(sys._getframe().f_code.co_name,self.s,i,p,'-------------')
            #print(self.M)
        global i
        if(self.M[self.s] == 0):
            i = rotulos[p]
        else:
            i = i + 1
        self.s = self.s - 1
        #print(p)

    def DSVS(self,p):
        #print(sys._getframe().f_code.co_name,self.s)
        global i
        i = rotulos[p]
        #print(p)

    def ENPR(self,k):
        #print(sys._getframe().f_code.co_name,self.s)
        self.s = self.s + 1
        self.M[self.s] = self.D[k]
        self.D[k] = self.s + 1

    def ENRT(self,j,n):#entrar no rótulo
        #print(sys._getframe().f_code.co_name,self.s)
        self.s = self.D[j]+n-1

    def NADA(self):
        #print(sys._getframe().f_code.co_name,self.s)
        pass

    def AMEM(self,n):
        #print(sys._getframe().f_code.co_name,self.s)
        self.s = self.s + n

    def DMEM(self,n):
        #print(sys._getframe().f_code.co_name,self.s)
        self.s = self.s - n
        if self.s <= -2:
            print('Linha %d: RunTime error. Stack underflow' %(i+1))
            sys.exit(0)
    
    def CRVL(self,m,n):
        global i
        #print(sys._getframe().f_code.co_name,self.s,i)
        #print(self.M)
        self.s = self.s + 1
        #if(self.s == 8):
            #print(m,n,self.D)
        self.M[self.s] = self.M[self.D[int(m)]+n]

    def ARMI(self,m,n):#armazenar indiretamente
        #print(sys._getframe().f_code.co_name,self.s)
        self.M[self.M[self.D[int(m)]+n]] = self.M[self.s]
        self.s = self.s -1

    def ARMZ(self,m,n):
        #print(sys._getframe().f_code.co_name,self.s)
        self.M[self.D[int(m)]+n] = self.M[self.s]
        self.s = self.s - 1

    def CHPR(self,p,m):#chamar procedimento
        #print(sys._getframe().f_code.co_name,self.s)
        global i
        self.M[self.s+1] = i + 1
        self.M[self.s+2] = m
        self.s = self.s + 2
        i = rotulos[p]
        #print(p)

    def IMPR(self):
        #print(sys._getframe().f_code.co_name,self.s)
        global i
        #print(self.M,i)
        print(self.M[self.s])
        self.s = self.s - 1

    def LEIT(self):
        #print(sys._getframe().f_code.co_name,self.s)
        self.s = self.s + 1
        self.M[self.s] = int(input())


class Parser(object):
    def __init__(self,entrada):
        self.posicao = 0
        self.entrada = entrada
        self.char_atual = self.entrada[self.posicao]

    def avançar(self):
        self.posicao += 1
        if self.posicao > len(self.entrada) - 1:
            self.char_atual = None
        else:
            self.char_atual = self.entrada[self.posicao]

    def espaco_branco(self):
        while(self.char_atual != None and (self.char_atual.isspace() or self.char_atual == ',')):
            self.avançar()

    def id(self):
        if(self.char_atual.isspace() or self.char_atual == ','):
            self.espaco_branco()
        resultado = ''
        while(self.char_atual != None and (self.char_atual.isalnum() or self.char_atual == '-')):
            resultado += self.char_atual
            self.avançar()
            if self.char_atual == ':':
                resultado += self.char_atual
                self.avançar()
        return resultado

def main():
    file_name = sys.argv[1]
    flag = True

    fp = open(file_name)
    contents = fp.read()
    #contents = " INPP AMEM 2 DSVS R00 R01: ENPR 1 AMEM 1 DSVS R02 R02: NADA CRVL 1, -4 CRCT 1 CMMA DSVF R04 CRVL 1, -4 CRCT 1 SUBT CHPR R01, 1 DSVS R03 R04: NADA CRCT 1 ARMZ 0, 1 R03: NADA CRVL 0, 1 ARMZ 1, 0 CRVL 1, 0 CRVL 1, -4 MULT ARMZ 0, 1 DMEM 1 RTPR 1, 1 R00: NADA LEIT ARMZ 0, 0 CRVL 0, 0 CHPR R01, 0 CRVL 0, 0 IMPR CRVL 0, 1 IMPR DMEM 2 PARA"
    p = P()
    parser = Parser(contents)

                
    while(True):
        if(flag):
            res = parser.id()
        else:
            flag = True
        if ':' in res:
            res_copy = copy.deepcopy(res)
            id_copy = parser.id()
            if(id_copy != 'NADA'):
                vetor_comandos.append([res_copy,'NADA'])
                flag = False
                res = id_copy
            else:
                vetor_comandos.append([res_copy,id_copy])
            rotulos[vetor_comandos[(len(vetor_comandos) - 1)][0][:-1]] = (len(vetor_comandos) - 1)
        elif res == 'CRVL' or res == 'ARMZ' or res == 'CHPR' or res == 'CREN' or res == 'ENRT' or res == 'RTPR':
            vetor_comandos.append([res,parser.id(),parser.id()])
        elif res == 'CRCT' or res == 'DSVF' or res == 'DSVS' or res == 'AMEM' or res == 'DMEM' or res == 'ENPR'  :
            vetor_comandos.append([res,parser.id()])
        else:
            vetor_comandos.append(res)
        if(res == 'PARA'):
            break
    #print(vetor_comandos)

    global i
    while(True):
        #print(len(vetor_comandos[i]))
        #print(i)
        if len(vetor_comandos[i]) > 3:
            method = getattr(p,vetor_comandos[i])
            method()
            i += 1
        elif len(vetor_comandos[i]) == 2:
            if ':' in vetor_comandos[i][0]:
                i += 1
            elif vetor_comandos[i][0] == 'DSVF' or vetor_comandos[i][0] == 'DSVS':
                if(vetor_comandos[i][1] not in rotulos):
                    print('Linha %d: RunTime error rotulo %s invalido' %(i+1,vetor_comandos[i][1]))
                    sys.exit(0)
                method = getattr(p,vetor_comandos[i][0])
                method(vetor_comandos[i][1])
            else:
                method = getattr(p,vetor_comandos[i][0])
                method(int(vetor_comandos[i][1]))
                i += 1
        elif len(vetor_comandos[i]) == 3:
            method = getattr(p,vetor_comandos[i][0])
            method(vetor_comandos[i][1],int(vetor_comandos[i][2]))
            if(type(i) == int):
                i += 1
        if(type(i) == int):        
            if(vetor_comandos[i] == 'PARA'):
                break
main()