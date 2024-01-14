# badbyte
![logo](https://raw.githubusercontent.com/C3l1n/badbyte/main/assets/logo.png)

Deal with bad characters easily during exploit writing with badchars.

## Table of Contents

1. [Installation](#Instalation)
2. [Usage](#Usage)
   * [Generate payload to check all characters](#Generate-payload-to-check-all-characters)
   * [Analyze memory dumped after trigger](#Analyze-memory-dumped-after-trigger)
3. [Programatically use](#Programatically-use)

## [↑](#table-of-contents)Instalation

using pip:
```bash
pip3 install badbyte 
```

or from repo:
```bash
git clone git@github.com:C3l1n/badbyte.git
cd badbyte
pip3 install .
```

## [↑](#table-of-contents)Usage

You can always use:
```bash
badbyte --help
```

### [↑](#table-of-contents)Generate payload to check all characters

```bash
badbyte g --bad "3d 26 25 0d" --pre START --post STOP
```

![logo](https://raw.githubusercontent.com/C3l1n/badbyte/main/assets/usage.png)

use:
* --bad to supply hexascii values of bad characters
* --pre to set string for marking start point (or leave default)
* --post to set string for marking stop point (or leave default)

Then use payload in your exploit and fire it.

### [↑](#table-of-contents)Analyze memory dumped after trigger

Copy hexascii from memory dump of your favourite debugger i.e. windbg:

![logo](https://github.com/C3l1n/badbyte/blob/main/assets/windbg.png)

remember to skip addresses and ascii representation. I use vim and column select or visual studio code and alt+shift select.

![logo](https://raw.githubusercontent.com/C3l1n/badbyte/main/assets/vscode.png)

Fire badbyte to analyze output:

```bash
badbyte p -c --pre START --post STOP
```

![logo](https://raw.githubusercontent.com/C3l1n/badbyte/main/assets/analyze.png)

## [↑](#table-of-contents)Programatically use

Documentation not made (feel free to read code) but you can find in example/programatically_generate_payload.py example of payload generation in exploit.