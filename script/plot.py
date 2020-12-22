import sys

import numpy
from numpy import loadtxt, log10

import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.use('pdf')
params = {
    "font.size": 12,    
    "axes.titlesize":12,   
    "axes.labelsize": 12, 
    "legend.fontsize": 12, 
    "xtick.labelsize": 12, 
    "ytick.labelsize": 12, 
    "figure.subplot.wspace":0.2, 
    "figure.subplot.hspace":0.4,
    "axes.spines.right":False,
    "axes.spines.top":False, 
    "xtick.direction":'in',
    "ytick.direction":'in'
}
mpl.rcParams.update(params)
props = {'xlabel': 'Batch', 'ylabel': r'log$(e)$'}
    
def get_ele(ls, idx):
    n = len(ls)
    return ls[idx%n]

def get_marker(i, marker_size=1, markevery=1000000):
    linestyle_list = ['solid', 'dashed', 'dashdot', 'dotted']
    marker_list    = ["o", "*", "s", "v", ","]
    color_list     = ["C1", "C2", "C3", "C6", "C8", "C9"]
    return dict(linestyle=get_ele(linestyle_list, i),
                marker=get_ele(marker_list, i),
                color=get_ele(color_list, i),
                markersize=marker_size,markevery=markevery)

def get_plots(path_name):
    energy_test = loadtxt("%s/test/test.e.out"%path_name)
    lcurve      = loadtxt("%s/train/lcurve.out"%path_name)[0::20,:]
    ibatch      = lcurve[:,0]

    style_dict = {
        'l2_tst':   get_marker(1, marker_size=4, markevery=100),
        'l2_trn':   get_marker(2, marker_size=4, markevery=100),
        'l2_e_tst': get_marker(3, marker_size=4, markevery=100),
        'l2_e_trn': get_marker(4, marker_size=4, markevery=100),
        'l2_f_tst': get_marker(5, marker_size=4, markevery=100),
        'l2_f_trn': get_marker(6, marker_size=4, markevery=100),
        # 'lr':       get_marker(7, marker_size=4, markevery=100)
    }

    fig, ax = plt.subplots(figsize=(10,6))
    for i, label_name in enumerate(style_dict):
        ax.plot(ibatch, log10(lcurve[:,i+1]), **style_dict[label_name], label=label_name)

    ax.set(**props)
    ax.grid(linestyle="--", alpha=0.2)

    fig.legend(frameon=False, loc='upper center',ncol=4,handlelength=4)
    fig.savefig("%s/test/loss_func.pdf"%path_name)
    
    fig, axs = plt.subplots(1, 1,figsize=(10,6))
    data1 = energy_test[:,0]-numpy.average(energy_test[:,0])
    data2 = energy_test[:,1]-numpy.average(energy_test[:,0])
    axs.scatter(data1, data2, marker='*', color='r', s=10)
    lo = numpy.min([numpy.min(energy_test[:,0]-numpy.average(energy_test[:,0])), numpy.min(energy_test[:,1]-numpy.average(energy_test[:,0]))])
    hi = numpy.max([numpy.max(energy_test[:,0]-numpy.average(energy_test[:,0])), numpy.max(energy_test[:,1]-numpy.average(energy_test[:,0]))])
    axs.set_xlim(lo, hi)
    axs.set_ylim(lo, hi)
    axs.set_aspect(1.0)

    m,b = numpy.polyfit(data1, data2, 1)
    print("m = %12.6f, b = %12.6f"%(m, b))
    x = numpy.linspace(lo, hi, 100)
    axs.plot(x, m*x+b)
    fig.savefig("%s/test/scatter_plot.pdf"%path_name)
    
def main(path_name):
    print("path_name = ", path_name)
    get_plots(path_name)
    
if __name__ == "__main__":
    main(sys.argv[1])
