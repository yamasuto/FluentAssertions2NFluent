import os
import re
import sys

# Define the replacement patterns for FluentAssertions to NFluent
REPLACEMENT_PATTERNS = [
    (r'\.Should\(\)\.Be\((.+?)\);', r'Check.That(\1).Is(\2);'),
    (r'\.Should\(\)\.Equal\((.+?)\);', r'Check.That(\1).Equals(\2);'),
    (r'\.Should\(\)\.BeSameAs\((.+?)\);', r'Check.That(\1).IsSameReferenceAs(\2);'),
    (r'\.Should\(\)\.NotBeSameAs\((.+?)\);', r'Check.That(\1).Not.IsSameReferenceAs(\2);'),
    (r'\.Should\(\)\.NotBe\((.+?)\);', r'Check.That(\1).IsNotEqualTo(\2);'),
    (r'\.Should\(\)\.BeEquivalentTo\((.+?)\);', r'Check.That(\1).Equals(\2);'),
    (r'\.Should\(\)\.HaveCount\((.+?)\);', r'Check.That(\1).CountIs(\2);'),
    (r'\.Should\(\)\.StartWith\((.+?)\);', r'Check.That(\1).StartsWith(\2);'),
    (r'\.Should\(\)\.EndWith\((.+?)\);', r'Check.That(\1).EndsWith(\2);'),
    (r'\.Should\(\)\.BeGreaterThan\((.+?)\);', r'Check.That(\1).IsStrictlyGreaterThan(\2);'),
    (r'\.Should\(\)\.BeOnOrAfter\((.+?)\);', r'Check.That(\1).IsAfterOrEqualTo(\2);'),
    (r'\.Should\(\)\.HaveCountGreaterThanOrEqualTo\((.+?)\);', r'Check.That(\1)./*HaveCountGreaterThanOrEqualTo*/(\2);'),
    (r'\.Should\(\)\.BeLessThanOrEqualTo\((.+?)\);', r'Check.That(\1)IsLessOrEqualThan(\2);'),
    # Parameter-less replacements
    (r'\.Should\(\)\.BeEmpty\(\);', r'Check.That(\1).IsEmpty();'),
    (r'\.Should\(\)\.NotBeEmpty\(\);', r'Check.That(\1).Not.IsEmpty();'),
    (r'\.Should\(\)\.BeNull\(\);', r'Check.That(\1).IsNull();'),
    (r'\.Should\(\)\.NotBeNull\(\);', r'Check.That(\1).IsNotNull();'),
    (r'\.Should\(\)\.BeTrue\(\);', r'Check.That(\1).IsTrue();'),
    (r'\.Should\(\)\.BeFalse\(\);', r'Check.That(\1).IsFalse();'),
    # template
    # misunderstanding (r'\.Should\(\)\.BeAssignableTo<(.+?)>\(\);', r'Check.That(\1).IsInstanceOf<\2>();'),
    (r'\.Should\(\)\.BeAssignableTo<(.+?)>\(\);', r'Check.That(\1).InheritsFrom<\2>();'),

    # multi-line
    (r'\.Should\(\)\.Equal\(', r'Check.That(\1).Equals('),
    (r'\.Should\(\)\.Be\(', r'Check.That(\1).Is('),
]

def replace_assertions(content, first_group):
    """Replace FluentAssertions with NFluent using defined patterns."""
    for pattern, replacement in REPLACEMENT_PATTERNS:
        content = re.sub(first_group + pattern, replacement, content)
    return content

def process_file(file_path, first_group):
    """Read the file, replace assertions, and save the result."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    new_content = replace_assertions(content, first_group)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(new_content)

def get_max_indentation_spaces(file_path) -> int:
    """Calculate the maximum number of spaces before `.Should().` in the file."""
    max_spaces = 0
    # print(f'### staring {file_path} {os.path.isfile(file_path)}')
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lc = 0
            for line in file:
                lc = lc + 1
                if '.Should().' not in line:
                    continue
                stripped_line = line.strip()
                if stripped_line.startswith('//') != True:
                    continue
                if stripped_line.endswith(';') != True:
                    print(f'detected multi-line definition at {lc} in {file_path}')
                idx = stripped_line.find('.Should().')
                space_count = stripped_line[:idx].count(' ')
                max_spaces = max(max_spaces, space_count)
        return max_spaces
    except UnicodeDecodeError as e:
        print(f"failed to read '{file_path}', Change the file encoding, {e}")
    except Exception as e:
        print(f"failed to read '{file_path}' {e}")

def main(directory):
    file_count = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.cs'):
                file_path = os.path.join(root, file)
                max_spaces = get_max_indentation_spaces(file_path) + 1

                for n in range(max_spaces, 0, -1):
                    first_group = r'([\S]+)'
                    if n > 1:
                        first_group = '(' + ' '.join([r'[\S]+'] * n) + ')'

                    process_file(file_path, first_group)
                    print(f'Processed with {n} {first_group} : {file_path}')

                file_count += 1

    print(f'Processed {file_count} files')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python replace_fluent_with_nfluent.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print("Usage: python replace_fluent_with_nfluent.py <directory>")
        sys.exit(1)

    main(directory)
