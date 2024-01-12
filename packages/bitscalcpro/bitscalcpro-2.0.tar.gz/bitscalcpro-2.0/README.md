<!-- BitsCalcPro -->

<p align="center"><b>BitsCalcPro</b></p>
<p align="center"><b>Comprehensive Numeric Converter & Analyzer</b></p>

##

<h3><p align="left">Disclaimer:</p></h3>

<i>This Python tool, named <b>BitsCalcPro</b> provides a versatile tool for converting between different numeric formats (decimal, binary, octal, hexadecimal, float and double).

Its extensive capabilities include byte order reversal, detailed bit size insights, and precise conversions for both normal order and reversed order formats.

Users can input values in different bases, and the tool will provide corresponding conversions, including binary, octal, hexadecimal, and floating-point representations.</i>

##

### Features:

- Bits size calculation:
  - Provides the number of bits required to represent the input value in binary, octal, hexadecimal, float, and double.

- Decimal conversions:
  - Converts decimal values to hexadecimal (normal and reversed order), octal, and binary.

- Binary conversions:
  - Converts binary values to decimal, hexadecimal (normal and reversed order), octal, float, and double.

- Octal conversions:
  - Converts octal values to decimal, hexadecimal (normal reversed order), binary, float, and double.

- Hexadecimal conversions:
  - Converts hexadecimal values to decimal, octal, binary, float, and double. Supports both normal and reversed modes.

- Float conversions:
  - Converts float values to hexadecimal (normal and reversed order), octal, binary, and double.

- Double conversions:
  - Converts double values to hexadecimal (normal and reversed order), octal, binary, and actual decimal.

These features make your tool versatile, allowing for seamless conversions between different number systems.

##

### Special Features:

- Input Validation:
  - Automatic validation to fix prefixes and spaces in input values.
  - Automatic determination the possible formats for the input values and then printing the results for each possible format.

- Byte Order Swap:
  - Specialized feature supporting byte order reversal for 16-bit, 32-bit, and 64-bit values.

- IEEE 754 Conversion Support:
  - Comprehensive support for IEEE 754 floating-point format, covering both single-precision (float) and double-precision (double) values.

##

### Installation:

- To install directly:
  ```bash
  pip install bitscalcpro
  ```

- To custom build, Clone this repository, Go to cloned directory and install the package:
  ```bash
  git clone https://github.com/muhammadrizwan87/bitscalcpro.git
  cd bitscalcpro
  python -m build
  pip install .
  ```
  
- After installation enter these commands:
  - To run the Tool:
    ```bash
    bcp
    ```
    - `bcp` short form of bitscalcpro.

  - Usage example:

    - To use with a numeric argument:
      ```bash
      bcp 1234
      ```
    - To export results:
      ```bash
      bcp 1234 | sed 's/\x1b\[[0-9;]*m//g' >> output.txt
      ```
##

### Follow Me on Telegram:
[Dimension of TDO](https://TDOhex.t.me)

[Useful Patches](https://Android_Patches.t.me)

<!-- // -->
