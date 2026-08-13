from vector import Vector


# Basic vectors
a = Vector([2, 4, 6])
b = Vector([1, 2, 3])

print("Vector:", a)

# Addition
print("Add:", a + b)

# Subtraction
print("Sub:", a - b)

# Scalar multiplication
print("Multiply:", a * 3)

# Reverse scalar multiplication
print("Reverse Multiply:", 3 * a)

# Scalar division
print("Divide:", a / 2)

# Equality
c = Vector([2, 4, 6])

print("Equal:", a == c)
print("Not Equal:", a == b)


# Invalid operations
try:
    print(a + 5)
except TypeError as e:
    print("Invalid Add:", e)

try:
    print(a - 5)
except TypeError as e:
    print("Invalid Sub:", e)


# Dot product
d = Vector([2, 4, 6])
e = Vector([1, 2, 3])

print("Dot Product:", d.dot(e))


# Magnitude
f = Vector([3, 4])

print("Magnitude:", f.magnitude())


# Normalization
print("Normalized:", f.normalize())
print("Normalized Magnitude:", f.normalize().magnitude())


# Zero vector normalization
zero = Vector([0, 0])

try:
    print("Zero Normalized:", zero.normalize())
except ValueError as e:
    print("Zero Vector Error:", e)


# Distance
x = Vector([1, 2])
y = Vector([4, 6])

print("Distance:", x.distance_to(y))