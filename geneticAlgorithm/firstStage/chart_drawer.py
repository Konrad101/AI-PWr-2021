import matplotlib.pyplot as plt


def draw_chart(best_list, worst_list, avg_list, size):
    plt.plot(size, best_list, label="best")
    plt.plot(size, worst_list, label="worst")
    plt.plot(size, avg_list, label="avg")
    plt.legend()
    plt.show()
