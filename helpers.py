
def print_adj_matrix(matrix):
    print("   ", *list(map(lambda x: str(x).zfill(3), range(len(matrix)))))
    for idx, row in enumerate(matrix):
        tx_row = map(lambda x: "  T" if x else "   ", row)
        print(str(idx).zfill(3), *list(tx_row))


def print_matrix(matrix):
    print("   ", *list(map(lambda x: str(x).zfill(3), range(len(matrix[0])))))
    for idx, row in enumerate(matrix):
        tx_row = map(lambda x: str(x).rjust(3), row)
        print(str(idx).zfill(3), *list(tx_row))

