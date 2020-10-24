from dynamic_accumulator.dynamic_accumulator import NeighboursMap, DynamicAccumulator
from tests.test_base import BaseTest
from matplotlib import pyplot as plt


class PerformanceTests(BaseTest):
    def test_analyze_random(self):
        x = range(1, 10002, 500)
        y1, y2, y3, y4 = [], [], [], []
        for i in x:
            nm = NeighboursMap()
            da = DynamicAccumulator(neighbours_map=self.NM)
            y1.append(self.n_random_operations_perf(da, nm, i))

            nm = NeighboursMap()
            da = DynamicAccumulator(10, neighbours_map=self.NM)
            y2.append(self.n_random_operations_perf(da, nm, i))

            nm = NeighboursMap()
            da = DynamicAccumulator(50, neighbours_map=self.NM)
            y3.append(self.n_random_operations_perf(da, nm, i))

            nm = NeighboursMap()
            da = DynamicAccumulator(80, neighbours_map=self.NM)
            y4.append(self.n_random_operations_perf(da, nm, i))

        self.draw_plot('Random operations', x, y1, y2, y3, y4)

    def test_analyze_adds_and_removes(self):
        x = range(1, 10002, 500)
        y1, y2, y3, y4 = [], [], [], []
        for i in x:
            nm = NeighboursMap()
            da = DynamicAccumulator(neighbours_map=self.NM)
            y1.append(self.n_adds_and_removes_perf(da, nm, i))

            nm = NeighboursMap()
            da = DynamicAccumulator(10, neighbours_map=self.NM)
            y2.append(self.n_adds_and_removes_perf(da, nm, i))

            nm = NeighboursMap()
            da = DynamicAccumulator(50, neighbours_map=self.NM)
            y3.append(self.n_adds_and_removes_perf(da, nm, i))

            nm = NeighboursMap()
            da = DynamicAccumulator(80, neighbours_map=self.NM)
            y4.append(self.n_adds_and_removes_perf(da, nm, i))

        self.draw_plot('Sequential operations', x, y1, y2, y3, y4)

    @staticmethod
    def draw_plot(title, x, y1, y2, y3, y4):
        plt.title(title)
        plt.plot(x, y1, '-', label='1 initial capacity')
        plt.plot(x, y2, '--', label='10 initial capacity')
        plt.plot(x, y3, '-.', label='50 initial capacity')
        plt.plot(x, y4, ':', label='80 initial capacity')
        plt.legend()
        plt.xlabel("operations")
        plt.ylabel("ms")
        plt.show()
