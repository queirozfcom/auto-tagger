import numpy as np


def plot_micro_f1_at_k(validation_points, ax, train_points=None):
    if train_points is not None:
        assert (len(validation_points) == len(train_points))

    ks = range(1, len(validation_points)+1)



    ax.plot(ks, validation_points, 'bo-', label='Validation set')

    if train_points is not None:
        ax.plot(ks, train_points, 'ro-', label='Train set')

    ax.set_xlim(0, 11)
    ax.set_ylim(0, 0.5)
    ax.set_xlabel('k', fontsize=13)
    ax.set_ylabel('Micro-averaged F1-score at k', fontsize=13)

    ax.set_xticks(np.arange(0, 11, 1))
    ax.set_yticks(np.arange(0, 1.05, 0.1))
    ax.grid(True)

    gridlines = ax.get_xgridlines() + ax.get_ygridlines()
    for line in gridlines:
        line.set_linestyle(':')
        line.set_linewidth(0.7)

    ax.legend()

    return ax
