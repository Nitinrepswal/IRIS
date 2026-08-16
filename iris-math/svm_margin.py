class SVMMargin:
    def __init__(self, weight=1.0, bias=0.0):
        self.weight = weight
        self.bias = bias

    def score(self, value):
        return self.weight * value + self.bias

    def margin_value(self, value, label):
        if label == 0:
            label = -1

        return label * self.score(value)

    def hinge_loss(self, value, label):
        margin = self.margin_value(value, label)

        return max(0, 1 - margin)

    def is_support_vector(self, value, label):
        margin = self.margin_value(value, label)

        return margin <= 1