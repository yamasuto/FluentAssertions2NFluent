# FluentAssertions2NFluent

Migration script from FluentAssertions to NFluent

<div id="top"></div>

<p style="display: inline">
  <img src="https://img.shields.io/badge/-Python-F2C63C.svg?logo=python&style=for-the-badge">
</p>

This Python script converts C# assertions written using **[FluentAssertions](https://github.com/fluentassertions/fluentassertions)** to **[NFluent](https://github.com/tpierrain/NFluent)**. 
It scans `.cs` files in the specified directory and applies regex-based replacements to switch the assertion syntax from FluentAssertions to NFluent.

**The regex-based replacements does not cover all FluentAssertions functions.**
You can add more regex-based replacements.

## Features

- Replaces common FluentAssertions patterns such as `Should().Be()`, `Should().Equal()`, `Should().BeSameAs()`, and many others.
- Handles both parameterized and parameterless assertions.
- Automatically detects the indentation before `Should()` calls to ensure accurate replacements in files with varying levels of indentation.

## Usage

### Prerequisites

- Python 3.x
- Basic knowledge of regex-based string replacements.

### Running the Script

To run the script, use the following command:

```bash
python replace_fluent_with_nfluent.py <directory>
```

### Notes

- The script overwrites the original files, so ensure you have backups or version control in place.
- It only processes .cs files. Make sure the target directory contains C# files that use FluentAssertions.
- **The replacement of multi-line definitions may not yield the expected results.** Please correct them manually after running the script.
