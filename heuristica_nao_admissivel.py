import heapq
import time


class AEstrela:
    def __init__(self, objetivo: tuple):
        self.objetivo = objetivo

    # Impressões
    def imprimir_estado(self, estado):
        rows = [estado[i : i + 3] for i in range(0, 9, 3)]
        for row in rows:
            print(" ".join(str(x) if x != 0 else "_" for x in row))
        print()

    def imprimir_resultados(self, stats):
        print(f"\nCusto (g): {stats['Custo']}, f=g+h: {stats['f']}")
        print("Caminho:")
        for estado in stats["Caminho"]:
            self.imprimir_estado(estado)
        print(f"Iterações: {stats['Iterações']}")
        print(f"Tempo: {stats['Tempo']}")

    def heuristica_superestimada(self, estado):
        resultado = 0
        for num in estado:
            # Calcula a distância Manhathan de cada numero pra sua posição no estado objetivo e soma em resultado
            index_atual = estado.index(num)
            linha_atual, col_atual = divmod(index_atual, 3)
            index_obj = self.objetivo.index(num)
            linha_obj, col_obj = divmod(index_obj, 3)
            resultado += (abs(linha_atual - linha_obj) + abs(col_atual - col_obj))*2 # Penaliza as distâncias maiores
        return resultado

    # Vizinhos
    def definir_vizinhos(self, estado):
        estado = tuple(estado)
        vizinhos = []
        index_zero = estado.index(0)
        linha, col = divmod(index_zero, 3)

        movimentos = []
        if linha > 0:
            movimentos.append(index_zero - 3)
        if linha < 2:
            movimentos.append(index_zero + 3)
        if col > 0:
            movimentos.append(index_zero - 1)
        if col < 2:
            movimentos.append(index_zero + 1)

        for index_mov in movimentos:
            novo_estado = list(estado)
            novo_estado[index_zero], novo_estado[index_mov] = (
                novo_estado[index_mov],
                novo_estado[index_zero],
            )
            vizinhos.append(tuple(novo_estado))

        return vizinhos

    # Reconstrução do caminho
    def reconstruir_caminho(self, pais):
        caminho = []
        estado_atual = self.objetivo
        while estado_atual is not None:
            caminho.append(estado_atual)
            estado_atual = pais[estado_atual]
        caminho.reverse()
        return caminho

    # Algoritmo A*
    def a_estrela(self, inicio, max_iteracoes: int):
        tempo_inicio = time.time()  # Contagem de segundos
        estados_abertos = []
        estados_fechados = set()
        pais = {inicio: None}
        distancias = {inicio: 0}

        # Calcula a heurística do estado inicial
        h0 = self.heuristica_superestimada(inicio)
        f0 = 0 + h0  # g (num movimentos) + heuristica
        heapq.heappush(estados_abertos, (f0, 0, h0, inicio))
        cont_iteracoes = 0

        while estados_abertos and cont_iteracoes < max_iteracoes:
            # Retira o estado com menor f do heap (prioridade)
            f, g, h, estado_atual = heapq.heappop(estados_abertos)
            print(f"\n[POP] Estado atual; f: {f}, g: {g}, h: {h}")
            self.imprimir_estado(estado_atual)

            # Se o estado atual for o objetivo, finaliza
            if estado_atual == self.objetivo:
                tempo_fim = time.time()
                print("[FIM] Objetivo alcançado")
                caminho = self.reconstruir_caminho(pais)
                stats = {
                    "Custo": g,
                    "Heuristica": h,
                    "f": f,
                    "Caminho": caminho,
                    "Iterações": cont_iteracoes,
                    "Tempo": tempo_fim - tempo_inicio,
                }
                return stats

            # Se o estado já foi explorado, ignora
            if estado_atual in estados_fechados:
                continue

            # Gera todos os vizinhos possíveis do estado atual
            vizinhos = self.definir_vizinhos(estado_atual)

            # Ignora vizinhos já explorados
            for vizinho in vizinhos:
                if vizinho in estados_fechados:
                    continue

                # g_novo = custo real do estado inicial até o vizinho
                g_novo = g + 1

                # Pega o custo conhecido do vizinho (se houver). Se não, assume infinito
                dist_vizinho = distancias.get(vizinho, float("inf"))

                # Só atualiza se encontramos um caminho melhor (menor g)
                if g_novo < dist_vizinho:
                    distancias[vizinho] = g_novo
                    pais[vizinho] = estado_atual
                    # Calcula heurística do vizinho
                    h_novo = self.heuristica_superestimada(vizinho)
                    # Calcula f = g + h
                    f_novo = g_novo + h_novo
                    # Adiciona o vizinho ao heap de abertos
                    heapq.heappush(estados_abertos, (f_novo, g_novo, h_novo, vizinho))
                    print(
                                                f"[PUSH] Vizinho {vizinho} com f={f_novo}, g={g_novo}, h={h_novo} adicionado"
                    )

            # Mostrar abertos e fechados
            # print(
            #     TA
            #     + f"[ABERTOS] {[(f, g, h, s) for f, g, h, s in estados_abertos]}"
            # )
            # print(+ f"[FECHADOS] {list(estados_fechados)}")

            estados_fechados.add(estado_atual)
            cont_iteracoes += 1

        print(f"[ERRO] Sem solução no limite de {max_iteracoes} iterações")
        return 0


def main():
    inicios = [
        (1, 2, 3, 4, 0, 6, 7, 5, 8),  # fácil
        (1, 2, 3, 5, 0, 6, 4, 7, 8),  # médio 1
        (3, 0, 6, 4, 2, 1, 7, 5, 8),  # médio 2
        (0, 4, 7, 2, 3, 1, 6, 8, 5),  # difícil 1
        (7, 2, 4, 5, 0, 6, 8, 3, 1),  # difícil 2
    ]
    objetivo = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    aestrela = AEstrela(objetivo)
    stats = []

    for i, inicio in enumerate(inicios):
        print("\n" + "=" * 40)
        print(f"=========== TESTE {i} ===========")
        print("=" * 40 + "\n")
        print("Estado inicial:")
        aestrela.imprimir_estado(inicio)

        resultado = aestrela.a_estrela(inicio, 1000000)
        stats.append(resultado)

        print("=" * 40)
        print(f"========= FIM TESTE {i} =========")
        print("=" * 40 + "\n")

    print("\n" + "=" * 40)
    print("=========== RESUMO FINAL ===========")
    print("=" * 40 + "\n")

    for i, stat in enumerate(stats):
        print("Resumo de desempenho -----------\n")
        if stat:
            print(
                f"Tempo teste {i}: ",
                stat["Tempo"],
                f"\nIterações {i}: ",
                stat["Iterações"],
                "\n",
            )
        else:
            print(f"Início {i} não resolvido dentro do limite\n")

if __name__ == "__main__":
    main()
