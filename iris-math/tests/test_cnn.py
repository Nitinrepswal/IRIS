import torch
import torch.nn as nn


class SimpleCNN(nn.Module):

    def __init__(self):
        super().__init__()

        # Convolution layer
        self.conv = nn.Conv2d(
            in_channels=1,
            out_channels=4,
            kernel_size=3
        )

        # Activation
        self.relu = nn.ReLU()

        # Pooling
        self.pool = nn.MaxPool2d(
            kernel_size=2
        )

        # After convolution:
        # 6x6 -> 4x4
        #
        # After pooling:
        # 4x4 -> 2x2
        #
        # 4 feature maps × 2 × 2 = 16
        self.fc = nn.Linear(
            4 * 2 * 2,
            2
        )

    def forward(self, x):

        print("Input shape:", x.shape)

        # Convolution
        x = self.conv(x)
        print("After convolution:", x.shape)

        # ReLU
        x = self.relu(x)
        print("After ReLU:", x.shape)

        # Max pooling
        x = self.pool(x)
        print("After pooling:", x.shape)

        # Flatten
        x = x.view(x.size(0), -1)
        print("After flatten:", x.shape)

        # Fully connected layer
        x = self.fc(x)
        print("Final output:", x.shape)

        return x


# --------------------------------------------------
# Create a simple 6x6 grayscale image
# --------------------------------------------------

x = torch.tensor([
    [
        [0., 0., 0., 0., 0., 0.],
        [0., 1., 1., 1., 1., 0.],
        [0., 1., 1., 1., 1., 0.],
        [0., 1., 1., 1., 1., 0.],
        [0., 1., 1., 1., 1., 0.],
        [0., 0., 0., 0., 0., 0.]
    ]
])

# Add batch dimension
# [1, 6, 6] -> [1, 1, 6, 6]
x = x.unsqueeze(0)


# --------------------------------------------------
# Create CNN
# --------------------------------------------------

model = SimpleCNN()


# --------------------------------------------------
# Forward pass
# --------------------------------------------------

output = model(x)


# --------------------------------------------------
# Display result
# --------------------------------------------------

print("\nOutput:")
print(output)