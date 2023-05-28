# Allure single html file builder

Tool to build allure generated folder into a single html file

## What it's doing?

After run by console command, or by call from python code, it:

1. Reads contents of allure-generated folder
2. Creates server.js file, which has all the data files inside and code to start fake XHR server
3. Patches index.html file, so it's using server.js and sinon-9.2.4.js (Taken from [here](https://sinonjs.org/)), and could be run in any browser without --allow-file-access-from-files parameter of chrome browser
4. Creates file complete.html with all files built-in in a single file

## Requirements

* Python 3.6+
* You need to have your allure report folder generated (`allure generate './some/path/to/allure/generated/folder'`)

## Installation


### Install with pip

```shell
pip install allure-combine
```

or:

### Install manually

1. Clone repo

```bash
git clone git@github.com:MihanEntalpo/allure-single-html-file.git
cd allure-single-html-file
```

2. Install requirements (actually there are only BeautifulSoup)

```bash
pip install -r ./requirements.txt
python setup.py install
```

## Run as console script

If you have cloned repo, not installed module via pip, replace `allure-combine` with `python ./allure_combine/combine.py` in following commands:

1) Create complete.html file inside the allure folder itself

```bash
allure-combine ./some/path/to/allure/generated/folder
```

2) Create complete.html file inside specified folder:

```bash
allure-combine ./some/path/to/allure/generated/folder --dest /tmp
```

3) Ensure that specified dest folder exists (create if not)

```bash
allure-combine ./some/path/to/allure/generated/folder --dest /tmp/allure-2022-05-05_12-20-01/result --auto-create-folders
```

4) Remove sinon.js and server.js from allure folder after complete.html is generated:


```bash
allure-combine ./some/path/to/allure/generated/folder --remove-temp-files
```

5) If html/json files what should be utf-8 is has broken encoding, ignore errors:
```bash
allure-combine ./some/path/to/allure/generated/folder --ignore-utf8-errors
```


## Import and use in python code

```shell
pip install allure-combine
```

```python
from allure_combine import combine_allure

# 1) Create complete.html in allure-generated folder
combine_allure("./some/path/to/allure/generated/folder")

# 2) Create complete.html in specified folder
combine_allure("./some/path/to/allure/generated/folder", dest_folder="/tmp")

# 3) Make sure that dest folder exists, create if not
combine_allure(
    "./some/path/to/allure/generated/folder",
    dest_folder="/tmp/allure-2022-05-05_12-20-01/result",
    auto_create_folders=True
)

# 4) Remove sinon.js and server.js from allure folder after complete.html is generated:
combine_allure(
    "./some/path/to/allure/generated/folder",
    remove_temp_files=True
)

# 5) If html/json files what should be utf-8 is has broken encoding, ignore errors:
combine_allure(
    "./some/path/to/allure/generated/folder",
    ignore_utf8_errors=True
)


```

## TODO

* Functionality to open image or video in new browser tab doesn't work yet.
* Need functionality to return combined file as a string, not saving it to a file directly
* Functionality to not change source files at all, work in a read-only filesystem

## Ports to other languages:

* Javascript port: https://github.com/aruiz-caritsqa/allure-single-html-file-js
