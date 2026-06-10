def merge_sort(arr):
    """
    Merge Sort - O(n log n) em todos os casos.
    Retorna o array ordenado e a contagem de movimentações (escritas durante a intercalação).
    """
    moves = [0]

    def merge(a, left, mid, right):
        L = a[left:mid + 1]
        R = a[mid + 1:right + 1]
        i = j = 0
        k = left
        while i < len(L) and j < len(R):
            if L[i] <= R[j]:
                a[k] = L[i]
                i += 1
            else:
                a[k] = R[j]
                j += 1
            moves[0] += 1
            k += 1
        while i < len(L):
            a[k] = L[i]
            i += 1
            k += 1
            moves[0] += 1
        while j < len(R):
            a[k] = R[j]
            j += 1
            k += 1
            moves[0] += 1

    def sort(a, left, right):
        if left < right:
            mid = (left + right) // 2
            sort(a, left, mid)
            sort(a, mid + 1, right)
            merge(a, left, mid, right)

    a = arr[:]
    sort(a, 0, len(a) - 1)
    return a, moves[0]


if __name__ == "__main__":
    import random
    random.seed(42)
    vetor = [random.randint(1, 100) for _ in range(20)]
    print("Original:", vetor)
    ordenado, mov = merge_sort(vetor)
    print("Ordenado:", ordenado)
    print(f"Movimentações: {mov}")
