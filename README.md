# AyonPDFMerger

**AyonPDFMerger** is a basic utility to merge PDF files.

## Usage

This script accepts 3 kinds of parameters:

1. Pass a directory that contains `.pdf` files.
	```bash
	python AyonPDFMerger.py [-o "outputFileName"] "path/to/directory/with/pdf/files"
	```

2. Pass a configuration plain text file.
	```bash
	python AyonPDFMerger.py [-o "outputFileName"] "path/to/directory/with/config.txt"
	```

	The file should be something like this:

	```
	path/to/file/a.pdf
	path/to/another/file/b.pdf
	...
	```

3. Pass a list of files:
	```bash
	python AyonPDFMerger.py [-o "outputFileName"] "path/to/a.pdf" "path/to/b.pdf" "path/to/c.pdf" ...
	```

If no output file is specified, it defaults to `result.pdf`, and will be written to the least common files directory.

## License

MIT License.
