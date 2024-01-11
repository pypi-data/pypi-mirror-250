
# NS2JSON

Name Server to JavaScript Object Notation is a Python script to converts and saves a data from a DNS response to a JSON file.


## Installing

Install the module by [pip][1] (check [how to use pip][2]):

```
py -m pip install ns2json
```


## How to use

```python
py -m ns2json [domain] [dns] [path]
```

|| Domain | DNS | Path |
| :--- | :--- | :--- | :--- |
| Full name | Domain name | DNS resolver | Path to save |
| Required | Yes | No | No |
| Default | No | 1.1.1.1 | From executed script |
| Example | google.com | 8.8.8.8 | C:\Users\Name\Desktop


## Examples

```python
py -m ns2json google.com 8.8.8.8 C:\Users\Name\Desktop
py -m ns2json google.com 8.8.8.8
py -m ns2json google.com C:\Users\Name\Desktop

# Output file name: google.com.json
```

## Comments

- The script uses the nslookup tool.
- Currently, the script works only on Windows.

## To Do
- Linux version.

[1]: https://pypi.org/ 
[2]: https://pip.pypa.io/en/stable/getting-started/