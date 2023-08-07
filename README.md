# BROS
Brazilian OSINT Sources

This is a basic specification of Brazilian Open Source Information Sources, pre-compiled with requirements and what kind of information it can provide.
The main objective of this repo is to answer the question: If I have a CPF what kind of information i can discover? or if I have a CPF and BIRTHDATE what else can I get ?

# How to test:
1. pip install virtualenv
2. virtualenv venv
3. source venv/bin/activate
4. pip install -r requirements.txt
5. python3 kkk.py --help

# With docker
1. docker build -t neo4j .
2. docker run -d -p 7474:7474 -p 7473:7473 -p 7687:7687 --name neo4j_container neo4j

# Some examples:
* python3 kkk.py --data-source ./tests/fake_sources --show-fields show all fields that you can get from fake_sources
* python3 kkk.py --data-source ./tests/fake_sources --graph image.png = write an image with the graph
* python3 kkk.py --data-source ./tests/fake_sources --neo4j ./config.yaml = write the graph into neo4j for posterior analysis.

You can change the ./tests/fake_sources to ./sources/Brazil

## How to contribute

If you find a new source write in Yaml you can write a Pull Request with the following:
    * name: the name of the source
    * description: What you can derive from the returns.
    * kind:
        * URL: the URL you should go to get information
        * whatsapp: the WhatsApp number
        * SMS: the SMS number
    * captcha: if there is a captcha
    * inputs: A list of fields that are necessary to grab the information (See data definitions)
    * returns: A list of information that can be obtained and it's XPATH for the crawler get it automatically

If you know how to code and want to improve the code, be my guest and write a PR tackling one of the millions of issues that we have.

## Some conventions to write your data source:

* All the YAMLs files have the same basic structure with the minimum: 
    * name - Name of the data source.
    * description - A description of the data source and what kind of information can be derived from this.
    * input - list of input fields you have to provide to get some information, those inputs can be AND(If you need more than one of them) or OR.
    * returns - list of returns you get from that source.

* All the inputs are CAPSLOCK and SNAKE_CASE
* All the returns are CAPSLOCK and SNAKE_CASE, if the returns are not the complete data, it must have PARTIAL_ in front of the data.
* The PARTIAL_ field has a subfield called masked_number which will be TRUE if the number of * in the mask corresponds to the actual number of omitted characters.


## ROADMAP

* [X] Add graph visualization to understand which info you can obtain with a piece of information
* [ ] Add more sources.
* [ ] Better data definitions to include Regex validations.
* [ ] Add subfilter by contexts(Eg: a CPF from SP will only look for sources that have SP in context.)
* [ ] Add Some browsing automation to get the data and bypass captchas with death by captcha.