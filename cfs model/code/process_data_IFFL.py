import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd

pad = 5
xpad = 15
ypad = 10

mpl.rcParams['lines.linewidth'] = 2
mpl.rcParams['lines.linestyle'] = '-'
mpl.rcParams['figure.figsize'] = 13,12

mpl.rcParams['axes.linewidth'] = 3
mpl.rcParams['axes.labelsize'] = 25
mpl.rcParams['axes.labelweight'] = 'bold'
mpl.rcParams['axes.titlesize'] = 25
mpl.rcParams['axes.titleweight'] = 'bold'

mpl.rcParams['font.family'] = 'Arial'
mpl.rcParams['font.size'] = '16'

color = 'black'
alpha = 0.1
markersize = 60
capsize = 6
elinewidth = 2


def get_kinetics(df, idx, measurement):
    newcols = pd.MultiIndex.from_arrays(np.roll(np.array([s.split(', ') for s in df.columns[1:]]),(1), axis=1).T, names = ('Measurement','Reaction ID','Replicate'))
    df = df.set_index('time')
    df.columns = newcols

    select = df[measurement].columns.get_level_values(0).isin([str(i) for i in idx])
    return df[measurement].loc[:, select]

def get_data(plot=False, exps = None):
    
    file = 'data/200527_IFFLaofa_TIDY.csv'
    CRISPRi_tit = pd.read_csv(file,index_col=0)

    leaks_kinetics = get_kinetics(CRISPRi_tit, exps, 'RFPEx')
    leaks_means = leaks_kinetics.groupby(level=0, axis=1).diff(periods =3,axis=0).groupby(level=0, axis=1).mean()/30
    leaks_stds = leaks_kinetics.groupby(level=0, axis=1).diff(periods =3,axis=0).groupby(level=0, axis=1).std()/30

    # treat data, save csv

    fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(11,12))
    fig.tight_layout(pad=pad)

    nmeans = leaks_means
    nstds = leaks_stds
    #nmeans = leaks_means.div(leaks_means['L'], axis=0)
    #nstds = nmeans*(((leaks_stds/leaks_means).to_numpy())**2 + np.tile((leaks_stds['L']/leaks_means['L']).to_numpy(),(3,1)).T**2)**0.5

    scale = nmeans.max()
    idx = nmeans.idxmax()
    stds = [nstds.loc[j,i] for i,j in zip(list(dict(idx)), list(idx))]

    nstds = nmeans.div(scale)*(((nstds.div(nmeans,axis=0).to_numpy())**2 + np.tile((stds/scale.to_numpy())**2,(len(leaks_means),1)))**0.5)
    nmeans = nmeans.div(scale)
    # nmeans = nmeans.reindex(columns=['19','18'])
    # nstds = nstds.reindex(columns=['19','18'])
    
    ax = ax[0]
    if plot:
        nmeans.plot(use_index = True, legend = False, logy = False, ax = ax, marker = 'o')
        for i in range(len(nmeans.columns)):
            m = nmeans.iloc[:,i].to_numpy()
            s = nstds.iloc[:,i].to_numpy()
            t = nmeans.iloc[:,i].index.values
            ax.fill_between(t, m-s, m+s, alpha = 0.1)

        ax.set_ylim([0,1.2])
        ax.set_xlim([0, 900])
        ax.set_ylabel('Normalized\n RFP Production Rate')
        ax.set_xlabel('time (min)')
        ax.xaxis.set_major_locator(mpl.ticker.MaxNLocator(6))
        ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(5))
        ax.xaxis.labelpad = xpad
        ax.yaxis.labelpad = ypad
        ax.legend(['IFFL 0.1nM sgRNA','IFFL 1nM sgRNA'], loc = 'upper left', frameon = False, prop = dict(size=14))
        
    return ax, nmeans, nstds