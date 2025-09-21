import heapq
import time
from colorama import init, Fore, Back, Style


class CustoUniforme:
    def __init__(self, objetivo: tuple):
        self.objetivo = objetivo

    def imprimir_estado(self, estado):
        tuple = [estado[i : i + 3] for i in range(0, 9, 3)]
        for row in tuple:
            print(" ".join(str(x) if x != 0 else "_" for x in row))
        print()

    def imprimir_resultados(self, stats):
        print(Fore.BLUE + f"Custo: {stats['Custo']}")
        print("Caminho:")
        for estado in stats["Caminho"]:
            self.imprimir_estado(estado)
        print(f"Iterações: {stats['Iterações']}")
        print(f"Tempo: {stats['Tempo']}")

    # Essa função aqui é toda quase toda Chat, só simplificada
    def definir_vizinhos(self, estado):
        estado = tuple(estado)
        vizinhos = []
        index_zero = estado.index(0)  # Posição do espaço vazio
        linha, col = divmod(index_zero, 3)  # Muda

        # Troca o 0 com as posições possiveis (cima, baixo, lados...)
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
            # Trocas de indexes
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
        # Heap para facilitar a fila de prioridade
        # Heapheapq.heappop(estados_abertos) vai trazer o estado com menos custo
        heapq.heappush(estados_abertos, (0, inicio))
        cont_iteracoes = 0

        while len(estados_abertos) > 0 and cont_iteracoes < max_iteracoes:

            # Retira o primeiro estado na lista de prioridade do Heap e a dist
            dist, estado_atual = heapq.heappop(estados_abertos)
            print(Fore.YELLOW + f"\n[POP] Estado atual; Dist: {dist}")
            self.imprimir_estado(estado_atual)

            # Se for o estado objetivo, para o algo e retorna o caminho, distancia e num de iterações
            if estado_atual == self.objetivo:
                tempo_fim = time.time()
                print(Fore.GREEN + "[FIM] Objetivo alcançado")
                caminho = self.reconstruir_caminho(pais)
                stats = {
                    "Custo": dist,
                    "Caminho": caminho,
                    "Iterações": cont_iteracoes,
                    "Tempo": tempo_fim - tempo_inicio,
                }
                return stats

            # Ignora o estado se ele já esta na lista dos fechados
            if estado_atual in estados_fechados:
                continue

            # Pegar os vizinhos
            vizinhos = self.definir_vizinhos(estado_atual)

            for vizinho in vizinhos:
                # Pular se o vizinho já estiver fechado
                if vizinho in estados_fechados:
                    continue

                # Distância do estado anterior até o vizinho novo
                dist_nova = dist + 1

                # Pegar a distância do vizinho se tiver, se não definir como infinita
                if vizinho in distancias.keys():
                    dist_vizinho = distancias[vizinho]
                else:
                    dist_vizinho = float("inf")  # Isso seria o infinito

                # Se a distância for menor, atualiza distancias e os pais
                if dist_nova < dist_vizinho:
                    distancias[vizinho] = dist_nova
                    pais[vizinho] = estado_atual
                    heapq.heappush(estados_abertos, (dist_nova, vizinho))
                    print(
                        Fore.BLUE
                        + f"[PUSH] Vizinho {vizinho} adicionado aos estados abertos"
                    )

            # Fecha o estado atual, atualiza as iterações
            estados_fechados.append(estado_atual)
            cont_iteracoes += 1

        # Se passar do número máximo de iterações, retorna 0
        print(Fore.RED + f"[ERRO] Sem solução no limite de {max_iteracoes} iterações")
        return 0

def main():
    init(autoreset=True)
    inicios = [
        (1, 2, 3, 4, 0, 6, 7, 5, 8),  # fácil
        (1, 2, 3, 5, 0, 6, 4, 7, 8),  # médio 1
        (3, 0, 6, 4, 2, 1, 7, 5, 8),  # médio 2
        (0, 4, 7, 2, 3, 1, 6, 8, 5),  # difícil 1
        (7, 2, 4, 5, 0, 6, 8, 3, 1),  # difícil 2
    ]
    objetivo = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    custo_uniforme = CustoUniforme(objetivo)
    stats = []

    for i, inicio in enumerate(inicios):
        print(Fore.MAGENTA + "\n" + "=" * 40)
        print(Fore.MAGENTA + f"=========== TESTE {i} ===========")
        print(Fore.MAGENTA + "=" * 40 + "\n")
        print("Estado inicial:")
        custo_uniforme.imprimir_estado(inicio)

        resultado = custo_uniforme.custo_uniforme(inicio, 100000)
        stats.append(resultado)

        print(Fore.MAGENTA + "=" * 40)
        print(Fore.MAGENTA + f"========= FIM TESTE {i} =========")
        print(Fore.MAGENTA + "=" * 40 + "\n")

    print(Fore.CYAN + "\n" + "=" * 40)
    print(Fore.CYAN + "=========== RESUMO FINAL ===========")
    print(Fore.CYAN + "=" * 40 + "\n")

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
