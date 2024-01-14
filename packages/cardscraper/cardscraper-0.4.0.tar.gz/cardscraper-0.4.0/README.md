# cardscraper

A tool for generating Anki packages by webscraping.

## Installation

install from [PyPI](https://pypi.org/project/cardscraper/)

```
pip install cardscraper
```

## Basic usage

`cardscraper ...` or `python -m cardscraper ...`

cardscraper has 3 main subcommands:

- `cardscraper gen` - takes in [input files](#input-file-format) and generates Anki packages
- `cardscraper init` - generates skeleton [input files](#input-file-format)
- `cardscraper list` - lists all available functions for each step (cardscraper has a [plugin system](#plugin-system))

and you can always use `cardscraper <subcommand> -h`

I recommend doing something like:

1. `cardscraper init hello.yaml`
2. edit the file to suit your needs
3. `cardscraper gen hello.yaml`

## Input file format

cardscraper takes in YAML files as input

```yaml
# here you can specify which function to use for each step
# (every one defaults to 'default')
meta:
  # controls package details and package dumping
  package: default
  # controls deck creation
  deck: default
  # controls model creation
  model: default
  # controls scraping and note creation
  scraping: default

# anki package info
package:
  # package name
  name: package_name
  # output folder (defaults to '.')
  output: ./out/
  # media folder (defaults to null)
  # the directory will be walked recursively
  # every pattern matched file will be added to the package as media
  media: ./media/
  # pattern to match files against for media (defaults to **/*.*)
  pattern: "**/*.png"

# anki deck info
deck:
  # deck name
  name: Deck
  # deck id
  # don't forget to make this value unique
  id: 987

# anki model info
model:
  # model name
  name: Model
  # model id
  # don't forget to make this value unique
  id: 321
  # card styling (defaults to '')
  css: |
    .question, .answer {
        text-align: center;
    }
    .question {
        font-size: 5rem;
        font-weight: 700;
    }
    .answer {
        font-size: 3rem;
    }
  # list of cards
  templates:
    # card name
    - name: Front
      # front side
      qfmt: |
        <div class='question'>
        {{Question}}
        </div>
      # back side
      afmt: |
        {{FrontSide}}
        <hr id='answer'>
        <div class='answer'>
        {{Answer}}
        </div>
    # same here
    - name: Back
      qfmt: |
        <div class='question'>
        {{Answer}}
        </div>
      afmt: |
        {{FrontSide}}
        <hr id='answer'>
        <div class='answer'>
        {{Question}}
        </div>

# scraping info
scraping:
  # list of urls to scrape
  urls:
    - https://www.scrapethissite.com/pages/simple/
  # you can set your own custom user agent (defaults to the one here)
  agent: Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0
  # list of queries
  # each query selects an html element and lets you use its text in the templates
  # each child query runs inside the parent one
  queries:
    # query name which you can use in the templates like {{Country}}
    - name: Country
      # css selector
      query: .country
      # you can select something specific from the query by providing a regex
      # this is a python regex with re.DOTALL enabled i.e. '.' captures '\n'
      # uses the first captured group
      # (defaults to null)
      regex: null
      # if true: we select every instance and iterate over them
      # if false: we only select the first one
      # basically it's querySelector() vs querySelectorAll()
      # (defaults to false)
      many: true
      children:
        - name: Question
          query: .country-info
          many: false
          regex: (Area .*)$
          children: null
        - name: Answer
          query: .country-name
          many: false
          regex: null
          children: null
```

## Using in code

```py
import yaml
from cardscraper import (
    Config,
    generate_anki_package,
    select_function_by_step_and_name,
    write_package,
)
from genanki import Model, Note

if __name__ == '__main__':
    with open('/path/to/config.yaml', 'r') as f:
        config: Config = yaml.load(f, yaml.Loader)
    # or you can make a config manually

    get_model = select_function_by_step_and_name('model', 'default')
    get_deck = select_function_by_step_and_name('deck', 'default')
    get_package = select_function_by_step_and_name('package', 'default')

    def get_notes(config: Config, model: Model) -> list[Note]:
        notes = []
        ...
        return notes

    package, path = generate_anki_package(
        config, get_model, get_notes, get_deck, get_package
    )
    write_package(package, path)
```

## Plugin system

you can add custom functions by exposing `cardscraper.step` entry point in your package

```toml
[project.entry-points.'cardscraper.model']
my_impl = 'mypackage:gen_model'
[project.entry-points.'cardscraper.scraping']
my_impl = 'mypackage:gen_notes'
[project.entry-points.'cardscraper.deck']
my_impl = 'mypackage:gen_deck'
[project.entry-points.'cardscraper.package']
my_impl = 'mypackage:gen_package'
```
