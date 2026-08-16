from svm_margin import SVMMargin


model = SVMMargin(
    weight=1.0,
    bias=-5.0
)

features = [2, 4, 6, 8]
labels = [0, 0, 1, 1]

for feature, label in zip(features, labels):
    score = model.score(feature)
    margin = model.margin_value(feature, label)
    loss = model.hinge_loss(feature, label)
    support = model.is_support_vector(feature, label)

    print(
        "Feature:", feature,
        "Label:", label,
        "Score:", score,
        "Margin:", margin,
        "Loss:", loss,
        "Support Vector:", support
    )