class SGD:
    def __init__(self, learning_rate=0.01):
        self.learning_rate = learning_rate

    def update(self, parameter, gradient):
        return parameter - (
            self.learning_rate * gradient
        )


class Momentum:
    def __init__(
        self,
        learning_rate=0.01,
        momentum=0.9
    ):
        self.learning_rate = learning_rate
        self.momentum = momentum
        self.velocity = 0.0

    def update(self, parameter, gradient):
        self.velocity = (
            self.momentum * self.velocity
            + gradient
        )

        return parameter - (
            self.learning_rate * self.velocity
        )


class Adam:
    def __init__(
        self,
        learning_rate=0.001,
        beta1=0.9,
        beta2=0.999,
        epsilon=1e-8
    ):
        self.learning_rate = learning_rate
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon

        self.m = 0.0
        self.v = 0.0
        self.t = 0

    def update(self, parameter, gradient):
        self.t += 1

        self.m = (
            self.beta1 * self.m
            + (1 - self.beta1) * gradient
        )

        self.v = (
            self.beta2 * self.v
            + (1 - self.beta2) * (gradient ** 2)
        )

        m_hat = self.m / (
            1 - self.beta1 ** self.t
        )

        v_hat = self.v / (
            1 - self.beta2 ** self.t
        )

        update = (
            self.learning_rate
            * m_hat
            / ((v_hat ** 0.5) + self.epsilon)
        )

        return parameter - update