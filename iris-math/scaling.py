import math

class MinMaxScaler:
    def __init__(self):
        self.min_values = None
        self.max_values = None

    def fit(self, data):
        self.min_values = [
            min(row[j] for row in data)
            for j in range(len(data[0]))
        ]

        self.max_values = [
            max(row[j] for row in data)
            for j in range(len(data[0]))
        ]

    def transform(self, data):
        if self.min_values is None or self.max_values is None:
            raise ValueError("Scaler has not been fitted")

        result = []

        for row in data:
            scaled_row = []

            for j, value in enumerate(row):
                minimum = self.min_values[j]
                maximum = self.max_values[j]

                if maximum == minimum:
                    scaled_value = 0.0
                else:
                    scaled_value = (value - minimum) / (maximum - minimum)

                scaled_row.append(scaled_value)

            result.append(scaled_row)

        return result

    def fit_transform(self, data):
        self.fit(data)
        return self.transform(data)


class StandardScaler:
    def __init__(self):
        self.means = None
        self.stds = None

    def fit(self, data):
        columns = len(data[0])

        self.means = [
            sum(row[j] for row in data) / len(data)
            for j in range(columns)
        ]

        self.stds = []

        for j in range(columns):
            variance = sum(
                (row[j] - self.means[j]) ** 2
                for row in data
            ) / len(data)

            self.stds.append(math.sqrt(variance))

    def transform(self, data):
        if self.means is None or self.stds is None:
            raise ValueError("Scaler has not been fitted")

        result = []

        for row in data:
            scaled_row = []

            for j, value in enumerate(row):
                if self.stds[j] == 0:
                    scaled_value = 0.0
                else:
                    scaled_value = (value - self.means[j]) / self.stds[j]

                scaled_row.append(scaled_value)

            result.append(scaled_row)

        return result

    def fit_transform(self, data):
        self.fit(data)
        return self.transform(data)