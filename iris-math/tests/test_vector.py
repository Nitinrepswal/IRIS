from vector import Vector

# basic vectors
a = Vector([2, 4, 6])
b = Vector([1, 2, 3])

print("Vector:", a)

# operators
print("Add:", a + b)
print("Sub:", a - b)
print("Multiply:", a * 3)
print("Reverse Multiply:", 3 * a)
print("Divide:", a / 2)

# equality
c = Vector([2, 4, 6])

print("Equal:", a == c)
print("Not Equal:", a == b)

# invalid operations
try:
    print(a + 5)
except TypeError as e:
    print("Invalid Add:", e)

try:
    print(a - 5)
except TypeError as e:
    print("Invalid Sub:", e)

# dot product
d = Vector([2, 4, 6])
e = Vector([1, 2, 3])

print("Dot Product:", d.dot(e))

# magnitude
f = Vector([3, 4])

print("Magnitude:", f.magnitude())

# normalize
print("Normalized:", f.normalize())
print("Normalized Magnitude:", f.normalize().magnitude())

# zero vector
zero = Vector([0, 0])

try:
    print("Zero Normalized:", zero.normalize())
except ValueError as e:
    print("Zero Vector Error:", e)

# distance
x = Vector([1, 2])
y = Vector([4, 6])

print("Distance:", x.distance_to(y))

# projection
print("Projection:", x.project_onto(y))

# angle
angle_a = Vector([1, 0])
angle_b = Vector([0, 1])

print("Angle:", angle_a.angle_with(angle_b))

#cross product
a = Vector([1, 0, 0])
b = Vector([0, 1, 0])

print("Cross Product:", a.cross(b))

# cross product magnitude
print("Cross Magnitude:", a.cross_magnitude(b))