import math
from math import isclose

def barycentric_coords(A, B, C, P):

    areaPCB = abs((P[0]*C[1] + C[0]*B[1] + B[0]*P[1]) - 
                  (P[1]*C[0] + C[1]*B[0] + B[1]*P[0]))

    areaACP = abs((A[0]*C[1] + C[0]*P[1] + P[0]*A[1]) - 
                  (A[1]*C[0] + C[1]*P[0] + P[1]*A[0]))

    areaABP = abs((A[0]*B[1] + B[0]*P[1] + P[0]*A[1]) - 
                  (A[1]*B[0] + B[1]*P[0] + P[1]*A[0]))

    areaABC = abs((A[0]*B[1] + B[0]*C[1] + C[0]*A[1]) - 
                  (A[1]*B[0] + B[1]*C[0] + C[1]*A[0]))
    if areaABC == 0:
        return None
    u = areaPCB / areaABC
    v = areaACP / areaABC
    w = areaABP / areaABC

    # Si cada coordenada esta entre 0 a 1 y la suma de las tres
    # es igual a 1, entonces son validas.
    if 0<=u<=1 and 0<=v<=1 and 0<=w<=1 and isclose(u+v+w, 1.0):
        return (u, v, w)
    else:
        return None

class Matrix:
    # Representa una matriz como lo hace numpy

    def __init__(self, matx) -> None:

        self.matx = matx
        self.rows = len(matx)
        self.cols = len(matx[0])
        if len(matx) != 4 or len(matx[0]) != 4:
            raise ValueError("Todas las matrices deben ser de tamaño 4x4")

    # permite utilizar el operador * para la clase Matrix
    def __mul__(self, newMatrix):
        # hace mutliplicacion de cualquier cantidad de matrices 4x4 
        result = [[0, 0, 0, 0] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    result[i][j] += self.matx[i][k] * newMatrix.matx[k][j]
        return Matrix(result)
    
    # permite utilizar el operador @ para la clase matrix
    def __matmul__(self, newVector):
        # mutiplica una matriz por vector
        if len(newVector.data) != 4:
            raise ValueError("El vector debe tener tamaño 4")
        result = [0, 0, 0, 0]
        for i in range(4):
            for j in range(4):
                result[i] += self.matx[i][j] * newVector.data[j]
        return Vector(result)
    

    # calcula la inversa de una matriz por el metodo de la adjunta
    def inversa(self):
        #  calcular la matriz menor
        def minor(matrix, row, col):
            # Eliminar la fila y la columna especificadas y retornar la matriz 3x3 resultante
            return [[matrix[i][j] for j in range(len(matrix[0])) if j != col] for i in range(len(matrix)) if i != row]

        # Función para calcular el determinante de una matriz
        def det(matrix):
            if len(matrix) == 2:
                return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

             # Calcula el determinante de una matriz expandiéndola a lo largo de su primera fila
            determinant = 0
            for c in range(len(matrix)):
                determinant += ((-1) ** c) * matrix[0][c] * det(minor(matrix, 0, c))
            return determinant
        
         # calcular la matriz de cofactores
        def cofactors(matrix):
            C = []
            for i in range(self.rows):
                row = []
                for j in range(self.cols):
                    # Calcula el cofactor usando el determinante de la matriz menor
                    row.append((((-1) ** (i + j)) * det(minor(matrix, i, j))))
                C.append(row)
            return C
        determinant = det(self.matx)
        if determinant == 0:
            raise ValueError("El determinante de la matriz es cero")
        
        cofactor_matrix = cofactors(self.matx)
        adjoint = [[cofactor_matrix[j][i] for j in range(self.cols)] for i in range(self.rows)] # Transpose the cofactor matrix
        inverse_matrix = [[adjoint[i][j] / determinant for j in range(self.cols)] for i in range(self.rows)]
        return Matrix(inverse_matrix)


class Vector:
    # Crea un vector
    def __init__(self, data):

        self.data = data

    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, key):
        return self.data[key]

    def __mul__(self, value):
        # Si se multiplica por otro vector (producto punto)
        if isinstance(value, Vector):
            return sum(a * b for a, b in zip(self.data, value.data))
        
        # Si se multiplica por un escalar
        elif isinstance(value, (int, float)):
            return Vector([elem * value for elem in self.data])

        else:
            raise ValueError("Unsupported operand type for multiplication")
        
    # Para manejar el caso en que un escalar precede al vector
    def __rmul__(self, value):
        return self * value

    # permite utilizar el operador - para la clase vector
    def __sub__(self, newVector):
         # Resta otro vector de este, elemento por elemento
        result = [self.data[i] - newVector.data[i] for i in range(len(self.data))]
        return Vector(result)

    def normalize(self):
         # Calcula la magnitud del vector
        magnitude = math.sqrt(sum(elem ** 2 for elem in self.data))
        # Divide cada elemento por la magnitud para normalizar
        return self * (1.0 / magnitude)

    def cross(self, otherVector):
        # Verifica que ambos vectores tengan tamaño 3
        if len(self.data) != 3 or len(otherVector.data) != 3:
            raise ValueError("Ambos vectores deben tener tamaño 3 para el producto cruz")

        # Calcula el producto cruz utilizando la fórmula estándar
        result = [
            self.data[1] * otherVector.data[2] - self.data[2] * otherVector.data[1],
            self.data[2] * otherVector.data[0] - self.data[0] * otherVector.data[2],
            self.data[0] * otherVector.data[1] - self.data[1] * otherVector.data[0]
        ]

        return Vector(result)
    
    def dot(self, other) -> float:
    #    producto punto
        if len(self.data) != len(other.data):
            raise ValueError(
                "Dot product is only defined for vectors of the same dimension")

        result = sum(self.data[i] * other.data[i]
                     for i in range(len(self.data)))
        return result
    
    def negate(self) -> 'Vector':
        # negacion de un vector
        result = [-elem for elem in self.data]
        return Vector(result)


def formatMatrix(data):
    
    return Matrix(data)


def formatVector(data):
    return Vector(data)
