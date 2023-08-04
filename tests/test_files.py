import os
import pytest
from kkk import load_data_source, showfields, create_graph, parse_yaml_graph, traverse_graph


def test_load_data_source():
    # Create a temporary directory for testing
    temp_dir = "temp_test_dir"
    os.makedirs(temp_dir, exist_ok=True)

    # Create some files with YAML and non-YAML formats in the temporary directory
    yaml_files = ['file1.yaml', 'file2.yml', 'file3.YAML']
    other_files = ['file4.txt', 'file5.csv', 'file6.json']
    for file in yaml_files + other_files:
        open(os.path.join(temp_dir, file), 'a').close()

    # Call the function and check if it returns the correct YAML files
    expected_yaml_files = [os.path.join(temp_dir, file) for file in yaml_files]
    assert load_data_source(temp_dir).sort() == expected_yaml_files.sort()

    # Clean up: remove temporary directory and its contents
    for file in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, file))
    os.rmdir(temp_dir)


@pytest.fixture
def read_data():
    return load_data_source('./tests/fake_sources')

@pytest.fixture
def get_graph(read_data):
    return parse_yaml_graph(read_data)

def test_show_fields(read_data):
    expected_fields = ["BIRTHDATE","MOTHER_NAME","NAME","EMAIL","CELLPHONE","FATHER_NAME","CPF","ADDRESS"]
    result = showfields(read_data)
    assert result == set(expected_fields)

def test_parse_yaml_graph(read_data):
    graph = parse_yaml_graph(read_data)
    assert graph.number_of_nodes() == 11 and graph.size() == 16

def test_search_graph_one_item(get_graph):
    expected_result = ['MOTHER_NAME', 'BIRTHDATE', 'NAME', 'CPF', 'PARTIAL_EMAIL', 'FATHER_NAME', 'STREET']
    result = traverse_graph(get_graph, ["CPF"])
    assert result == expected_result

def test_search_graph_two_itens(get_graph):
    expected_result = ['MOTHER_NAME', 'BIRTHDATE', 'NAME', 'CPF', 'PARTIAL_EMAIL', 'FATHER_NAME', 'STREET']
    result = traverse_graph(get_graph, ["CPF","ADDRESS"])
    assert result == expected_result

def test_search_graph_one_item_no_return(get_graph):
    expected_result = []
    result = traverse_graph(get_graph, ["ADDRESS"])
    assert result == expected_result