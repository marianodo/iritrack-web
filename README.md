Installation
============

Create a virtual environment 

```python
mkdir venv
virtualenv venv
```
 
Activate it using `source ./venv/bin/activate`. To install dependencies, 
use

```
pip install -r requirements.txt
```

Server Code
===========

run

	python runserver.py

and open http://localhost:8000/reports/driver_id .


Iritrac txt files to xml
========================

Converts CSV files generated by iritrack GPS tracking system to any xml based format. 
Output structure is determined by `template.mustache`

Depends on:

	pystache

which can be installed by typing 

	sudo pip install pystache

Usage
-----

To convert a single file type

	python txt2kml.py -f <filename>
 
 and the output file will have the same name but will end in `kml`

 To convert every file in the current directory, use

	python txt2kml.py -t

and to get more help type `python txt2kml.py -h`.


