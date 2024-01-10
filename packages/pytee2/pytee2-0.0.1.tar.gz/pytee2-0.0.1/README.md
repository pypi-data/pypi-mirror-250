# pytee2

[![PyPI - Version](https://img.shields.io/pypi/v/pytee2.svg)](https://pypi.org/project/pytee2)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytee2.svg)](https://pypi.org/project/pytee2)

pytee2 is a package providing functionalities of redirecting `stdout` and `stderr` to a string and an output file. The key feature of pytee2 is that it can redirect `stdout` and `stderr` from C binding invocations. 

-----

**Table of Contents**

- [pytee2](#pytee2)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Known issues](#known-issues)
  - [License](#license)

## Installation

```console
pip install pytee2
```

## Usage

```Python
from pytee2 import Tee
tee = Tee(output_filepath='output.txt')
tee.start()

# do many things...

tee.stop()
```
Now the `stdout` and `stderr` have been saved to output.txt, and you can get the string version of the output by

```Python
capturedtext = tee.get_capturedtext()
```

## Known issues

pytee2 cannot work properly on Windows. This issue should be fixed in the future. 

## License

`pytee2` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
