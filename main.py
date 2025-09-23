from a_estrela import AEstrela
from custo_uniforme import CustoUniforme

def validar_tabuleiro(tabuleiro_str):
    try:
        numeros = list(map(int, tabuleiro_str.split(",")))
    except ValueError:
        return False
    if len(numeros) != 9:
        return False
    if set(numeros) != set(range(9)):
        return False
    return True

def main():
    objetivo = (1, 2, 3, 4, 5, 6, 7, 8, 0)

    # Loop até o input estar correto
    while True:
        tabuleiro_recebido = input("Digite o tabuleiro inicial (ex: 1,2,3,4,5,6,7,0,8): ")
        if validar_tabuleiro(tabuleiro_recebido):
            inicio = tuple(map(int, tabuleiro_recebido.split(",")))
            break
        else:
            print("Formato inválido! Certifique-se de digitar 9 números de 0 a 8, separados por vírgula, sem repetição.")

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
            heuristica = ae.heuristica_distancia_manhatthan
        else:
            heuristica = ae.heuristica_nao_admissivel
        resultado = ae.a_estrela(inicio, heuristica, 100000)
    else:
        print("Opção inválida!")
        return

    if resultado:
        print(f"\nTotal de nodos visitados: {resultado['NodosVisitados']}")
        print(f"Tamanho do caminho: {len(resultado['Caminho'])}")
        print(f"Tempo de execução da busca (segundos): {resultado['TempoBusca']:.4f}")
        print(f"Tempo total (incluindo reconstrução e gravação): {resultado['TempoTotal']:.4f}")
        print(f"Maior tamanho da fronteira: {resultado['MaiorFronteira']}")

if __name__ == "__main__":
    main()
