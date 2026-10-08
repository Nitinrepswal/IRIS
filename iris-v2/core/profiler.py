import time


class PerformanceProfiler:
    def __init__(self):
        self.records = []

    def measure(self, name, function, *args, **kwargs):
        start = time.perf_counter()

        try:
            result = function(*args, **kwargs)

            elapsed = time.perf_counter() - start

            record = {
                "name": name,
                "time": round(elapsed, 4),
                "success": True
            }

            self.records.append(record)

            return result

        except Exception as error:
            elapsed = time.perf_counter() - start

            record = {
                "name": name,
                "time": round(elapsed, 4),
                "success": False,
                "error": str(error)
            }

            self.records.append(record)

            raise

    def get_records(self):
        return self.records.copy()

    def get_average(self, name):
        times = [
            record["time"]
            for record in self.records
            if record["name"] == name
        ]

        if not times:
            return 0

        return round(
            sum(times) / len(times),
            4
        )

    def get_slowest(self):
        if not self.records:
            return None

        return max(
            self.records,
            key=lambda record: record["time"]
        )

    def clear(self):
        self.records.clear()