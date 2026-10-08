import time


class ToolProfiler:
    def __init__(self):
        self.records = []

    def execute(self, tool, arguments=None):
        start = time.perf_counter()

        try:
            if arguments is None:
                arguments = {}

            result = tool.execute(**arguments)

            elapsed = time.perf_counter() - start

            self.records.append({
                "tool": tool.name,
                "time": round(elapsed, 4),
                "success": result.get("success", False)
            })

            return result

        except Exception as error:
            elapsed = time.perf_counter() - start

            self.records.append({
                "tool": tool.name,
                "time": round(elapsed, 4),
                "success": False,
                "error": str(error)
            })

            raise

    def get_records(self):
        return self.records.copy()

    def get_average(self, tool_name):
        times = [
            record["time"]
            for record in self.records
            if record["tool"] == tool_name
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