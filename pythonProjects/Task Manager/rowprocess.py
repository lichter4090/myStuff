from psutil import Process, cpu_count

amount_cpu = cpu_count()
first = True


class RowProcess:
    def __init__(self, process: Process):
        self.id = process.pid
        self.name = process.name()

        self.percent = process.cpu_percent(interval=None)
        self.percent /= amount_cpu

        self.data = self.id, self.name, self.percent

    @staticmethod
    def get_titles():
        return "PID", "Name", "CPU"

    @staticmethod
    def get_cpu_idx():
        return 2

    def get_col(self):
        return self.data

    def __call__(self):
        return self.get_col()

    def __getitem__(self, item):
        return self.data[item]
