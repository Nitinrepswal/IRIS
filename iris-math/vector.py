import math
class Vector:

    # create vector
    def __init__(self, values):
        self.values = values

    # show vector
    def __repr__(self):
        return f"{self.values}"

    # check same size
    def _check_size(self, other):
        if len(self.values) != len(other.values):
            raise ValueError("Vectors must have the same size")

    # vector + vector
    def __add__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented

        self._check_size(other)

        result = []

        for i in range(len(self.values)):
            result.append(self.values[i] + other.values[i])

        return Vector(result)

    # vector - vector
    def __sub__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented

        self._check_size(other)

        result = []

        for i in range(len(self.values)):
            result.append(self.values[i] - other.values[i])

        return Vector(result)

    # vector * scalar
    def __mul__(self, scalar):
        result = []

        for i in range(len(self.values)):
            result.append(self.values[i] * scalar)

        return Vector(result)

    # scalar * vector
    def __rmul__(self, scalar):
        return self * scalar

    # vector / scalar
    def __truediv__(self, scalar):
        if scalar == 0:
            raise ZeroDivisionError("Cannot divide a vector by zero")

        result = []

        for i in range(len(self.values)):
            result.append(self.values[i] / scalar)

        return Vector(result)

    # compare vectors
    def __eq__(self, other):
        if not isinstance(other, Vector):
            return False

        return self.values == other.values

    # dot product
    def dot(self, other):
        if not isinstance(other, Vector):
            raise TypeError("Dot product requires another Vector")

        self._check_size(other)

        result = 0

        for i in range(len(self.values)):
            result += self.values[i] * other.values[i]

        return result

    # vector length
    def magnitude(self):
        total = 0

        for value in self.values:
            total += value ** 2

        return total ** 0.5

    # make unit vector
    def normalize(self):
        magnitude = self.magnitude()

        if magnitude == 0:
            raise ValueError("Cannot normalize a zero vector")

        result = []

        for value in self.values:
            result.append(value / magnitude)

        return Vector(result)

    # distance between vectors
    def distance_to(self, other):
        if not isinstance(other, Vector):
            raise TypeError("Distance requires another Vector")

        self._check_size(other)

        return (self - other).magnitude()

    # project onto another vector
    def project_onto(self, other):
        if not isinstance(other, Vector):
            raise TypeError("Projection requires another Vector")

        self._check_size(other)

        denominator = other.dot(other)

        if denominator == 0:
            raise ValueError("Cannot project onto a zero vector")

        scalar = self.dot(other) / denominator

        return other * scalar

    # angle in radians
    def angle_with(self, other):
        if not isinstance(other, Vector):
            raise TypeError("Angle requires another Vector")

        self._check_size(other)

        magnitude_product = self.magnitude() * other.magnitude()

        if magnitude_product == 0:
            raise ValueError("Cannot calculate angle with a zero vector")

        cosine = self.dot(other) / magnitude_product

        # avoid floating point issues
        cosine = max(-1, min(1, cosine))

        return math.acos(cosine)

    # cross product
    def cross(self, other):
        if not isinstance(other, Vector):
            raise TypeError("Cross product requires another Vector")

        if len(self.values) != 3 or len(other.values) != 3:
            raise ValueError("Cross product requires 3D vectors")

        return Vector([
            self.values[1] * other.values[2] - self.values[2] * other.values[1],
            self.values[2] * other.values[0] - self.values[0] * other.values[2],
            self.values[0] * other.values[1] - self.values[1] * other.values[0]
        ])

    # cross product length
    def cross_magnitude(self, other):
        return self.cross(other).magnitude()