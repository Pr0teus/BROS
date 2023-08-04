# BROS
Brazilian OSINT Sources

This is a basic specification of Brazilian Open Source Information Sources, pre-compiled with requirements and what kind of information it can provide.

## How to contribute

If you find a new source write in Yaml you can write a Pull Request with the following:
    * name: the name of the source
    * description: What you can derive from the returns.
    * kind:
        * URL: the URL you should go to get information
        * whastapp: the WhatsApp number
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

[X] Add graph visualization to understand which info you can obtain with a piece of information
[ ] Add more sources.
[ ] Better data definitions to include Regex validations.
[ ] Add subfilter by contexts(Eg: a CPF from SP will only look for sources that have SP in context.)
[ ] Add Some browsing automation to get the data and bypass captchas with death by captcha.