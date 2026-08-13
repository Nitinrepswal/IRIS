class Vector:
    def __init__(self, values):
        self.values = values

    def __repr__(self):
        return f"{self.values}"

    def _check_size(self, other):
        if len(self.values) != len(other.values):
            raise ValueError("Vectors must have the same size")

    def __add__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented

        self._check_size(other)

        result = []

        for i in range(len(self.values)):
            result.append(self.values[i] + other.values[i])

        return Vector(result)

    def __sub__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented

        self._check_size(other)

        result = []

        for i in range(len(self.values)):
            result.append(self.values[i] - other.values[i])

        return Vector(result)

    def __mul__(self, scalar):
        result = []

        for i in range(len(self.values)):
            result.append(self.values[i] * scalar)

        return Vector(result)

    def __rmul__(self, scalar):
        return self * scalar

    def __truediv__(self, scalar):
        if scalar == 0:
            raise ZeroDivisionError("Cannot divide a vector by zero")

        result = []

        for i in range(len(self.values)):
            result.append(self.values[i] / scalar)

        return Vector(result)

    def __eq__(self, other):
        if not isinstance(other, Vector):
            return False

        return self.values == other.values

    def dot(self, other):
        if not isinstance(other, Vector):
            raise TypeError("Dot product requires another Vector")

        self._check_size(other)

        result = 0

        for i in range(len(self.values)):
            result += self.values[i] * other.values[i]

        return result

    def magnitude(self):
        total = 0

        for value in self.values:
            total += value ** 2

        return total ** 0.5

    def normalize(self):
        magnitude = self.magnitude()

        if magnitude == 0:
            raise ValueError("Cannot normalize a zero vector")

        result = []

        for value in self.values:
            result.append(value / magnitude)

        return Vector(result)

    def distance_to(self, other):
        if not isinstance(other, Vector):
            raise TypeError("Distance requires another Vector")

        self._check_size(other)

        return (self - other).magnitude()