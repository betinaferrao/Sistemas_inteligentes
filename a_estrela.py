import heapq
import time
from busca import Busca

class AEstrela(Busca):

    def heuristica_pecas_fora_do_lugar(self, estado):
        return sum(1 for i in range(9) if estado[i] != 0 and estado[i] != self.objetivo[i])

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

    def a_estrela(self, inicio, heuristica, max_iteracoes: int):
        tempo_inicio = time.time()
        estados_abertos = []
        estados_fechados = set()
        pais = {inicio: None}
        distancias = {inicio: 0}
        heapq.heappush(estados_abertos, (heuristica(inicio), 0, inicio))
        cont_iteracoes = 0
        nodos_visitados = 0
        max_fronteira = 0

        tempo_busca_inicio = time.time()
        while estados_abertos and cont_iteracoes < max_iteracoes:
            max_fronteira = max(max_fronteira, len(estados_abertos))
            f, g, estado_atual = heapq.heappop(estados_abertos)
            nodos_visitados += 1

            if estado_atual == self.objetivo:
                tempo_busca_fim = time.time()
                caminho = self.reconstruir_caminho(pais)
                self.salvar_fronteira_visitados(estados_abertos, estados_fechados)
                tempo_fim_total = time.time()
                return {
                    "Custo": g,
                    "NodosVisitados": nodos_visitados,
                    "TempoBusca": tempo_busca_fim - tempo_busca_inicio,
                    "TempoTotal": tempo_fim_total - tempo_inicio,
                    "MaiorFronteira": max_fronteira,
                    "Caminho": caminho
                }

            if estado_atual in estados_fechados:
                continue

            for vizinho in self.definir_vizinhos(estado_atual):
                if vizinho in estados_fechados:
                    continue
                g_novo = g + 1
                if g_novo < distancias.get(vizinho, float("inf")):
                    distancias[vizinho] = g_novo
                    pais[vizinho] = estado_atual
                    f_novo = g_novo + heuristica(vizinho)
                    heapq.heappush(estados_abertos, (f_novo, g_novo, vizinho))

            estados_fechados.add(estado_atual)
            cont_iteracoes += 1

        print("[ERRO] Sem solução no limite de iterações")
        return None
