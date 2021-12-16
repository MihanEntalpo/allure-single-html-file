# Allure single html file builder

Tool to build allure generated folder into a single html file

## What it's doing?

After run by console command, or by call from python code, it:

1. Reads contents of allure-generated folder
2. Creates server.js file, which has all the data files inside and code to start fake XHR server
3. Patches index.html file, so it's using server.js and sinon-9.2.4.js (Taken from [here](https://sinonjs.org/)), and could be run in any browser without --allow-file-access-from-files parameter of chrome browser
4. Creates file complete.html with all files built-in in a single file

## Requirements

* Python 3.5+
* You need to have your allure report folder generated (`allure generate './some/path/to/allure/generated/folder'`)

## Installation

(pip module not available yet, coming soon)

1. Clone repo

```bash
git clone git@github.com:MihanEntalpo/allure-single-html-file.git
cd allure-single-html-file
```

2. Install requirements (actually there are only BeautifulSoup)

```bash
pip install -r ./requirements.tx
```

## Run as console script

```bash
python ./combine.py ./some/path/to/allure/generated/folder
```

## Import and use in python code

```python
from combine import combine_allure

combine_allure("./some/path/to/allure/generated/folder")
```

## TODO

* Functionality to open image in new browser tab doesn't work yet.
* Need to check for attached html-files
