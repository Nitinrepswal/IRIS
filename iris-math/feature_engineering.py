class FeatureEngineer:
    def add_feature(self, data, feature_function):
        result = []

        for row in data:
            new_feature = feature_function(row)
            new_row = row + [new_feature]
            result.append(new_row)

        return result

    def select_features(self, data, indices):
        result = []

        for row in data:
            selected_row = [row[i] for i in indices]
            result.append(selected_row)

        return result