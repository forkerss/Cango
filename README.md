# Cango 💥

A library for executing commands asynchronously.

> From lotuc, i just encapsulate the module for reuse.

## Installation

```
pip install Cango
```

## Usage

You can override the `process_stdout`,`process_stderr` method

```Python
# Simple use of Cango
from Cango import Cango

cmd = ["masscan", "--ports", ports, ip_range]
masscan = Cango(cmd)
masscan.run()
print(masscan.finished)
for item in masscan.genresult():
    if item:
        print(item)
```
