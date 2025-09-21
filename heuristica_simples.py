import heapq
from colorama import init, Fore


class AEstrela:
    def __init__(self, inicial: tuple, objetivo: tuple):
        self.inicial = inicial
        self.objetivo = objetivo

    # Impressões
    def imprimir_estado(self, estado):
        rows = [estado[i : i + 3] for i in range(0, 9, 3)]
        for row in rows:
            print(" ".join(str(x) if x != 0 else "_" for x in row))
        print()

    def imprimir_resultados(self, stats):
        print(Fore.BLUE + f"Custo (g): {stats['Custo']}, Heurística (h): {stats['Heuristica']}, f=g+h: {stats['f']}")
        print("Caminho:")
        for estado in stats["Caminho"]:
            self.imprimir_estado(estado)
        print(f"Iterações: {stats['Iterações']}")

    # Heurística
    def heuristica_pecas_fora_do_lugar(self, estado):
        # Conta quantas peças não estão na posição correta (ignorando o 0)
        return sum(
            1 for i in range(9) if estado[i] != 0 and estado[i] != self.objetivo[i]
        )

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
    def a_estrela(self, max_iteracoes: int):
        estados_abertos = []
        estados_fechados = set()
        pais = {self.inicial: None}
        distancias = {self.inicial: 0}

        # Calcula a heurística do estado inicial
        h0 = self.heuristica_pecas_fora_do_lugar(self.inicial)
        # f = g + h, aqui g=0 pois é o estado inicial
        f0 = 0 + h0
        # Tupla armazenada: (f, g, h, estado)
        heapq.heappush(estados_abertos, (f0, 0, h0, self.inicial))
        cont_iteracoes = 0

        # Loop principal do A*
        while estados_abertos and cont_iteracoes < max_iteracoes:
            # Retira o estado com menor f do heap (prioridade)
            f, g, h, estado_atual = heapq.heappop(estados_abertos)
            print(Fore.YELLOW + f"\n[POP] Estado atual; f: {f}, g: {g}, h: {h}")
            self.imprimir_estado(estado_atual)

            # Se o estado atual for o objetivo, finaliza
            if estado_atual == self.objetivo:
                print(Fore.GREEN + "[FIM] Objetivo alcançado")
                caminho = self.reconstruir_caminho(pais)
                stats = {"Custo": g, "Heuristica": h, "f": f, "Caminho": caminho, "Iterações": cont_iteracoes}
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
                    h_novo = self.heuristica_pecas_fora_do_lugar(vizinho)
                    # Calcula f = g + h
                    f_novo = g_novo + h_novo
                    # Adiciona o vizinho ao heap de abertos
                    heapq.heappush(estados_abertos, (f_novo, g_novo, h_novo, vizinho))
                    print(
                        Fore.BLUE
                        + f"[PUSH] Vizinho {vizinho} com f={f_novo}, g={g_novo}, h={h_novo} adicionado"
                    )

            # Mostrar abertos e fechados
            print(Fore.MAGENTA + f"[ABERTOS] {[(f, g, h, s) for f, g, h, s in estados_abertos]}")
            print(Fore.CYAN + f"[FECHADOS] {list(estados_fechados)}")

            estados_fechados.add(estado_atual)
            cont_iteracoes += 1

        print(Fore.RED + f"[ERRO] Sem solução no limite de {max_iteracoes} iterações")
        return 0


def main():
    init(autoreset=True)
    inicio = (1, 2, 3, 4, 0, 6, 7, 5, 8)
    objetivo = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    solver = AEstrela(inicio, objetivo)
    stats = solver.a_estrela(2000)
    if stats:
        solver.imprimir_resultados(stats)


if __name__ == "__main__":
    main()
