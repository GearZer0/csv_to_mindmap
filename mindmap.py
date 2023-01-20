import pandas as pd
import sys
from graphviz import Digraph

COLOR_SCHEME = "piyg6"

FILE_NAME_TYPE = "sample.xls" if len(sys.argv) < 2 else sys.argv[1]
FILE_NAME = FILE_NAME_TYPE.split(".")[0]
FILE_TYPE = FILE_NAME_TYPE.split(".")[-1]

G = Digraph(format='png')
G.graph_attr["bgcolor"] = "#2980b9:#6dd5fa"
G.graph_attr["gradientangle"] = "90"
G.graph_attr["ranksep"]="3"
G.graph_attr["strict"]="False"
G.graph_attr["directed"]="True"
G.graph_attr["label"]=FILE_NAME
G.graph_attr["fontsize"]="150"
G.graph_attr["fontname"]="Bahnschrift SemiBold SemiConden"


# Nodes design attributes
G.node_attr["shape"] = "rectangle"
G.node_attr["colorscheme"] = COLOR_SCHEME
G.node_attr["style"] = "filled"
G.node_attr["fontsize"] = "50"
G.node_attr["fontname"] = "Calibri Bold"


# Edge design attributes
G.edge_attr["colorscheme"] = COLOR_SCHEME
G.edge_attr["penwidth"] = "10"



if(FILE_TYPE == "xls"):
    df = pd.read_excel(FILE_NAME_TYPE)
elif(FILE_TYPE == "csv"):
    df = pd.read_csv(FILE_NAME_TYPE)
else:
    print(FILE_TYPE + " is not acceptable file extension - only csv and xls")

# Remove duplicates
df = df.drop_duplicates()

# Get the unique values of the first column and set their numbers 0 to ...
first_column_values = df.iloc[:, 0].drop_duplicates().reset_index(drop=True)

# Replace null values to None
df = df.where(pd.notnull(df), None)

pairs = []

for index, row in df.iterrows():
    filtered_columns = [column for column in row.values if column is not None]

    # The color is decided by the first column
    color_index = str(first_column_values[first_column_values == filtered_columns[0]].index[0] + 1)

    for column in range(len(filtered_columns)-1):
        tup = (filtered_columns[column],filtered_columns[column+1])
        if tup not in pairs:
            pairs.append(tup)
            G.edge(filtered_columns[column],filtered_columns[column+1], color=color_index)
            G.node(filtered_columns[column],fillcolor=color_index)

    G.node(filtered_columns[-1], fillcolor=color_index)

G = G.unflatten(stagger=5)  
G.render(FILE_NAME, view=True)
