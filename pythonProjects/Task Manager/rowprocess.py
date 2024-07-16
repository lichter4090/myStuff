from psutil import Process, cpu_count

amount_cpu = cpu_count()
first = True


def round_two_dig(num: float):
    return float(f"{num:.2f}")


class RowProcess:
    def __init__(self, process: Process):
        self.id = process.pid
        self.name = process.name()
        self.username = process.username()

        self.percent = process.cpu_percent(interval=None)
        self.percent /= amount_cpu
        self.percent = round_two_dig(self.percent)

        self.memory_usage = process.memory_info().rss / (1024 * 1024)
        self.memory_usage = round_two_dig(self.memory_usage)

        self.children = []
        self.has_parent = False  # Assume no parent by default

        try:
            self.children = [RowProcess(c) for c in process.children()]

            self.p = process.parent()
            if self.p:
                self.has_parent = True

        except Exception:
            pass

        self.data = self.id, self.percent, self.memory_usage

    @staticmethod
    def get_titles():
        return "PID", "CPU", "Memory"

    @staticmethod
    def get_cpu_idx():
        return 1

    @staticmethod
    def get_width_of_cols():
        return 70, 140, 140

    def get_col(self):
        return self.data

    def get_name(self):
        return self.name

    def get_cpu_usage(self):
        return self.percent

    def get_memory_usage(self):
        return self.memory_usage

    def get_children(self):
        return self.children

    def get_has_parent(self):
        return self.has_parent

    def __call__(self):
        return self.get_col()

    def __getitem__(self, item):
        return self.data[item]
