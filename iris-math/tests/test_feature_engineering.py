from feature_engineering import FeatureEngineer


data = [
    [2, 60],
    [4, 75],
    [6, 85],
    [1, 50]
]

engineer = FeatureEngineer()


# Create a new feature
def study_score(row):
    return row[0] * row[1]


new_data = engineer.add_feature(data, study_score)

print("Original data:")
for row in data:
    print(row)

print("\nData with new feature:")
for row in new_data:
    print(row)


# Select features
selected_data = engineer.select_features(data, [0])

print("\nSelected feature:")
for row in selected_data:
    print(row)