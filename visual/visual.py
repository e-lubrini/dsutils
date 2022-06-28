import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot(data,
        x=None,
        y=None,
        hue=None,

        key_id=None,
        drop_doubles = True,

        slice_top = False,
        split=False,
        yscale=None,
        cut=0,

        title='',
        xlabel='',
        ylabel='',
        huelabel='',
        palette='pastel',
        
        type='dist',

        bins=25,
        ):

    ## df
    subset = list(filter(None,[x,y,hue,key_id]))
    data = data.dropna(subset=subset)

    if drop_doubles:
        data = data.drop_duplicates(subset=subset)


    if slice_top:
        for k,v in slice_top.items():
            top = pd.value_counts(data[k]).iloc[0:v].index
            data = data[data[k].isin(top)]

    if split:
        for k,v in split.items():
            other_slice = pd.value_counts(data[k]).iloc[v-1:].index
            data.loc[data[k].isin(other_slice), k] = 'other'
    
    if not key_id:
        key_id = key_id=data.columns[0]
    
    ## fig
    if type == 'violin':
        split = len(set(data[hue]))==2
        sns.violinplot(data=data,
                    x=x,
                    y=y,
                    hue=hue,
                    legend=True,
                    split=split,
                    palette=palette,
                    cut=cut,
                    )
    elif type == 'dist':
        sns.displot(data=data,
                    x=x,
                    y=y,
                    hue=hue,      
                    kind='kde',
                    legend=True,
                    palette=palette,
                    cut=cut,
                    )
    elif type == 'hist':
        sns.histplot(data=data,
                    x=x,
                    y=y,
                    hue=hue,
                    bins=bins,      
                    legend=True,
                    palette=palette,
                    )
    elif type == 'cat':
        sns.catplot(data=data,
                    x=x,
                    y=y,
                    palette=palette,
                    )
                    
    if yscale:
        plt.yscale(yscale)

    if not ylabel:
        ylabel = y
    if not xlabel:
        xlabel = x
    if not huelabel:
        huelabel = hue
        
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)

    if not title:
        if hue and x and not y:
            title = 'Distribution of ' + str(huelabel)+ (' per ' + str(xlabel))*bool(xlabel)
        else:
            title = str(xlabel)+ (' vs ' + str(ylabel))*bool(ylabel) + (' grouped by ' + str(huelabel))*bool(huelabel)
    plt.title(title)
    plt.show()
    