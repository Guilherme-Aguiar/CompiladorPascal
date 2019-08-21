#!/usr/bin/env python3
import sys
import copy
import os

INTEIRO, MAIS, MENOS, VEZES, DIV,EPAREN,DPAREN, FIM, PTVIRG, PONTO, ID, VIRGULA, DOISPT, DPIGUAL = 'INTEIRO', 'MAIS', 'MENOS','VEZES','DIV','EPAREN','DPAREN', 'FIM','PTVIRG', 'PONTO', 'ID', 'VIRGULA', 'DOISPT', 'DPIGUAL'
IGUAL, MAIOR, MENOR, MAIORIGUAL, MENORIGUAL, NAOIGUAL = 'IGUAL', 'MAIOR','MENOR', 'MAIORIGUAL', 'MENORIGUAL', 'NAOIGUAL'

class Token(object):
    def __init__(self,tipo,valor):
        self.tipo = tipo
        self.valor = valor


PALAVRAS_RESERVADAS = {
    'program': Token('program', 'program'),
    'label': Token('label','label'),
    'var': Token('var','var'),
    'procedure': Token('procedure','procedure'),
    'function': Token('function','function'),
    'begin': Token('begin','begin'),
    'end': Token('end','end'),
    'not': Token('not','not'),
    'and': Token('and','and'),
    'or': Token('or','or'),
    'div': Token('div','div'),
    'goto': Token('goto','goto'),
    'if': Token('if','if'),
    'then': Token('then','then'),
    'else': Token('else','else'),
    'do': Token('do','do'),
    'while': Token('while','while'),
    'integer': Token('integer','integer'),
    'real': Token('real','real'),
    'boolean': Token('boolean','boolean'),
    'read': Token('read','read'),
    'write': Token('write','write')
}    
class GeradorMepa(object):
    def __init__(self):
        self.instrucoes_mepa = ''
        self.variaveis = {}
        self.numero_rotulo = 1
        self.estruturas_rotulos = {}
    def insere_instrucao(self,token,primeiro_parametro='',segundo_parametro=''):
        if token == 'program':
            self.instrucoes_mepa += 'INPP' + '\n'
        elif token == 'amen':
            self.instrucoes_mepa += 'AMEM ' + str(primeiro_parametro) + '\n'
        elif token == 'dsvs':
            if primeiro_parametro == '0':
                self.instrucoes_mepa += 'DSVS R00' + '\n'
            else:
                if(self.numero_rotulo <= 9):
                    self.instrucoes_mepa += 'DSVS R0' + str(self.numero_rotulo) + '\n'
                else:
                    self.instrucoes_mepa += 'DSVS R' + str(self.numero_rotulo) + '\n' 
        elif token == 'rotulo':
            if primeiro_parametro == '0':
                self.instrucoes_mepa += 'R00: NADA' + '\n'
            else:
                if(self.numero_rotulo <= 9):
                    self.instrucoes_mepa += 'R0' + str(self.numero_rotulo) + ': NADA\n'
                    self.numero_rotulo += 1
                else:
                    self.instrucoes_mepa += 'R' + str(self.numero_rotulo) + ': NADA\n'
                    self.numero_rotulo += 1
        elif token == 'leit':
            self.instrucoes_mepa += 'LEIT\n'
        elif token == 'impr':
            self.instrucoes_mepa += 'IMPR\n'
        elif token == 'armz':
            self.instrucoes_mepa += 'ARMZ ' + str(primeiro_parametro) +', '+ str(segundo_parametro) + '\n'
        elif token == 'crct':
            self.instrucoes_mepa += 'CRCT ' + str(primeiro_parametro) + '\n'
        elif token == 'crvl':
            self.instrucoes_mepa += 'CRVL ' + str(primeiro_parametro) +', '+str(segundo_parametro) +'\n'
        elif token == 'dsvf':
            self.instrucoes_mepa += 'DSVF '
            if(self.numero_rotulo <= 9):
                self.instrucoes_mepa += 'R0' + str(self.numero_rotulo) + '\n'
            else:
                self.instrucoes_mepa += 'R' + str(self.numero_rotulo) + '\n'
        elif token == 'enpr':
            self.instrucoes_mepa += 'ENPR ' + str(primeiro_parametro) + '\n'
        elif token == 'chpr':
            self.instrucoes_mepa += 'CHPR ' + str(primeiro_parametro) + ', ' + str(segundo_parametro) + '\n'
        elif token == 'dmen':
            self.instrucoes_mepa += 'DMEM ' + primeiro_parametro + '\n'
        elif token == 'para':
            self.instrucoes_mepa += 'PARA'
                 
        #print(self.instrucoes_mepa,'<-',self.numero_rotulo)
    def escreve_mepa(self):
        f = open("teste.mepa", "w")
        f.write(self.instrucoes_mepa)
        f.close()
class Interpretador(object):
    def __init__(self,entrada):
        self.entrada = entrada
        self.posicao = 0
        self.char_atual = self.entrada[self.posicao]
        self.token_atual = self.proximo_token(0)
        self.token_anterior = ''
        self.char_anterior = ''
        self.posicao_anterior = ''
        self.variaveis_declaradas = []
        self.variaveis_declaradas_procedimento = []
        self.funcoes_declaradas = []
        self.procedimentos_declarados = ['write','read']
        self.variaveis_inteiras = []
        self.variaveis_reais = []
        self.variaveis_booleanas = []
        self.variaveis_em_analise = ''
        self.mepa = GeradorMepa()
        self.is_read = False
        self.n_read = 0
        self.is_write = False
        self.n_write = 0
        self.armz_auxiliar = ''
        self.is_assign = False
        self.cond_auxiliar = ''
        self.is_while = False
        self.op_simples_auxiliar = ''
        self.op_termo_auxiliar = ''
        self.n_procedure = 0
        self.is_procedure = False
        self.n_parametros = 0

    def error(self):
        #raise Exception("failed")
        print("Rejeito")
        sys.exit()

    def avançar(self):
        self.posicao += 1
        if self.posicao > len(self.entrada) - 1:
            self.char_atual = None
        else:
            self.char_atual = self.entrada[self.posicao]

    def espaco_branco(self):
        while(self.char_atual != None and self.char_atual.isspace()):
            self.avançar()

    def numeros(self):
        eFloat = False
        numero_total = ''
        while(self.char_atual != None and self.char_atual.isdigit()):
            numero_total += self.char_atual
            self.avançar()
            if(self.char_atual == '.'):
                numero_total += self.char_atual
                self.avançar()
                eFloat = True
        if(eFloat):
            return float(numero_total)
        else:
            return int(numero_total)
    
    def id(self):
        resultado = ''
        while(self.char_atual != None and self.char_atual.isalnum()):
            resultado += self.char_atual
            self.avançar()
        token = PALAVRAS_RESERVADAS.get(resultado, Token(ID, resultado))
        return token

    def proximo_token(self,n='1'):
        if(n != 0):
            self.token_anterior = copy.deepcopy(self.token_atual)
            self.char_anterior = copy.deepcopy(self.char_atual)
            self.posicao_anterior = copy.deepcopy(self.posicao)


        if(self.posicao > len(self.entrada) - 1):
            return Token(FIM,'FIM')

        self.char_atual = self.entrada[self.posicao]

        if(self.char_atual.isspace()):
            self.espaco_branco()

        #print(self.posicao,"||",(len(self.entrada) - 1))

        if(self.char_atual == None):
            return Token(FIM,'FIM')

        if(self.char_atual.isdigit()):
            return Token(INTEIRO, self.numeros())

        if(self.char_atual.isalpha()):
            return self.id()

        if(self.char_atual == '+'):
            self.posicao += 1
            return Token(MAIS, '+')

        if(self.char_atual == '-'):
            self.posicao += 1
            return Token(MENOS, '-')

        if(self.char_atual == '*'):
            self.posicao += 1
            return Token(VEZES, '*')

        if(self.char_atual == '/'):
            self.posicao += 1
            return Token(DIV, '/')

        if(self.char_atual == '('):
            self.posicao += 1
            return Token(EPAREN, '(')

        if(self.char_atual == ')'):
            self.posicao += 1
            return Token(DPAREN, ')')

        if(self.char_atual == ';'):
            self.posicao += 1
            return Token(PTVIRG, ';')
        
        if(self.char_atual == ','):
            self.posicao += 1
            return Token(VIRGULA, ',')

        if(self.char_atual == '.'):
            self.posicao += 1
            return Token(PONTO, '.')

        if(self.char_atual == ':'):
            if(self.entrada[self.posicao+1] == '='):
                self.posicao+= 2
                return Token(DPIGUAL, ':=')
            else:
                self.posicao += 1
                return Token(DOISPT, ':')

        if(self.char_atual == '='):
            self.posicao += 1
            return Token(IGUAL, '=')

        if(self.char_atual == '>'):
            if(self.entrada[self.posicao+1] == '='):
                self.posicao +=2
                return Token(MAIORIGUAL, '>=')
            self.posicao += 1
            return Token(MAIOR, '>')

        if(self.char_atual == '<'):
            if(self.entrada[self.posicao+1] == '='):
                self.posicao +=2
                return Token(MENORIGUAL, '<=')
            elif(self.entrada[self.posicao+1] == '>'):
                self.posicao += 2
                return Token(NAOIGUAL, '<>')
            self.posicao += 1
            return Token(MENOR, '<')
        
        self.error()

    def programa(self):
        self.consome('program')
        self.mepa.insere_instrucao(self.token_anterior.valor)
        self.consome(ID)
        self.consome(EPAREN)
        while(self.token_atual.tipo in (ID)):
            self.consome(ID)
            if(self.token_atual.tipo == VIRGULA):
                self.consome(VIRGULA)
                if(self.token_atual.tipo != ID):
                    self.error()
        self.consome(DPAREN)
        self.consome(PTVIRG)
        self.bloco()
        if(self.mepa.variaveis):
            self.mepa.insere_instrucao('dmen',str(len(self.mepa.variaveis[str(self.n_procedure)])))
        self.mepa.insere_instrucao('para')
        #print(self.mepa.instrucoes_mepa)
        if(self.token_atual.tipo != 'FIM'):
            self.error()
        self.mepa.escreve_mepa()
    
    def bloco(self):
        if(self.token_atual.tipo == 'label'):
            self.bloco_label()
        if(self.token_atual.tipo == 'var'):
            self.bloco_var()
        if(not self.is_procedure):
            self.mepa.insere_instrucao('dsvs','0')
        if(self.token_atual.tipo == 'procedure'):
            self.mepa.insere_instrucao('rotulo')
            self.bloco_procedure()
            self.bloco2()
        if(self.token_atual.tipo == 'function'):
            self.bloco_function()
            self.bloco2()
        self.consome('begin')
        if(not self.is_procedure):
            self.mepa.insere_instrucao('rotulo','0')
        else:
            self.mepa.insere_instrucao('rotulo')
        while(self.token_atual.tipo not in 'end'):
            self.comando()
            self.token_atual = self.proximo_token()
            if(self.token_anterior.valor != 'end'):
                self.token_atual = self.token_anterior
                self.char_atual = self.char_anterior
                self.posicao = self.posicao_anterior
                self.consome(PTVIRG)   
            else:
                self.token_atual = self.token_anterior
                self.char_atual = self.char_anterior
                self.posicao = self.posicao_anterior
        self.token_atual = self.proximo_token(0)
        self.token_atual = self.proximo_token(0)
        if(self.token_atual.valor == 'FIM'):
            self.token_atual = self.token_anterior
            self.char_atual = self.char_anterior
            self.posicao = self.posicao_anterior
            self.consome('end')
            self.consome(PONTO)
        else:
            self.token_atual = self.token_anterior
            self.char_atual = self.char_anterior
            self.posicao = self.posicao_anterior
            self.consome('end')

        

    def bloco2(self):
        if(self.token_atual.tipo == 'procedure'):
            self.bloco_procedure()
            self.bloco2()
        if(self.token_atual.tipo == 'function'):
            self.bloco_function()
            self.bloco2()


    def bloco_label(self):
        self.consome('label')
        while(self.token_atual.tipo in INTEIRO):
            self.consome(INTEIRO)
            if(self.token_atual.tipo == VIRGULA):
                self.consome(VIRGULA)
        self.consome(PTVIRG)  

    def bloco_var(self):
        self.consome('var')
        outro_contador = 0
        contador_de_variaveis = 0
        while(self.token_atual.tipo in (ID)):
            self.variaveis_declaradas.append(self.token_atual.valor)
            if(str(self.n_procedure) not in self.mepa.variaveis):
                self.mepa.variaveis[str(self.n_procedure)] = {}
            self.mepa.variaveis[str(self.n_procedure)][self.token_atual.valor] = str(outro_contador)
            #print(self.mepa.variaveis)
            var_atual = self.token_atual.valor
            self.consome(ID)
            contador_de_variaveis += 1
            outro_contador += 1
            if(self.token_atual.tipo == VIRGULA):
                self.consome(VIRGULA)
                continue
            self.consome(DOISPT)
            if(self.token_atual.valor == 'integer'):
                self.variaveis_inteiras.append(var_atual)
                self.consome('integer')
            elif(self.token_atual.valor == 'real'):
                self.variaveis_reais.append(var_atual)
                self.consome('real')
            elif(self.token_atual.valor == 'boolean'):
                self.variaveis_booleanas.append(var_atual)
                self.consome('boolean')
            #print(self.variaveis_inteiras,self.variaveis_reais)
            self.consome(PTVIRG)
            self.mepa.insere_instrucao('amen',contador_de_variaveis)
            if(self.is_procedure):
                self.mepa.insere_instrucao('dsvs')
            contador_de_variaveis = 0
    
    def bloco_procedure(self):
        self.is_procedure = True
        self.consome('procedure')
        self.n_procedure += 1
        self.mepa.insere_instrucao('enpr',self.n_procedure)
        self.procedimentos_declarados.append(self.token_atual.valor)
        self.mepa.estruturas_rotulos[self.token_atual.valor] = 'R0' + str(self.mepa.numero_rotulo-1)
        self.consome(ID)
        if(self.token_atual.tipo == EPAREN):
            self.parametros_formais()
        self.consome(PTVIRG)
        self.bloco()
        self.consome(PTVIRG)
        self.mepa.insere_instrucao('dmen',str(len(self.mepa.variaveis[str(self.n_procedure)])))
        self.mepa.instrucoes_mepa += "RTPR " + str(self.n_procedure) + ', ' + str(self.n_parametros) + '\n'
        self.is_procedure = False
        self.n_procedure -= 1

    def bloco_function(self):
        self.consome('function')
        self.funcoes_declaradas.append(self.token_atual.valor)
        self.consome(ID)
        if(self.token_atual.tipo == EPAREN):
            self.parametros_formais()
        else:
            self.n_parametros = 0
        self.consome(DOISPT)
        self.consome(ID)
        self.consome(PTVIRG)
        self.bloco()
        self.consome(PTVIRG)


    def parametros_formais(self):
        self.consome(EPAREN)
        while(self.token_atual.tipo in (ID,'var')):
            if(self.token_atual.tipo == 'var'):
                self.consome('var')
            self.variaveis_declaradas.append(self.token_atual.valor)
            self.consome(ID)
            if(self.token_atual.tipo == VIRGULA):
                self.consome(VIRGULA)
                continue
            self.consome(DOISPT)
            if(self.token_atual.tipo == ID):
                self.consome(ID)
            elif(self.token_atual.tipo == 'integer'):
                self.consome('integer')
            elif(self.token_atual.tipo == 'real'):
                self.consome('real')
            elif(self.token_atual.tipo == 'boolean'):
                self.consome('boolean')
            if(self.token_atual.tipo == PTVIRG):
                self.consome(PTVIRG)
            self.n_parametros += 1
        self.consome(DPAREN)
    
    def comando(self):
        if(self.token_atual.tipo == INTEIRO):
            self.consome(INTEIRO)
            self.consome(DOISPT)
        self.comando_sem_rotulo()
    
    def comando_sem_rotulo(self):
        if(self.token_atual.tipo in (ID,'read','write')):
            self.comando_sem_rotulo_id()
        elif(self.token_atual.tipo == 'goto'):
            self.consome('goto')
            self.consome(INTEIRO)
        elif(self.token_atual.tipo == 'begin'):
            self.comando_sem_rotulo_begin()
        elif(self.token_atual.tipo == 'if'):
            self.comando_sem_rotulo_if()
        elif(self.token_atual.tipo == 'while'):
            self.comando_sem_rotulo_while()
    
    def comando_sem_rotulo_id(self):
        possivel_variavel = self.token_atual.valor
        self.token_atual = self.proximo_token()
        if(self.token_atual.tipo != EPAREN): 
            self.token_atual = self.token_anterior
            self.char_atual = self.char_anterior
            self.posicao = self.posicao_anterior
            if(self.token_atual.valor in self.variaveis_declaradas):
                self.variaveis_em_analise = self.token_atual.valor
                self.consome(ID)
            elif(self.token_atual.valor in self.funcoes_declaradas):
                self.consome(ID)
            elif(self.token_atual.valor in self.procedimentos_declarados):
                self.mepa.insere_instrucao('chpr',self.mepa.estruturas_rotulos[self.token_atual.valor],self.n_procedure)
                self.consome(ID)
            elif(self.token_atual.valor == 'read'):
                self.consome('read')
                self.mepa.insere_instrucao('leit')
            elif(self.token_atual.valor == 'write'):
                self.consome('write')
            else:  
                self.error()
        else:
            self.token_atual = self.token_anterior
            self.char_atual = self.char_anterior
            self.posicao = self.posicao_anterior
            if(self.token_atual.valor == 'read'):
                self.consome('read')
                self.is_read = True
                self.mepa.insere_instrucao('leit')
            elif(self.token_atual.valor == 'write'):
                self.consome('write')
                self.is_write = True
            elif(self.token_atual.valor in self.procedimentos_declarados):
                self.consome(ID)
            else:  
                self.error()
        if(self.token_atual.tipo == DPIGUAL):
            #self.armz_auxiliar += 'ARMZ ' + str(self.n_procedure) +', '+ str(self.mepa.variaveis[str(self.n_procedure)][self.token_anterior.valor] + '\n')
            for key,value in self.mepa.variaveis.items():
                for x,y in value.items():
                    if(self.token_anterior.valor == x):
                        self.armz_auxiliar += 'ARMZ ' + key +', '+ y + '\n'    
            self.is_assign = True
            self.consome(DPIGUAL)
            self.expressao()
            self.mepa.instrucoes_mepa += self.op_termo_auxiliar
            self.mepa.instrucoes_mepa += self.op_simples_auxiliar
            self.mepa.instrucoes_mepa += self.armz_auxiliar
            #print(self.mepa.instrucoes_mepa)
            self.is_assign = False
            self.armz_auxiliar = ''
            self.op_termo_auxiliar = ''
            self.op_simples_auxiliar = ''
        elif(self.token_atual.tipo == EPAREN):
            self.consome(EPAREN)
            while(self.token_atual.tipo in (ID,INTEIRO)):
                self.expressao()
                if(self.token_atual.tipo == VIRGULA):
                    self.consome(VIRGULA)
            self.consome(DPAREN)
            self.is_read = False
            self.n_read = 0
            self.is_write = False
            self.n_write = 0

    def comando_sem_rotulo_begin(self):
        self.consome('begin')
        while(self.token_atual.tipo not in 'end'):
            self.comando()
            self.token_atual = self.proximo_token()
            if(self.token_anterior.valor != 'end'):
                self.token_atual = self.token_anterior
                self.char_atual = self.char_anterior
                self.posicao = self.posicao_anterior
                self.consome(PTVIRG)   
            else:
                self.token_atual = self.token_anterior
                self.char_atual = self.char_anterior
                self.posicao = self.posicao_anterior
        self.consome('end')
        if(self.is_while):
            self.mepa.instrucoes_mepa += 'DSVS ' + self.mepa.estruturas_rotulos['while'] 
            self.is_while = False
            self.mepa.instrucoes_mepa += 'R0' + str(self.mepa.numero_rotulo) + ': NADA\n'

    def comando_sem_rotulo_if(self):
        self.consome('if')
        self.expressao()
        self.mepa.instrucoes_mepa += self.cond_auxiliar
        self.cond_auxiliar = ''
        self.consome('then')
        self.mepa.instrucoes_mepa += 'DSVF R0' + str(self.mepa.numero_rotulo+1) + '\n'
        self.comando_sem_rotulo()
        if(self.token_atual.tipo == 'else'):
            self.mepa.instrucoes_mepa += 'DSVS R0' + str(self.mepa.numero_rotulo) + '\n'
            self.consome('else')
            self.mepa.instrucoes_mepa += 'R0' + str(self.mepa.numero_rotulo+1) + ': NADA' +  '\n'
            self.mepa.numero_rotulo +=1
            self.comando_sem_rotulo()
            self.mepa.instrucoes_mepa += 'R0' + str(self.mepa.numero_rotulo-1) + ': NADA' +  '\n'
            self.mepa.numero_rotulo +=1   
    
    def comando_sem_rotulo_while(self):
        self.mepa.estruturas_rotulos['while'] = 'R0' + str(self.mepa.numero_rotulo) + '\n'
        self.mepa.insere_instrucao('rotulo')
        self.consome('while')
        self.is_while = True
        self.expressao()
        self.mepa.instrucoes_mepa += self.cond_auxiliar
        self.cond_auxiliar = ''
        self.mepa.insere_instrucao('dsvf')
        self.consome('do')
        self.comando_sem_rotulo()


    def expressao(self):
        self.expressao_simples()
        if(self.token_atual.tipo == IGUAL):
            self.cond_auxiliar = 'CMIG\n'
            self.consome(IGUAL)
            self.expressao_simples()
        elif(self.token_atual.tipo == MAIOR):
            self.cond_auxiliar = 'CMMA\n'
            self.consome(MAIOR)
            self.expressao_simples()
        elif(self.token_atual.tipo == MENOR):
            self.cond_auxiliar = 'CMME\n'
            self.consome(MENOR)
            self.expressao_simples()
        elif(self.token_atual.tipo == MENORIGUAL):
            self.cond_auxiliar = 'CMEG\n'
            self.consome(MENORIGUAL)
            self.expressao_simples()
        elif(self.token_atual.tipo == MAIORIGUAL):
            self.cond_auxiliar = 'CMAG\n'
            self.consome(MAIORIGUAL)
            self.expressao_simples()
        elif(self.token_atual.tipo == NAOIGUAL):
            self.cond_auxiliar = 'CMDG\n'
            self.consome(NAOIGUAL)
            self.expressao_simples()
                
    def expressao_simples(self):
        if(self.token_atual.tipo == MAIS):
            self.consome(MAIS)
        elif(self.token_atual.tipo == MENOS):
            self.consome(MENOS)
        self.termo()
        variavel_antes_tipo = self.compara_valores(self.token_anterior.valor)
        if(self.token_atual.tipo == MAIS):
            while(self.token_atual.tipo == "MAIS"):
                self.op_simples_auxiliar = 'SOMA\n'
                #print(self.op_simples_auxiliar)
                self.consome(MAIS)
                self.termo()
                if(not self.is_assign):
                    self.mepa.instrucoes_mepa += self.op_simples_auxiliar
            variavel_depois_tipo = self.compara_valores(self.token_anterior.valor)
            if(variavel_antes_tipo != '' and variavel_depois_tipo != ''):
                self.checa_valores(variavel_antes_tipo,variavel_depois_tipo)
        elif(self.token_atual.tipo == MENOS):
            while(self.token_atual.tipo == "MENOS"):
                self.op_simples_auxiliar = 'SUBT\n'
                self.consome(MENOS)
                self.termo()
                if(not self.is_assign):
                    self.mepa.instrucoes_mepa += self.op_simples_auxiliar
                variavel_depois_tipo = self.compara_valores(self.token_anterior.valor)
                if(variavel_antes_tipo != '' and variavel_depois_tipo != ''):
                    self.checa_valores(variavel_antes_tipo,variavel_depois_tipo)
        elif(self.token_atual.tipo == 'or'):
            while(self.token_atual.tipo == "or"):
                self.op_simples_auxiliar = 'DISJ\n'
                self.consome('or')
                self.termo()
                if(not self.is_assign):
                    self.mepa.instrucoes_mepa += self.op_simples_auxiliar
                variavel_depois_tipo = self.compara_valores(self.token_anterior.valor)
                if(variavel_antes_tipo != '' and variavel_depois_tipo != ''):
                    self.checa_valores(variavel_antes_tipo,variavel_depois_tipo)

    def compara_valores(self,variavel_antes):
        variavel_antes_tipo = ''
        if(type(variavel_antes) == float or variavel_antes in self.variaveis_reais):
            variavel_antes_tipo = 'float'
        elif(type(variavel_antes) == int or variavel_antes in self.variaveis_inteiras):
            variavel_antes_tipo = 'int'
        elif(type(variavel_antes) == bool or variavel_antes in self.variaveis_booleanas):
            variavel_antes_tipo = 'bool'
        else:
            variavel_antes_tipo = ''
        return variavel_antes_tipo
    
    def checa_valores(self,antes,depois):
        if(antes != depois):
                if(self.variaveis_em_analise not in self.variaveis_reais):
                    self.error()
                elif(self.variaveis_em_analise in self.variaveis_reais and (antes == 'bool' or depois == 'bool')):
                        self.error()
        elif(self.variaveis_em_analise in self.variaveis_inteiras):
            if(antes == 'float' or antes == 'bool' or depois == 'float' or depois == 'bool'):
                self.error()
        
        
    
    def termo(self):
        self.fator()
        while(self.token_atual.tipo in (VEZES,'div','and')):
            variavel_antes_tipo = self.compara_valores(self.token_anterior.valor)
            if(self.token_atual.tipo == VEZES):
                self.op_termo_auxiliar = 'MULT\n'
                self.consome(VEZES)
                self.fator()
                if(not self.is_assign):
                    self.mepa.instrucoes_mepa += self.op_termo_auxiliar
                variavel_depois_tipo = self.compara_valores(self.token_anterior.valor)
                if(variavel_antes_tipo != '' and variavel_depois_tipo != ''):
                    self.checa_valores(variavel_antes_tipo,variavel_depois_tipo)
            elif(self.token_atual.tipo == 'div'):
                self.op_termo_auxiliar = 'DIVI\n'
                self.consome('div')
                self.fator()
                if(not self.is_assign):
                    self.mepa.instrucoes_mepa += self.op_termo_auxiliar
                variavel_depois_tipo = self.compara_valores(self.token_anterior.valor)
                if(variavel_antes_tipo != '' and variavel_depois_tipo != ''):
                    self.checa_valores(variavel_antes_tipo,variavel_depois_tipo)    
            elif(self.token_atual.tipo == 'and'):
                self.op_termo_auxiliar = 'CONJ\n'
                self.consome('and')
                self.fator()
                if(not self.is_assign):
                    self.mepa.instrucoes_mepa += self.op_termo_auxiliar
                variavel_depois_tipo = self.compara_valores(self.token_anterior.valor)
                if(variavel_antes_tipo != '' and variavel_depois_tipo != ''):
                    self.checa_valores(variavel_antes_tipo,variavel_depois_tipo)

    def fator(self):
        if(self.token_atual.tipo == ID):
            self.token_atual = self.proximo_token()
            if(self.token_atual.tipo != EPAREN):    
                self.token_atual = self.token_anterior
                self.char_atual = self.char_anterior
                self.posicao = self.posicao_anterior
                if(self.token_atual.valor in self.variaveis_declaradas):
                    if(self.is_read):
                        if(self.n_read >= 1):
                            self.mepa.insere_instrucao('leit')
                        for key,value in self.mepa.variaveis.items():
                                for x,y in value.items():
                                    if(self.token_atual.valor == x):
                                        self.mepa.insere_instrucao('armz',key,y)
                        self.n_read += 1
                    elif(self.is_write):
                        for key,value in self.mepa.variaveis.items():
                                for x,y in value.items():
                                    if(self.token_atual.valor == x):
                                        self.mepa.insere_instrucao('crvl',key,y)
                        self.mepa.insere_instrucao('impr')
                        self.n_write += 1
                    elif(self.is_while or self.is_assign):
                        for key,value in self.mepa.variaveis.items():
                                for x,y in value.items():
                                    if(self.token_atual.valor == x):
                                        self.mepa.insere_instrucao('crvl',key,y)
                    else:
                        for key,value in self.mepa.variaveis.items():
                                for x,y in value.items():
                                    if(self.token_atual.valor == x):
                                        self.mepa.insere_instrucao('crvl',key,y)
                    self.consome(ID)
                elif(self.token_atual.valor in self.funcoes_declaradas):
                    self.consome(ID)
                elif(self.token_atual.valor in self.procedimentos_declarados):
                    self.consome(ID)
                else:  
                    self.error()
            else:
                self.token_atual = self.token_anterior
                self.char_atual = self.char_anterior
                self.posicao = self.posicao_anterior
                if(self.token_atual.valor in self.funcoes_declaradas):
                    self.consome(ID)
                elif(self.token_atual.valor in self.procedimentos_declarados):
                    self.error()
                else:  
                    self.error()
            if(self.token_atual.tipo == EPAREN):
                self.consome(EPAREN)
                while(self.token_atual.tipo not in DPAREN):
                    self.expressao()
                    if(self.token_atual.tipo == VIRGULA):
                        self.consome(VIRGULA)
                self.consome(DPAREN)
        elif(self.token_atual.tipo == INTEIRO):
            if(self.is_assign):
                self.mepa.insere_instrucao('crct',self.token_atual.valor)
            elif(self.is_write):
                self.mepa.insere_instrucao('crct',self.token_atual.valor)
                self.mepa.insere_instrucao('impr')
                self.n_write += 1
            else:
                self.mepa.insere_instrucao('crct',self.token_atual.valor)
            self.consome(INTEIRO)
        elif(self.token_atual.tipo == EPAREN):
            self.consome(EPAREN)
            self.expressao()
            self.consome(DPAREN)          
        elif(self.token_atual.tipo == 'not'):
            self.consome('not')
            self.fator()
        else:
            self.error()

            

    def consome(self,token_tipo):
        mepa = GeradorMepa()
        #print('TOKEN ESPERADO = ', token_tipo, '|| TOKEN DA ENTRADA = ',self.token_atual.tipo, '(',self.token_atual.valor,') ')
        if(token_tipo == self.token_atual.tipo):   
            self.token_atual = self.proximo_token()
        else:
            self.error() 
       
def main():
    file_name = sys.argv[1]
    fp = open(file_name)
    contents = fp.read()
    #contents = "program exemplo73 (input, output); var n, s, i : integer; procedure soma; var q : integer; begin q:=i*i; if (i div 2) * 2 = i then s:=s+q else s:=s-q end; begin read (n); s:=0; i:=0; while i<=n do begin soma; write(s); i:=i+1 end end. "

    interpretador = Interpretador(contents)
    interpretador.programa()
    print("Aceito")

main()
