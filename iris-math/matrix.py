class Matrix:

    # create matrix
    def __init__(self, values):
        if not values:
            raise ValueError("Matrix cannot be empty")

        columns = len(values[0])

        if columns == 0:
            raise ValueError("Matrix rows cannot be empty")

        for row in values:
            if len(row) != columns:
                raise ValueError("All rows must have the same size")

        self.values = values

    # show matrix
    def __repr__(self):
        return f"{self.values}"

    # matrix shape
    @property
    def shape(self):
        return (len(self.values), len(self.values[0]))