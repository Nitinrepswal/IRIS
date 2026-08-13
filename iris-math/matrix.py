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

    # matrix * scalar
    def __mul__(self, scalar):
        if isinstance(scalar, Matrix):
            return self.multiply_matrix(scalar)

        if isinstance(scalar, Vector):
            return self.multiply_vector(scalar)

        result = []

        for i in range(len(self.values)):
            row = []

            for j in range(len(self.values[0])):
                row.append(self.values[i][j] * scalar)

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