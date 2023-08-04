import os
import fnmatch
import typer
import yaml
import networkx as nx
import matplotlib.pyplot as plt
from py2neo import Graph, Node, Relationship
import uuid

app = typer.Typer()

def read_config(path_to_yaml):
    with open(path_to_yaml, 'r') as file:
        yaml_data = yaml.safe_load(file)

    neo4j_uri = yaml_data.get('neo4j_uri', 'bolt://localhost:7687')
    neo4j_username = yaml_data.get('neo4j_username', 'neo4j')
    neo4j_password = yaml_data.get('neo4j_password', 'neo4jpasswd')

    return neo4j_uri, neo4j_username, neo4j_password

def load_data_source(data_source_path: str):
    typer.echo(f"Loading data sources from path: {data_source_path}")
    yaml_files = []
    for root, _, files in os.walk(data_source_path):
        for file in files:
            if fnmatch.fnmatch(file, '*.yaml') or fnmatch.fnmatch(file, '*.yml') or fnmatch.fnmatch(file, '*.YAML'):
                yaml_files.append(os.path.join(root, file))
    typer.echo(f"Loaded {len(yaml_files)} sources from path: {data_source_path}")
    return yaml_files


def showfields(data_source: list):
    # Function to show available fields from the data sources
    typer.echo("Showing available fields from the data sources")
    fields= []
    for file_path in data_source:
        with open(file_path, "r") as file:
            try:
                yaml_data = yaml.safe_load(file)
                input = yaml_data.get("input", {})
                if isinstance(input, dict):
                    if 'and' in input:
                        for and_field in input["and"]:
                            fields.append(*and_field.keys())
                    if 'or' in input:
                        for or_field in input["or"]:
                            fields.append(*or_field.keys())
            except Exception as error:
                print(f"Error {error} on {file_path}")
    typer.echo("Fields Available:")
    for field in set(fields):
        print(f"*  {field}")
    return set(fields)


def parse_yaml_graph(data_source:list) -> nx.Graph:
    parsed_graph = nx.DiGraph()
    for file_path in data_source:
        with open(file_path, "r") as file:
            try:
                source_nodes= []
                dest_nodes = []
                yaml_data = yaml.safe_load(file)
                input = yaml_data.get("input", {})
                if isinstance(input, dict):
                    # AND case
                    if 'and' in input:
                        and_block = input["and"]
                        for and_requirement in and_block:
                            Caption = and_requirement.keys()
                            source_nodes.append(*Caption)
                            parsed_graph.add_node(*Caption, id=str(uuid.uuid4()), Caption=str(*Caption), Color="blue", bool_type="and")
                    # OR case
                    if 'or' in input:
                        or_block = input["or"]
                        for or_requirement in or_block:
                            Caption = or_requirement.keys()
                            source_nodes.append(*or_requirement.keys())
                            parsed_graph.add_node(*or_requirement.keys(), id=str(uuid.uuid4()), Caption=str(*Caption), Color="blue", bool_type="or")
                # Extract returns
                returns = yaml_data.get("returns", {})
                for return_key, _ in returns.items():
                    parsed_graph.add_node(return_key, id=str(uuid.uuid4()), Caption=str(return_key), Color="green")
                    dest_nodes.append(return_key)
                # Edges:
                val = 1
                for source in source_nodes:
                    for dest in dest_nodes:
                        edge = (source, dest)
                        parsed_graph.add_edge(*edge, Caption=yaml_data.get("name", {}), bool_type=parsed_graph.nodes[source]['bool_type'])
                        val = val+1
            except yaml.YAMLError as error:
                print(f"Error processing YAML file: {file_path} {error}")
    return parsed_graph


def create_graph(graph:nx.Graph, filename: str):
    # Function to create a graph and save it as an image
    typer.echo(f"Creating a graph and saving it as: {filename} ")
    pos = nx.spring_layout(graph, seed = 50)
    node_colors = [node[1]["Color"] for node in graph.nodes(data=True)]
    nx.draw(graph, pos, ax = None, with_labels = True,font_size = 10, node_size = 200, node_color = node_colors)
    plt.savefig(filename)

def traverse_graph(graph, roots):
    reachable_nodes = []
    for item in roots:
        #reachable_nodes.append(item)
        for childs in nx.bfs_predecessors(graph,item):
            for child in list(childs):
                if child not in reachable_nodes:
                    temp_list = []
                    for edge in graph.in_edges(child, data=True):
                        if edge[2]['bool_type'] == "or":
                            reachable_nodes.append(child)
                        if edge[2]['bool_type'] == "and":
                            temp_list.append(edge[0])
                    if len(temp_list) > 0:
                        if set(temp_list).issubset(set(reachable_nodes)):
                            reachable_nodes.append(child)
    print(f"Lista agora : {reachable_nodes}")
    return reachable_nodes        


def write_to_neo4j(graph, uri, username, password):
    # Connect to the Neo4j database
    graph_db = Graph(uri, auth=(username, password))

    # Dictionary to store Neo4j node objects based on their ID
    neo4j_nodes = {}

    # Create nodes and relationships from the graph
    for node in graph.nodes():
        node_data = graph.nodes[node]
        node_properties = {key: value for key, value in node_data.items()}
        node_label = node_data['Caption']
        node_id = node_data['id']

        # Check if the node with the same ID already exists in Neo4j
        if node_data['id'] in neo4j_nodes:
            neo4j_node = neo4j_nodes[node_data['id']]
        else:
            neo4j_node = Node(node_id, **node_properties)
            neo4j_node.__primarylabel__ = node_label  # Set the primary label
            neo4j_node.__primarykey__ = "id"  # Set the primary key
            neo4j_nodes[node_id] = neo4j_node
        graph_db.merge(neo4j_node, "id", "Caption")

    for edge in graph.edges():
        from_node, to_node = edge
        relationship_data = graph.edges[from_node, to_node]
        relationship_properties = {key: value for key, value in relationship_data.items()}

        for key, value in relationship_properties.items():
            if isinstance(value, str) and value.isnumeric():
                relationship_properties[key] = int(value)
            elif isinstance(value, str) and '.' in value and all(part.isnumeric() for part in value.split('.')):
                relationship_properties[key] = float(value)

        from_node_id = graph.nodes[from_node]['id']
        to_node_id = graph.nodes[to_node]['id']
        
        rel = Relationship(neo4j_nodes[from_node_id], "PROVIDES", neo4j_nodes[to_node_id], **relationship_properties)
        graph_db.create(rel)

@app.command()
def main(
    data_source: str = typer.Option(None, "--data-source", "-ds", help="Load all sources from the path"),
    show_fields: bool = typer.Option(False, "--show-fields", "-sf", help="Show the available fields"),
    graph: str = typer.Option(None, "--graph", help="Save an image with the filename"),
    what_i_know: str = typer.Option(None, help="Create a list of output that I can get from what I know"),
    neo4j: str = typer.Option(None, help="Load your data to neo4j"),
):
    datasources = None
    global_graph = None
    if data_source:
        datasources = load_data_source(data_source)

    if show_fields:
        showfields(datasources)

    if graph:
        global_graph = parse_yaml_graph(datasources)
        create_graph(global_graph, graph)
       

    if what_i_know:
        if not global_graph:
            global_graph = parse_yaml_graph(datasources)
        traverse_graph(global_graph,["CPF"])

    if neo4j:
        if not global_graph:
            global_graph = parse_yaml_graph(datasources)
        neo4j_uri, neo4j_username, neo4j_password = read_config(neo4j)
        # Write the graph to the Neo4j database
        write_to_neo4j(global_graph, neo4j_uri, neo4j_username, neo4j_password)


if __name__ == "__main__":
    app()
