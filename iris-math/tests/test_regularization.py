from regularization import l1_penalty, l2_penalty


weights = [2.0, -3.0, 1.0]

strength = 0.1


l1 = l1_penalty(weights, strength)
l2 = l2_penalty(weights, strength)


print("Weights:", weights)
print("Regularization strength:", strength)
print("L1 penalty:", l1)
print("L2 penalty:", l2)