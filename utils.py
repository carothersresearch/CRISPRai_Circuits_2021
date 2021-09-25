# MATPLOTLIB Settings 
# https://matplotlib.org/3.2.1/tutorials/introductory/customizing.html#customizing-with-matplotlibrc-files

import matplotlib as mpl
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
import openpyxl
from scipy.stats import ttest_ind, ttest_ind_from_stats

N = 5 # NUMBER OF FIGURES
P = 5 # NUMBER OF MAX PANNELS PER FIGURE
pad = 5
xpad = 15
ypad = 10

mpl.rcParams['lines.linewidth'] = 2
mpl.rcParams['lines.linestyle'] = '-'
mpl.rcParams['figure.figsize'] = 13,12

mpl.rcParams['axes.linewidth'] = 3
#mpl.rcParams['axes.labelsize'] = 25
mpl.rcParams['axes.labelweight'] = 'bold'
mpl.rcParams['axes.titlesize'] = 25
mpl.rcParams['axes.titleweight'] = 'bold'

mpl.rcParams['font.family'] = 'Arial'
mpl.rcParams['font.size'] = '16'

color = 'black'
alpha = 0.2
markersize = 60
capsize = 8
elinewidth = 4
lw = 4
barwidth = 0.5

def get_values(df, t, background = False, normalize = None, stats = False, scale = False):
    df = df.loc[t]
    tidy  = pd.DataFrame(np.unique([s.split(', ')[:2] for s in df.index[1:]],axis=0), columns = ['Reaction ID','Replicate'])
    cols = list(np.unique([s.split(', ')[2] for s in df.index[1:]]))
    vals = [[df['{}, {}, {}'.format(tidy['Reaction ID'].loc[j],tidy['Replicate'].loc[j],i)] for i in cols] for j in tidy.index]
    new = pd.concat([tidy, pd.DataFrame(vals, columns = cols)], axis=1)

    if background:
        newc = []
        bm = {}; bs = {}
        for c in cols:
            l='({}-{})'.format(c,background)
            bm[l] = new.loc[new['Reaction ID'] == background,c].mean()
            bs[l] = new.loc[new['Reaction ID'] == background,c].std()
            new[l] = new[c]-bm[l]
            newc.append(l)
        cols.extend(newc)
        
    if normalize:
        newc = []
        for c in cols:
            if normalize.isnumeric():
                print('use scale')
            else:
                new[c+'/'+normalize] = new[c]/new[normalize]
            newc.append(c+'/'+normalize)
        cols.extend(newc)
        
    if scale:
        newc = []
        sm = {}; ss = {}
        for c in cols:
            l='({}/{})'.format(c,scale)
            sm[l] = new.loc[new['Reaction ID'] == scale,c].mean()
            ss[l] = new.loc[new['Reaction ID'] == scale,c].std()
            new[l] = new[c]/sm[l]
            newc.append(l)
        cols.extend(newc)
    
    if stats:
        for c in cols:
            new[c+' mean'] = new.groupby('Reaction ID')[c].transform('mean')
            if background:
                if background in c:
                    new[c+' std'] = (new.groupby('Reaction ID')[c].transform('std')**2+bs[c]**2)**0.5
                else: new[c+' std'] = new.groupby('Reaction ID')[c].transform('std')
            elif scale:
                if scale in c:
                    new[c+' std'] = new[c+' mean']*((new.groupby('Reaction ID')[c].transform('std')/new[c+' mean'])**2+(ss[c]/sm[c])**2)**0.5
                else: new[c+' std'] = new.groupby('Reaction ID')[c].transform('std')                                                          
            else: new[c+' std'] = new.groupby('Reaction ID')[c].transform('std')
                
    return new

def trans_filter(df,t,idx, background = False, normalize = None, stats = False, sort = True, scale = False):
    data = get_values(df,t, background, normalize, stats, scale)
    new = pd.DataFrame(columns = data.columns)
    for i in idx:
        new = pd.concat([new,data[data['Reaction ID'] == str(i)]])
    #new['Reaction ID'] = new['Reaction ID'].astype(float)
    if sort: new = new.sort_values('Reaction ID')
    new['Reaction ID'] = new['Reaction ID'].astype(str)
    #if background: new = new.append(data[data['Reaction ID'] == background],ignore_index=True)
    return new.reset_index(drop=True)

def get_kinetics(df, idx, measurement):
    newcols = pd.MultiIndex.from_arrays(np.roll(np.array([s.split(', ') for s in df.columns[1:]]),(1), axis=1).T, names = ('Measurement','Reaction ID','Replicate'))
    df = df.set_index('time')
    df.columns = newcols

    select = df[measurement].columns.get_level_values(0).isin([str(i) for i in idx])
    return df[measurement].loc[:, select]
    
def add_concentrations(df, c, label, axis = 0):
    if axis == 0:
        df[label] = np.nan
        for r, n in zip(df['Reaction ID'].unique(),c):
            idx = df['Reaction ID'] == r
            df.loc[idx,label] = [n]*np.sum(idx)
            
    if axis == 1:
        change = {i:k for i,k in zip(list(df.columns.get_level_values(0).unique()),c)}
        newcols = np.concatenate((np.array([*df.columns]),np.array([change[i] for i in list(df.columns.get_level_values(0))],ndmin=2).T),axis=1)
        df.columns = pd.MultiIndex.from_arrays(newcols.T, names=(tuple(df.columns.names)+(label,)))
        
def scatter_plot(ax, df, x, y, yerr, ylabel, xlabel = None):
    ax.errorbar(df[x], df[y], yerr = df[yerr], alpha = alpha, capsize = capsize, fmt = 'none', ecolor = color, elinewidth = elinewidth )
    df.plot(x = x, y = y, kind = 'scatter', s=markersize, ax = ax, logx = True, logy = False, color = color)
    
    ax.set_ylabel(ylabel)
    ax.xaxis.set_major_locator(mpl.ticker.LogLocator(base=10, numticks=6))
    ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(5))
    ax.xaxis.labelpad = xpad
    ax.yaxis.labelpad = ypad
    if xlabel: ax.set_xlabel(xlabel)
        
def bar_plot(ax, df, x, xonly, y, yerr, ylabel, position = 0.5, width = barwidth, color = color, yerrshift = 0):
    df = df.drop_duplicates(x)
    df = df.set_index('Reaction ID').drop([r for r in df['Reaction ID'] if r not in xonly]).reindex(index=xonly).reset_index()
    df.plot.bar(x = x, y = y, ax = ax, color = color,legend=False, position = position, width = width)
    ax.errorbar(np.arange(len(df))+yerrshift, df[y], yerr = df[yerr], alpha = alpha, capsize = capsize, fmt = 'none', ecolor = color, elinewidth = elinewidth )
        
    ax.set_ylabel(ylabel)
    ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(5))
    ax.xaxis.labelpad = xpad
    ax.yaxis.labelpad = ypad
    
def plot_fits(ax, x, y, yerr, xlabel, ylabel, title = None, xerr = None, x_ticks = [0,20,40,60], legend_size = 22):
    ax.errorbar(x, y, yerr, xerr, fmt='ko')
    
    sol1 = np.polyfit(np.log(x), y, 1, full=True)
    xnew = np.linspace(x.iloc[0],x.iloc[-1])
    fit_log =  np.polyval(sol1[0], np.log(xnew))
    r2_log = [1-sol1[1]/((y - y.mean())**2).sum()][0][0]

    sol2 = np.polyfit(x, y, 1, full=True)
    fit_linear =  np.polyval(sol2[0], xnew)
    r2_linear = [1-sol2[1]/((y - y.mean())**2).sum()][0][0]
    
    print(aicc(6,2,sol2[1]))
    print(aicc(6,2,sol1[1]))
    print('next')
    
    RL = np.exp((aicc(6,2,sol2[1])-aicc(6,2,sol1[1]))/2)[0]
    if r2_log > r2_linear:
        ax.plot(xnew,fit_log, 'r', alpha = 0.75, label = 'log $R^2 =$ {r:.{d}f}'.format(r = r2_log, d =3))
        ax.plot(xnew,fit_linear, 'k', alpha = 0.25, label = 'linear $R^2 =$ {r:.{d}f}'.format(r = r2_linear,d = 3))
    else:
        ax.plot(xnew,fit_log, 'k', alpha = 0.25, label = 'log $R^2 =$ {r:.{d}f}'.format(r=r2_log, d= 3))
        ax.plot(xnew,fit_linear, 'r', alpha = 0.75, label = 'linear $R^2 =$ {r:.{d}f}'.format(r=r2_linear,d=3))
        
    ax.plot(xnew,fit_log, 'k', alpha = 0.5, label = '$RL =$ {r:.{d}f}'.format(r=RL, d= 3))
    
    l = ax.legend(frameon = False, handlelength=0, loc='lower right', prop={'size': legend_size},borderaxespad=0)
    l._legend_box.align = "right"
    
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_ylim([min(y)*0.9,max(y)*1.1])
    ax.xaxis.set_major_locator(mpl.ticker.FixedLocator(x_ticks))
    ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(4))
    

    
    if title: ax.set_title(title)
    return r2_log/r2_linear, np.exp((aicc(6,2,sol2[1])-aicc(6,2,sol1[1]))/2)

def aicc(n,k,r):
    return n*np.log(r/n)+2*k+(2*k*(k+1))/(n-k-1)
    
def add_comment(filename, sheet, cell, comment):
    wb2 = openpyxl.load_workbook(filename)
    wb2[sheet][cell] = comment
    wb2.save(filename)