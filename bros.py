import click
import yaml
from splinter import Browser
from bs4 import BeautifulSoup
from lxml import etree



@click.command()
@click.argument('path')
def crawl(path):
    with open(path) as f:
        bot = yaml.safe_load(f.read())
    inputs = {}
    print(bot['inputs'])
    for value in bot['inputs']:
        inputs[value] = input(f'Informe o {value}')
    print(inputs)
    with Browser() as browser:
        browser.visit(bot['url'])
        for value in bot['inputs']:
            print(bot['inputs'][value])
            if bot['inputs'][value]['type'] == 'input':
                browser.fill(bot['inputs'][value]['field'], inputs[value])
            elif bot['inputs'][value]['type'] == 'select':
                browser.select(bot['inputs'][value]['field'], inputs[value])
            else:
                print('desconheco tipo field')
        import time
        time.sleep(50)
        soup = BeautifulSoup(browser.html, 'html.parser')
        for result in bot['results']:
            dom = etree.HTML(str(soup))
            if bot['results'][result]['type'] == 'table':
                value = dom.xpath(bot['results'][result]['XPATH'])
                for i in value:
                    for j in i.iter():
                        print(j.text)
            elif bot['results'][result]['type'] == 'text':
                value = dom.xpath(bot['results'][result]['XPATH'])
                print(f'{result}: {value}')
            else:
                value = dom.xpath(bot['results'][result]['XPATH'])[0].text
                print(f'{result}: {value}')


        


if __name__ == '__main__':
    crawl()
