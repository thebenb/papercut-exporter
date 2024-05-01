class Metric:
    def __init__(self, name, value, comment):
        self.name = name
        self.value = value
        self.comment = comment

    def __str__(self):
        return f"{self.name}: {self.value}"
