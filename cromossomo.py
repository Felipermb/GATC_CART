# Criado por Felipe Reis

# Exemplo de Cromossomo
# 0 0 000000 00000000 00000000 101 0

# criterion                 :  0 = 'gini' ||  1 = 'entropy'
# splitter                  :  0 = 'best' ||  1 = 'random'
# max_depth                 :  0 =  None  || [1 -> 50] (int)
# min_samples_split         : [2 -> 255] (int)
# min_samples_leaf          : [1 -> 255] (int)
# min_weight_fraction_leaf  : [0 -> 0.5] = (0 -> 5) * 0.1
# presort                   :  0 = True || 1 = False

# Imports necessários
from GATC_CART.StellPlatesDataset import StellPlatesDataset
from sklearn import tree, cross_validation, datasets
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, cross_val_predict

import pandas as pd

class Cromossomo():

    individuo = ''
    lambyda = ''
    mascara = ''

    fitness = 0
    acuracia = 0
    size = 0

    algoritmoEscolhido = 0

    #######################################
    # CONSTRUTORES

    def __init__(self, ind, lambyda, mascara, algoritmo):
        self.inicializarVariaveis(ind, lambyda, mascara, algoritmo)

    #######################################
    # INICIALIZADORES

    def inicializarVariaveis(self, ind, lamb, masc,algoritmo):
        self.individuo = ind
        self.lambyda = lamb
        self.mascara = masc
        self.algoritmoEscolhido = algoritmo
        self.calcularFitness()

    #######################################
    # Váriaveis do cromossomo

    def getCriterion(self):
        if(self.individuo[0] == '0'):
            return 'gini'
        else:
            return 'entropy'

    def getSplitter(self):
        if(self.individuo[1] == '0'):
            return 'best'
        else:
            return 'random'

    def getMaxDepth(self):
        aux = 0
        soma = 0
        for i in range(7, 1, -1):
            bit = int(self.individuo[i])
            if(bit == 1):
                soma = soma + (2 ** aux)
            aux += 1

        if(soma == 0):
            return None
        elif(soma > 50):
            return 50
        else:
            return soma

    def getMinSamplesSplit(self):
        aux = 0
        soma = 0
        for i in range(15, 7, -1):
            bit = int(self.individuo[i])
            if(bit == 1):
                soma = soma + (2 ** aux)
            aux += 1

        if (soma < 2):
            return 2
        else:
            return soma

    def getMinSamplesLeaf(self):
        aux = 0
        soma = 0
        for i in range(23, 15, -1):
            bit = int(self.individuo[i])
            if(bit == 1):
                soma = soma + (2 ** aux)
            aux += 1

        if (soma < 1):
            return 1
        else:
            return soma

    def getMinWeigthFractionLeaf(self):
        soma = 0
        aux = 0
        for i in range(26, 23, -1):
            bit = int(self.individuo[i])
            if(bit == 1):
                soma = soma + (2 ** aux)

            if(soma > 5):
                return 5 * 0.1
            else:
                return soma * 0.1

    def getPresort(self):
        if(self.individuo[26] == '1'):
            return False
        else:
            return True

    #######################################
    # OPERADORES

    # Função para calcular o fitness do cromossomo
    #
    # A proposta de otimização é:
    # Obter maior valor de Acurácia e/ou Diminuir o tamanho da árvore final gerada
    def calcularFitness(self):
        if(self.algoritmoEscolhido == 0):
            dataset = StellPlatesDataset()
            target = dataset.target
            data = dataset.data   
        elif (self.algoritmoEscolhido  == 1):
            dataset = datasets.load_iris()
            target = dataset.target
            data = dataset.data  
        elif (self.algoritmoEscolhido  == 2):
            dataset = datasets.load_wine()
            target = dataset.target
            data = dataset.data  
        elif (self.algoritmoEscolhido  == 3):
            dataset = datasets.load_digits()
            target = dataset.target
            data = dataset.data  
        elif (self.algoritmoEscolhido  == 4):
            dataset = datasets.load_breast_cancer()
            target = dataset.target
            data = dataset.data
        elif (self.algoritmoEscolhido  == 5):
            data = pd.read_csv('BaseDeDados/isolet.csv', sep=',')
            list = ['classe']
            target = data.classe
            data = data.drop(list,axis = 1)
        else :
            data = pd.read_csv('BaseDeDados/madelon.csv', sep=',')
            list = ['classe']
            target = data.classe
            data = data.drop(list,axis = 1)

        # Carrega o algoritmo de ML que será utilizado (No caso, árvore de decisão = DecisionTreeClassifier() )
        # AQUI, nós passaremos os parâmetros, pois é aqui que usamos o Cromossomo, para poder testa-lo e obter calcular seu fitnes
        cri = self.getCriterion()
        spl = self.getSplitter()
        max_d = self.getMaxDepth()
        min_ss = self.getMinSamplesSplit()
        min_sl = self.getMinSamplesLeaf()
        min_wfleaf = self.getMinWeigthFractionLeaf()
        pre = self.getPresort()

        # Acrescenta o parâmetro random_state = 0, para que o algoritmo continue deterministico
        clf = DecisionTreeClassifier(criterion=cri, splitter=spl, max_depth=max_d, min_samples_split=min_ss,
                                     min_samples_leaf=min_sl, min_weight_fraction_leaf=min_wfleaf, presort=pre, random_state=0)

        # Chama a função fit e realiza a montagem da árvore
        scores = cross_validation.cross_val_score(clf, data, target, cv=10, scoring='accuracy')
        self.acuracia = round(100*scores.mean(), 2)
        clf = clf.fit(data, target)

        # scores = cross_validation.cross_val_score(clf, iris.data, iris.target, cv=5, scoring='f1')
        # self.acuracia = accuracy_score(Y_test, clf.predict(X_test)) * 100

        # Retorna o tamanho da árvore
        treeObj = clf.tree_
        self.size = treeObj.node_count

        # como queremos diminuir a profundidade da árvore e aumentar a acuracia
        # usaremos 1/size para podermos com valor de aumento nos dois parâmetros dsa nossa função de calculo de fitness
        self.fitness = (1/self.size) + self.acuracia
