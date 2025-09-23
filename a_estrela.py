import heapq
import time
from busca import Busca  # Classe base que contém métodos comuns, como definir_vizinhos e reconstruir_caminho

class AEstrela(Busca):

    # Heurística: conta o número de peças fora do lugar em relação ao objetivo
    def heuristica_pecas_fora_do_lugar(self, estado):
        return sum(1 for i in range(9) if estado[i] != 0 and estado[i] != self.objetivo[i])

    # Heurística: soma das distâncias de Manhattan de cada peça até sua posição final
    def heuristica_distancia_manhatthan(self, estado):
        resultado = 0
        for i, num in enumerate(estado):
            if num == 0:  # Ignora o espaço vazio
                continue
            linha_atual, col_atual = divmod(i, 3)  # posição atual da peça
            index_obj = self.objetivo.index(num)   # índice da posição correta da peça
            linha_obj, col_obj = divmod(index_obj, 3)  # posição correta da peça
            resultado += abs(linha_atual - linha_obj) + abs(col_atual - col_obj)  
        return resultado
    
    def heuristica_nao_admissivel(self, estado):
        return self.heuristica_distancia_manhatthan(estado) * 4

    # Algoritmo A* propriamente dito
    def a_estrela(self, inicio, heuristica, max_iteracoes: int):
        tempo_inicio = time.time()  # tempo total do método, incluindo reconstrução e gravação
        estados_abertos = []        # heap de prioridade com os estados a serem explorados
        estados_fechados = set()    # conjunto de estados já visitados
        pais = {inicio: None}       
        distancias = {inicio: 0}    
        heapq.heappush(estados_abertos, (heuristica(inicio), 0, inicio))  # insere o estado inicial no heap
        cont_iteracoes = 0
        nodos_visitados = 0
        max_fronteira = 0  # maior tamanho que a fronteira (heap) atingiu

        tempo_busca_inicio = time.time()  # tempo de execução apenas da busca

        # Loop principal do A*
        while estados_abertos and cont_iteracoes < max_iteracoes:
            max_fronteira = max(max_fronteira, len(estados_abertos))  # atualiza o maior tamanho da fronteira
            f, g, estado_atual = heapq.heappop(estados_abertos)  # retira o estado com menor f = g + h
            nodos_visitados += 1

            # Verifica se alcançou o objetivo
            if estado_atual == self.objetivo:
                tempo_busca_fim = time.time()  
                caminho = self.reconstruir_caminho(pais)  # reconstrói o caminho da solução
                # salva fronteira e visitados no arquivo .json
                self.salvar_fronteira_visitados(estados_abertos, estados_fechados)  
                tempo_fim_total = time.time()  
                return {
                    "Custo": g,  # custo do caminho até o objetivo
                    "NodosVisitados": nodos_visitados,  
                    "TempoBusca": tempo_busca_fim - tempo_busca_inicio, 
                    "TempoTotal": tempo_fim_total - tempo_inicio, 
                    "MaiorFronteira": max_fronteira,
                    "Caminho": caminho
                }

            if estado_atual in estados_fechados:  # ignora estados já visitados
                continue

            # Expande os vizinhos do estado atual
            for vizinho in self.definir_vizinhos(estado_atual):
                if vizinho in estados_fechados:
                    continue
                g_novo = g + 1  # custo do caminho até o vizinho
                # Se o novo custo é menor que o registrado, atualiza informações
                if g_novo < distancias.get(vizinho, float("inf")):
                    distancias[vizinho] = g_novo
                    pais[vizinho] = estado_atual
                    f_novo = g_novo + heuristica(vizinho)  # f = g + h
                    heapq.heappush(estados_abertos, (f_novo, g_novo, vizinho))  # insere vizinho no heap

            estados_fechados.add(estado_atual)  # marca estado atual como visitado
            cont_iteracoes += 1

        # Caso não encontre solução dentro do limite de iterações imprime mensagem de erro
        print("[ERRO] Sem solução no limite de iterações")
        return None
