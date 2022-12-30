from graphviz import Digraph
import pandas as pd
import random

# Output file extension/format
G = Digraph(format='png')

# Create a dictionary to store the color and fill color for each value in the first column
color_map = {}

df = pd.read_excel('data4.xlsx')
df = df.drop_duplicates()
df = df.where(pd.notnull(df), None)

pairs = []

for index, row in df.iterrows():
    filtered_columns = [column for column in row.values if column is not None]
    for column in range(len(filtered_columns)-1):
        tup = (filtered_columns[column],filtered_columns[column+1])
        if tup not in pairs:
            pairs.append(tup)

# Set the colour for the edges to blue
G.attr('edge', color='blue')

for index, row in df.iterrows():
    # Get the value in the first column
    first_column_value = row[0]
    
    # If the value is not in the color map, generate a random color and fill color for it
    if first_column_value not in color_map:
        r = lambda: random.randint(0,255)
        color_map[first_column_value] = ('#%02X%02X%02X' % (r(),r(),r()), '#%02X%02X%02X' % (r(),r(),r()))
    
    # Set the color and fill color for the node based on the value in the first column
    G.node(str(row[0]), color=color_map[first_column_value][0], fillcolor=color_map[first_column_value][1], style='filled')

G.edges(pairs)

G.render('sg', view=True)
