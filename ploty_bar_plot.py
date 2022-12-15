import plotly.plotly as py
import plotly.graph_objs as go

# these two lines are what allow your code to shou up in a notebook
from plotly.offline import init_notebook_mode, iplot
init_notebook_mode()

counts = df[column].value_counts()
data = [go.Bar(
            x=counts.index,
            y=counts.values
    )]
py.iplot(data, filename='basic-bar')

## STACKED EXAMPLE
pos_responses = df[df['Response'] == 'Positive']['Column'].value_counts()
neg_responses = df[df['Response'] == 'Negative']['Column'].value_counts()

trace1 = go.Bar(
    x=pos_responses.index,
    y=pos_responses.values,
    name='Positive'
)
trace2 = go.Bar(
    x=neg_responses.index,
    y=neg_responses.values,
    name='Negative'
)

data = [trace1, trace2]
layout = go.Layout(
    barmode='stack'
)

fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='stacked-bar')