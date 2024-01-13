# Python Local Database
![Logo Python Local Database](https://raw.githubusercontent.com/fortmea/python-local-database/main/images/logo.png)

A python package made to simplify the use of json as a mean to organize and store data in python.
[![Upload Python Package](https://github.com/fortmea/python-local-database/actions/workflows/release.yml/badge.svg)](https://github.com/fortmea/python-local-database/actions/workflows/release.yml)
----------

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Python Local Database.

### Linux/macOS:
```bash
pip install pylocaldatabase
```

### Windows:
```bash
py -m pip install pylocaldatabase
```

Release history and file downloads can be found [on the project's pypi page](https://pypi.org/project/pylocaldatabase/).

----

## Usage

```python

# import library
from pylocaldatabase import pylocaldatabase

# define database file and assign databasecontroller instance to var dbcontroll
dbcontroll = pylocaldatabase.databasecontroller(path="file.json")

# load data from file
dbcontroll.load()

# create database file 'file.json'
dbcontroll.makeDatabase()

# creating document 
dbcontroll.insertDocument({}, "documentName")

# assigning document to a var
document = dbcontroll.getDocument("documentName")

# inserting Item in the document
document.insertItem("ItemName", {"Property":"Property Value"})

# reading Item data
itemData = document.getItem("ItemName").get()

# assigning item to var
item = document.getItem("ItemName")

# inserting new property in Item
item.insertProperty("Property Name", "Property Value")

# removing property from item
item.removeProperty("Property Name")

# removing item from document 

document.removeItem("ItemName")

# save data 
dbcontroll.save()
```
## Examples
Examples can be found [here](https://github.com/fortmea/python-local-database/tree/main/examples).

## Cryptography
An example on how to use the built-in Cryptography functions, you can refer to [Example 2.](https://github.com/fortmea/python-local-database/blob/main/examples/example2.py)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
