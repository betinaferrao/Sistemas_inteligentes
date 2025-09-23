import heapq
import time

# ---------------- CLASSE A* ----------------
class AEstrela:
    def __init__(self, objetivo: tuple):
        self.objetivo = objetivo

    def imprimir_estado(self, estado):
        rows = [estado[i: i + 3] for i in range(0, 9, 3)]
        for row in rows:
            print(" ".join(str(x) if x != 0 else "_" for x in row))
        print()

    def heuristica_pecas_fora_do_lugar(self, estado):
        return sum(
            1 for i in range(9) if estado[i] != 0 and estado[i] != self.objetivo[i]
        )

    def heuristica_distancia_manhathan(self, estado):
        resultado = 0
        for i, num in enumerate(estado):
            if num == 0:
                continue
            linha_atual, col_atual = divmod(i, 3)
            index_obj = self.objetivo.index(num)
            linha_obj, col_obj = divmod(index_obj, 3)
            resultado += abs(linha_atual - linha_obj) + abs(col_atual - col_obj)
        return resultado

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

    # Algoritmo A*
    def a_estrela(self, inicio, heuristica, max_iteracoes: int):
        tempo_inicio = time.time()
        estados_abertos = []
        estados_fechados = set()
        pais = {inicio: None}
        distancias = {inicio: 0}

        h0 = heuristica(inicio)  # <<< usa a função passada
        f0 = 0 + h0
        heapq.heappush(estados_abertos, (f0, 0, h0, inicio))
        cont_iteracoes = 0
        nodos_visitados = 0  

        while estados_abertos and cont_iteracoes < max_iteracoes:
            f, g, h, estado_atual = heapq.heappop(estados_abertos)
            nodos_visitados += 1 
            print(f"\n[POP] Estado atual; f: {f}, g: {g}, h: {h}")
            self.imprimir_estado(estado_atual)

            if estado_atual == self.objetivo:
                tempo_fim = time.time()
                print("[FIM] Objetivo alcançado")
                caminho = self.reconstruir_caminho(pais)  # gera lista de estados do caminho
                stats = {
                    "Custo": g,
                    "Iterações": cont_iteracoes,
                    "Tempo": tempo_fim - tempo_inicio,
                    "NodosVisitados": nodos_visitados,
                    "Caminho": caminho,  # <<< adiciona aqui
                }
                return stats

            if estado_atual in estados_fechados:
                continue

            vizinhos = self.definir_vizinhos(estado_atual)
            for vizinho in vizinhos:
                if vizinho in estados_fechados:
                    continue

                g_novo = g + 1
                dist_vizinho = distancias.get(vizinho, float("inf"))

                if g_novo < dist_vizinho:
                    distancias[vizinho] = g_novo
                    pais[vizinho] = estado_atual
                    h_novo = heuristica(vizinho)  # <<< usa a função passada
                    f_novo = g_novo + h_novo
                    heapq.heappush(estados_abertos, (f_novo, g_novo, h_novo, vizinho))
                    print(f"[PUSH] Vizinho {vizinho} com f={f_novo}, g={g_novo}, h={h_novo} adicionado")

            estados_fechados.add(estado_atual)
            cont_iteracoes += 1

        print(f"[ERRO] Sem solução no limite de {max_iteracoes} iterações")
        return 0



# ---------------- CLASSE CUSTO UNIFORME ----------------
class CustoUniforme:
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

    def custo_uniforme(self, inicio, max_iteracoes: int):
        tempo_inicio = time.time()
        estados_abertos = []
        estados_fechados = []
        pais = {inicio: None}
        distancias = {inicio: 0}

        heapq.heappush(estados_abertos, (0, inicio))
        cont_iteracoes = 0

        while estados_abertos and cont_iteracoes < max_iteracoes:
            dist, estado_atual = heapq.heappop(estados_abertos)

            if estado_atual == self.objetivo:
                tempo_fim = time.time()
                caminho = self.reconstruir_caminho(pais)
                return {
                    "Custo": dist,
                    "Iterações": cont_iteracoes,
                    "Tempo": tempo_fim - tempo_inicio,
                    "Caminho": caminho,
                }

            if estado_atual in estados_fechados:
                continue

            for vizinho in self.definir_vizinhos(estado_atual):
                if vizinho in estados_fechados:
                    continue
                dist_nova = dist + 1
                dist_vizinho = distancias.get(vizinho, float("inf"))

                if dist_nova < dist_vizinho:
                    distancias[vizinho] = dist_nova
                    pais[vizinho] = estado_atual
                    heapq.heappush(estados_abertos, (dist_nova, vizinho))

            estados_fechados.append(estado_atual)
            cont_iteracoes += 1

        print("[ERRO] Sem solução no limite de iterações")
        return None


# ---------------- FUNÇÃO PRINCIPAL ----------------
def main():
    objetivo = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    tabuleiro_recebido = input("Digite o tabuleiro inicial (ex: 1,2,3,4,5,6,7,0,8): ")
    inicio = tuple(map(int, tabuleiro_recebido.split(",")))

    print("\nEscolha o algoritmo de busca:")
    print("1. Custo Uniforme")
    print("2. A* com heurística admissível simples")
    print("3. A* com heurística admissível precisa")
    print("4. A* com heurística não admissível")
    escolha = input("Opção: ")

    if escolha == "1":
        cu = CustoUniforme(objetivo)
        resultado = cu.custo_uniforme(inicio, 100000)
    elif escolha in ["2", "3", "4"]:
        ae = AEstrela(objetivo)
        if escolha == "2":
            heuristica = ae.heuristica_pecas_fora_do_lugar
        elif escolha == "3":
            heuristica = ae.heuristica_distancia_manhathan
        else:
            heuristica = lambda estado: ae.heuristica_distancia_manhathan(estado) * 4

        resultado = ae.a_estrela(inicio, heuristica, 100000)
    else:
        print("Opção inválida!")
        return

    if resultado:
        print(f"\nCusto: {resultado['Custo']}")
        print(f"Iterações: {resultado['Iterações']}")
        print(f"Tempo: {resultado['Tempo']:.4f} segundos")
        print("Caminho solução:")
        for estado in resultado["Caminho"]:
            print(estado)



if __name__ == "__main__":
    main()
