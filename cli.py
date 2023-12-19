import typer
from bros import *


app = typer.Typer()
banner = """
  ___ ___  ___  ___ 
 | _ ) _ \/ _ \/ __|
 | _ \   / (_) \__ \\
 |___/_|_\\___/|___/
 """
@app.command()
def main(
    data_source: str = typer.Option(None, "--data-source", "-ds", help="Load all sources from the path"),
    show_fields: bool = typer.Option(False, "--show-fields", "-sf", help="Show the available fields"),
    graph: str = typer.Option(None, "--graph", help="Save an image with the filename"),
    what_i_know: str = typer.Option(None, help="Create a list of output that I can get from what I know"),
    neo4j: str = typer.Option(None, help="Load your data to neo4j"),
):
    """
    BROS - Brazilian Open Sources.
    """
    typer.echo(banner)
    datasources = None
    global_graph = None
    if data_source:
        datasources = Bros.load_data_source(data_source_path=data_source)

    if show_fields:
        Bros.showfields(data_source=datasources)

    if graph:
        global_graph = Bros.parse_yaml_graph(datasources)
        Bros.create_graph(global_graph, graph)
       

    if what_i_know:
        if not global_graph:
            global_graph = Bros.parse_yaml_graph(datasources)
        params = []
        for n in what_i_know.split(','):
            params.append(n)
        if params not in available_fields:
            typer.BadParameter("Fields are not in graph")
        traverse_graph(global_graph,params)

    if neo4j is None:
        print("No config file")
        raise typer.Abort()
    if neo4j.is_file():
        if not global_graph:
            global_graph = Bros.parse_yaml_graph(datasources)
        neo4j_uri, neo4j_username, neo4j_password = read_config(neo4j)
        # Write the graph to the Neo4j database
        Bros.write_to_neo4j(global_graph, neo4j_uri, neo4j_username, neo4j_password)


if __name__ == "__main__":
    app()