# BROS
Brazilian OSINT Sources

This is a basic specification of Brazilian Open Source Information Sources, pre-compiled with requirements and what kind of information it can provides.

## How to contribute

If you find a new source write in Yaml:
* name: the name of the source
* url: the url you should go to get information
* captcha: if there is a captcha
* inputs: A list of fields that are necessary to grab the information (See data definitions)
* results: A list of information that can be obtained and it's XPATH for the crawler get it automatically

## TODO

* Add captcha automation with deathbycaptcha
* Add graph visualization to understand wich info you can obtain with a piece of information
* Better data definitions to include Regex validations.