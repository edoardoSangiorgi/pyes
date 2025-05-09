import matplotlib.pyplot as plt
import matplotlib as mpl

class PlotManager:

    def __init__(self, use_tex=True, figsize=(8, 4.5)):

        mpl.rcParams.update({
            'text.usetex': use_tex,
            'font.family': 'serif',
            'font.size': 12,
            'axes.titlesize': 14,
            'axes.labelsize': 12,
            'figure.figsize': figsize
        })
    


    def plot_graphic(self, x_data, y_data, label=None, x_label=None, y_label=None):

        
        fig, ax = plt.subplots()
        ax.plot(x_data, y_data, label=label)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        
        if label:
            ax.legend()
       




if __name__ == '__main__':

    import numpy as np
    pm = PlotManager()
    x = np.linspace(0, 2*np.pi, 100)
    pm.plot_graphic(x, np.sin(x), "Sine Wave", "X", "Y")
    pm.plot_graphic(x, np.cos(x), "Cosine Wave", "X", "Y")

    plt.show()