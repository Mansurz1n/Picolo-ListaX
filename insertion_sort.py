def insertion_sort(arr):
    """
    Insertion Sort - O(n²) no caso médio e pior caso, O(n) no melhor caso.
    Retorna o array ordenado e a contagem de movimentações.
    """
    moves = 0
    a = arr[:]
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
            moves += 1
        a[j + 1] = key
        if j + 1 != i:
            moves += 1  # conta a inserção do key na posição final
    return a, moves


if __name__ == "__main__":
    import random
    random.seed(42)
    vetor = [random.randint(1, 100) for _ in range(20)]
    print("Original:", vetor)
    ordenado, mov = insertion_sort(vetor)
    print("Ordenado:", ordenado)
    print(f"Movimentações: {mov}")
