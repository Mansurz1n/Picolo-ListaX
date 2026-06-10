import sys
sys.setrecursionlimit(300000)


def quick_sort(arr):
    """
    Quick Sort com pivô mediana de 3 - O(n log n) no caso médio, O(n²) no pior caso.
    O pivô mediana de 3 evita o pior caso em arrays já ordenados.
    Retorna o array ordenado e a contagem de trocas.
    """
    swaps = [0]

    def partition(a, low, high):
        # Escolhe o pivô como mediana entre a[low], a[mid] e a[high]
        mid = (low + high) // 2
        if a[low] > a[mid]:
            a[low], a[mid] = a[mid], a[low]
            swaps[0] += 1
        if a[low] > a[high]:
            a[low], a[high] = a[high], a[low]
            swaps[0] += 1
        if a[mid] > a[high]:
            a[mid], a[high] = a[high], a[mid]
            swaps[0] += 1
        # Coloca o pivô na penúltima posição
        pivot = a[mid]
        a[mid], a[high - 1] = a[high - 1], a[mid]
        swaps[0] += 1
        i = low
        for j in range(low, high):
            if a[j] <= pivot:
                a[i], a[j] = a[j], a[i]
                swaps[0] += 1
                i += 1
        a[i], a[high] = a[high], a[i]
        swaps[0] += 1
        return i

    def sort(a, low, high):
        if low < high:
            pi = partition(a, low, high)
            sort(a, low, pi - 1)
            sort(a, pi + 1, high)

    a = arr[:]
    sort(a, 0, len(a) - 1)
    return a, swaps[0]


if __name__ == "__main__":
    import random
    random.seed(42)
    vetor = [random.randint(1, 100) for _ in range(20)]
    print("Original:", vetor)
    ordenado, trocas = quick_sort(vetor)
    print("Ordenado:", ordenado)
    print(f"Trocas: {trocas}")
