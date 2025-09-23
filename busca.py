import json

class Busca:
    def __init__(self, objetivo: tuple):
        self.objetivo = objetivo

    def definir_vizinhos(self, estado):
        estado = tuple(estado)
        vizinhos = []
        index_zero = estado.index(0)
        linha, col = divmod(index_zero, 3)
        movimentos = []
        if linha > 0: movimentos.append(index_zero - 3)
        if linha < 2: movimentos.append(index_zero + 3)
        if col > 0: movimentos.append(index_zero - 1)
        if col < 2: movimentos.append(index_zero + 1)
        for index_mov in movimentos:
            novo_estado = list(estado)
            novo_estado[index_zero], novo_estado[index_mov] = (
                novo_estado[index_mov],
                novo_estado[index_zero],
            )
            vizinhos.append(tuple(novo_estado))
        return vizinhos

    def reconstruir_caminho(self, pais):
        caminho = []
        estado_atual = self.objetivo
        while estado_atual is not None:
            caminho.append(estado_atual)
            estado_atual = pais[estado_atual]
        caminho.reverse()
        return caminho

    def salvar_fronteira_visitados(self, fronteira, visitados, arquivo="fronteira_visitados.json"):
        lista_fronteira = []

        for s in fronteira:
            # Se é A*, o estado está na posição 2 da tupla (f, g, estado)
            if isinstance(s, tuple) and len(s) == 3:
                lista_fronteira.append(list(s[2]))
            # Se é Custo Uniforme, o estado está na posição 1 da tupla (dist, estado)
            elif isinstance(s, tuple) and len(s) == 2:
                lista_fronteira.append(list(s[1]))
            # Caso seja só o estado
            else:
                lista_fronteira.append(list(s))

        dados = {
            "Fronteira": lista_fronteira,
            "Visitados": [list(v) for v in visitados]
        }

        with open(arquivo, "w") as f:
            json.dump(dados, f, indent=4)
