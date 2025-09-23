import json

class Busca:
    def __init__(self, objetivo: tuple):
        # Usado para comparar e reconstruir caminho
        self.objetivo = objetivo

    # Gera todos os estados vizinhos válidos a partir do estado atual
    def definir_vizinhos(self, estado):
        estado = tuple(estado)  
        vizinhos = []           

        index_zero = estado.index(0)  # encontra a posição do espaço vazio (0)
        linha, col = divmod(index_zero, 3)  # converte índice linear em linha e coluna
        movimentos = []  

        if linha > 0:
            movimentos.append(index_zero - 3)  
        if linha < 2:
            movimentos.append(index_zero + 3)  
        if col > 0:
            movimentos.append(index_zero - 1)  
        if col < 2:
            movimentos.append(index_zero + 1)  
            
        # Cria novos estados trocando o espaço vazio com as posições válidas
        for index_mov in movimentos:
            novo_estado = list(estado)  # cria uma cópia do estado
            novo_estado[index_zero], novo_estado[index_mov] = (
                novo_estado[index_mov],
                novo_estado[index_zero],
            )  # troca a posição do zero com o movimento permitido
            vizinhos.append(tuple(novo_estado))  

        return vizinhos

    # Reconstrói o caminho da solução usando o dicionário de pais
    def reconstruir_caminho(self, pais):
        caminho = []
        estado_atual = self.objetivo  # começa do estado objetivo
        while estado_atual is not None:
            caminho.append(estado_atual)           # adiciona o estado atual ao caminho
            estado_atual = pais[estado_atual]      # segue para o estado pai
        caminho.reverse()  # inverte para que o caminho vá do inicial até o objetivo
        return caminho

    # Salva a fronteira e os estados visitados em um arquivo JSON
    def salvar_fronteira_visitados(self, fronteira, visitados, arquivo="fronteira_visitados.json"):
        lista_fronteira = []

        for s in fronteira:
            # Para A*: o estado está na posição 2 da tupla (f, g, estado)
            if isinstance(s, tuple) and len(s) == 3:
                lista_fronteira.append(list(s[2]))  # converte o estado para lista para JSON
            # Para Custo Uniforme: o estado está na posição 1 da tupla (dist, estado)
            elif isinstance(s, tuple) and len(s) == 2:
                lista_fronteira.append(list(s[1]))
            # Caso seja só o estado
            else:
                lista_fronteira.append(list(s))

        # Converte os estados visitados para listas também
        dados = {
            "Fronteira": lista_fronteira,
            "Visitados": [list(v) for v in visitados]
        }

        # Salva os dados em um arquivo JSON legível
        with open(arquivo, "w") as f:
            json.dump(dados, f, indent=4)
