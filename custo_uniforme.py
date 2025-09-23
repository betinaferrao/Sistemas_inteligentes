import heapq
import time
from busca import Busca

class CustoUniforme(Busca):

    def custo_uniforme(self, inicio, max_iteracoes: int):
        tempo_inicio = time.time()
        estados_abertos = []
        estados_fechados = []
        pais = {inicio: None}
        distancias = {inicio: 0}
        heapq.heappush(estados_abertos, (0, inicio))
        cont_iteracoes = 0
        nodos_visitados = 0
        max_fronteira = 0

        tempo_busca_inicio = time.time()
        while estados_abertos and cont_iteracoes < max_iteracoes:
            max_fronteira = max(max_fronteira, len(estados_abertos))
            dist, estado_atual = heapq.heappop(estados_abertos)
            nodos_visitados += 1

            if estado_atual == self.objetivo:
                tempo_busca_fim = time.time()
                caminho = self.reconstruir_caminho(pais)
                self.salvar_fronteira_visitados(estados_abertos, estados_fechados)
                tempo_fim_total = time.time()
                return {
                    "Custo": dist,
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
                dist_nova = dist + 1
                if dist_nova < distancias.get(vizinho, float("inf")):
                    distancias[vizinho] = dist_nova
                    pais[vizinho] = estado_atual
                    heapq.heappush(estados_abertos, (dist_nova, vizinho))

            estados_fechados.append(estado_atual)
            cont_iteracoes += 1

        print("[ERRO] Sem solução no limite de iterações")
        return None
