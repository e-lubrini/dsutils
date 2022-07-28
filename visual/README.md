# Visualisations

## Seaborn Wrapper
### Usage

minimal working example: 
```python
plot(x=x : str,
    y=y : str,
    data=data : DataFrame,
    type=type : str)
```

### Examples
#### Violin
```python
x = 'dateIdentified'
y = 'availability'
hue = 'language'
palette = sns.color_palette('tab10',n_colors=2)

plot(x=x, y=y, hue=hue, data=df,
    type='violin',
    split={hue:2},
    drop_doubles=[key_id], drop_na=[x],
    xlabel='date', ylabel='accessibility', huelabel='language',
    sort_alpha=[hue],
    swarm=True,
    save_dir = save_dir,
    )
```

<p align="center">
  <img src="https://github.com/e-lubrini/utils/blob/main/visual/img/violin.png" width="750" />
</p>

#### Scatterplot
```python
x = 'dateIdentified'
y = 'database'
hue = 'language'
style='availability'

plot(x=x, y=y, hue=hue, style=style, data=df,
    type='scatter',
    split={hue:4,style:3,y:7},
    legend_position='out',
    drop_doubles=[key_id],
    xlabel='date', ylabel='database',
    sort_alpha=[hue],
    save_dir = save_dir,
    )
    
```

<p align="center">
  <img src="https://github.com/e-lubrini/utils/blob/main/visual/img/scatter.png" width="750" />
</p>

#### Distribution
```python
x = 'dateIdentified'
hue = 'database'

plot(x=x, hue=hue, data=df,
    type='dist',
    split={hue:5},
    legend_position=None, drop_na=[hue],
    drop_doubles=[key_id],
    xlabel='date', ylabel='', huelabel='database',
    save_dir = save_dir,
    )
```


<p align="center">
  <img src="https://github.com/e-lubrini/utils/blob/main/visual/img/dist.png" width="750" />
</p>

#### Composiiton
```python
hue = 'language'

plot(hue=hue, data=df,
    type='perc',
    drop_doubles=[key_id], drop_na=[hue],
    legend_position='out',
    save_dir = save_dir,
    )
```


<p align="center">
  <img src="https://github.com/e-lubrini/utils/blob/main/visual/img/perc.png" width="750" />
</p>
