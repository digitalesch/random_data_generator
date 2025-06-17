
# Project Title

A brief description of what this project does and who it's for

```
python -m venv <name of environment>
```

example

```
python -m venv venv
```

activate the environment with 
```
source venv/bin/activate
```

install requirements through ***"requirements.txt"*** file and wait for packages to be installed
```
pip install -r requirements.txt
```
Run commands for data generation

```
python scripts/generate_data.py && python scripts/partition_data.py
```

Data will be generated in path 
```
data/inputs/<filename>.csv
```
and partitioned like the bellow structure
```
data/partitions/<date field YEAR>/<date field MONTH>/<date field DAY>/<filename>_<date field YEAR><date field MONTH><date field DAY>
```

After executing the command, the data will be presented like so (the actual dates / data may vary, since its randomly generated)\
![image](https://github.com/user-attachments/assets/0f81267b-8055-4e23-b7b6-94989f04b91d)
