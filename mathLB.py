class mathLib:
    def __init__(self):
        pass

    def multiply_matrices(self, *matrices):
        # Matrices 4x4
        for matrix in matrices:
            if len(matrix) != 4 or any(len(row) != 4 for row in matrix):
                raise ValueError("Todas las matrices deben ser de tamaño 4x4")
            
        result = matrices[0]

        # Multiplicamos la matriz de resultado (primera) por cada matriz agregada
        for i in range(1, len(matrices)):
            next_matrix = matrices[i]
            new_result = [[0, 0, 0, 0] for _ in range(4)]
            for i in range(4):
                for j in range(4):
                    for k in range(4):
                        new_result[i][j] += result[i][k] * next_matrix[k][j]
            result = new_result
        # print(result)
        return result

    def multiply_matrix_vector(self, matrix, vector):
        if len(matrix[0]) != len(vector):
            raise ValueError("La matriz y el vector deben tener la misma longitud")
        result = [0 for _ in range(len(vector))]
        for i in range(len(matrix)):
            for j in range(len(vector)):
                result[i] += matrix[i][j] * vector[j]
        return result
