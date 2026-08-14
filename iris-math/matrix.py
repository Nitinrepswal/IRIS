from vector import Vector

class Matrix:

    # create matrix
    def __init__(self, values):
        if not values:
            raise ValueError("Matrix cannot be empty")

        columns = len(values[0])

        if columns == 0:
            raise ValueError("Matrix rows cannot be empty")

        for row in values:
            if len(row) != columns:
                raise ValueError("All rows must have the same size")

        self.values = values

    # show matrix
    def __repr__(self):
        return f"{self.values}"

    # matrix shape
    @property
    def shape(self):
        return (len(self.values), len(self.values[0]))

    # check same shape
    def _check_shape(self, other):
        if self.shape != other.shape:
            raise ValueError("Matrices must have the same shape")

    # matrix + matrix
    def __add__(self, other):
        if not isinstance(other, Matrix):
            return NotImplemented

        self._check_shape(other)

        result = []

        for i in range(len(self.values)):
            row = []

            for j in range(len(self.values[0])):
                row.append(self.values[i][j] + other.values[i][j])

            result.append(row)

        return Matrix(result)

    # matrix - matrix
    def __sub__(self, other):
        if not isinstance(other, Matrix):
            return NotImplemented

        self._check_shape(other)

        result = []

        for i in range(len(self.values)):
            row = []

            for j in range(len(self.values[0])):
                row.append(self.values[i][j] - other.values[i][j])

            result.append(row)

        return Matrix(result)

    # matrix * scalar, vector or matrix
    def __mul__(self, other):
        if isinstance(other, Matrix):
            return self.multiply_matrix(other)

        if isinstance(other, Vector):
            return self.multiply_vector(other)

        result = []

        for i in range(len(self.values)):
            row = []

            for j in range(len(self.values[0])):
                row.append(self.values[i][j] * other)

            result.append(row)

        return Matrix(result)

    # scalar * matrix
    def __rmul__(self, scalar):
        return self * scalar

    # compare matrices
    def __eq__(self, other):
        if not isinstance(other, Matrix):
            return False

        return self.values == other.values

    # transpose
    def transpose(self):
        result = []

        for j in range(len(self.values[0])):
            row = []

            for i in range(len(self.values)):
                row.append(self.values[i][j])

            result.append(row)

        return Matrix(result)

    # matrix * vector
    def multiply_vector(self, vector):
        if not isinstance(vector, Vector):
            raise TypeError("Matrix multiplication requires a Vector")

        if len(self.values[0]) != len(vector.values):
            raise ValueError("Matrix columns must match vector size")

        result = []

        for row in self.values:
            total = 0

            for i in range(len(row)):
                total += row[i] * vector.values[i]

            result.append(total)

        return Vector(result)

    # matrix * matrix
    def multiply_matrix(self, other):
        if not isinstance(other, Matrix):
            raise TypeError("Matrix multiplication requires another Matrix")

        if self.shape[1] != other.shape[0]:
            raise ValueError("Matrix dimensions are not compatible")

        result = []

        for i in range(self.shape[0]):
            row = []

            for j in range(other.shape[1]):
                total = 0

                for k in range(self.shape[1]):
                    total += self.values[i][k] * other.values[k][j]

                row.append(total)

            result.append(row)

        return Matrix(result)

    # determinant
    def determinant(self):
        rows, columns = self.shape

        if rows != columns:
            raise ValueError("Determinant requires a square matrix")

        # 1×1
        if rows == 1:
            return self.values[0][0]

        # 2×2
        if rows == 2:
            a = self.values[0][0]
            b = self.values[0][1]
            c = self.values[1][0]
            d = self.values[1][1]

            return a * d - b * c

        # 3×3 and larger
        total = 0

        for j in range(columns):
            minor_matrix = []

            for i in range(1, rows):
                row = []

                for k in range(columns):
                    if k != j:
                        row.append(self.values[i][k])

                minor_matrix.append(row)

            minor = Matrix(minor_matrix).determinant()
            cofactor = ((-1) ** j) * minor

            total += self.values[0][j] * cofactor

        return total

    # find minor
    def minor(self, row, column):
        rows, columns = self.shape

        if rows != columns:
            raise ValueError("Minor requires a square matrix")

        if row < 0 or row >= rows or column < 0 or column >= columns:
            raise IndexError("Minor index out of range")

        minor_matrix = []

        for i in range(rows):
            if i == row:
                continue

            current_row = []

            for j in range(columns):
                if j != column:
                    current_row.append(self.values[i][j])

            minor_matrix.append(current_row)

        return Matrix(minor_matrix)

    # find cofactor
    def cofactor(self, row, column):
        minor_value = self.minor(row, column).determinant()

        sign = (-1) ** (row + column)

        return sign * minor_value

    # cofactor matrix
    def cofactor_matrix(self):
        rows, columns = self.shape

        if rows != columns:
            raise ValueError("Cofactor matrix requires a square matrix")

        result = []

        for i in range(rows):
            row = []

            for j in range(columns):
                row.append(self.cofactor(i, j))

            result.append(row)

        return Matrix(result)

    # adjugate matrix
    def adjugate(self):
        return self.cofactor_matrix().transpose()

    # inverse matrix
    def inverse(self):
        determinant = self.determinant()

        if determinant == 0:
            raise ValueError("Singular matrix has no inverse")

        return (1 / determinant) * self.adjugate()

    # solve AX = B
    def solve(self, b):
        if not isinstance(b, Vector):
            raise TypeError("B must be a Vector")

        if self.shape[0] != self.shape[1]:
            raise ValueError("Matrix must be square")

        if len(b.values) != self.shape[0]:
            raise ValueError("Vector size must match matrix rows")

        return self.inverse() * b