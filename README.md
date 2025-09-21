# Trabalho 1 de Sistemas Inteligentes

## 1. Custo Uniforme (sem heurística)

Algoritmo que implementa custo uniforme, com base no algoritmo Dijkstra (disponível em dijkstra.txt). A implementação utiliza a biblioteca heapq do python para a definição da lista de prioridade.

Instruções de compilação (requisitos contem uma biblioteca para impressões coloridas):

`pip install -r requirements.txt`

`python3 custo_uniforme.py`

Para exemplos diferentes, **modificar as tuplas na função main** e/ou a quantidade máxima de iterações ao chamar a função custo_uniforme.

## 2. A\* com uma heurística não admissível

## 3. A\* com uma heurística admissível simples

O algoritmo A* combina a busca em custo uniforme com uma heurística que estima o custo restante até o objetivo. Neste trabalho, utilizamos uma heurística simples admissível para o problema do 8-puzzle, baseada em peças fora do lugar.

#### 3.1 Definição da heurística

Nome: Peças fora do lugar (misplaced tiles)

Descrição: Conta o número de peças que não estão na posição correta, ignorando o espaço vazio (0). Cada peça fora do lugar contribui com um custo mínimo de 1 movimento.

## 4. A\* com a heurística admissível mais precisa que conseguirem
