# AyonPDFMerger
# Merge PDF files easily.
# 'outputFileName' (extension .pdf not mandatory) is the output PDF file name. 
# If not specified, it'll be 'result.pdf' and will be written to the least
# common directory of the param files.
# Usage 1:
# 	python AyonPDFMerger.py [-o "outputFileName"] "path/to/directory/with/pdf/files"
# Usage 2:
# 	python AyonPDFMerger.py [-o "outputFileName"] "path/to/directory/with/config.txt"
# Usage 3:
# 	python AyonPDFMerger.py [-o "outputFileName"] "path/to/a.pdf" "path/to/b.pdf" "path/to/c.pdf" ...

import os
import sys
import getopt
import glob
import os.path
import fnmatch
from os import listdir
from os.path import isfile, join
from PyPDF2 import PdfFileReader, PdfFileMerger

# Merge all PDF files and creates a single resulting PDF file.
def mergePDFFiles(pdfs, resultFileName):
	# F*** you, Windows.
	if os.name == 'nt':
		pdfs = [pdf.replace(os.sep, '/') for pdf in pdfs]

	merger = PdfFileMerger()
	for pdf in pdfs:
		merger.append(pdf)

	merger.write(resultFileName)

# Gets all the .pdf files in the folder.
def getPDFFilesInFolder(folder):
	pattern = '*.pdf'
	pdfFiles = []
	
	# Get all files.
	allFiles = os.listdir(folder)

		# Keep only .pdf files.
	for file in allFiles:  
		if fnmatch.fnmatch(file, pattern):
			pdfFiles.append(os.path.abspath(os.path.join(folder + os.sep + file)))

	return pdfFiles

# Finds all the .pdf files that are listed in the text file.
def getPDFFilesInTextFile(txtFile):
	pattern = '*.pdf'
	pdfFiles = []

	# The .pdf files are the file lines and should keep that order.
	with open(txtFile, 'r', encoding='utf-8') as f:
		allFiles = f.readlines()
		allFiles = [line.strip() for line in allFiles]

		# Keep only .pdf files.
		for file in allFiles:
			if fnmatch.fnmatch(file, pattern):
				pdfFiles.append(file)
		f.close()

	return pdfFiles

# Gets the least common directory (prefix) for all the files.
def getCommonFolder(files):
	folders = [os.path.dirname(file) for file in files]
	commonPrefix = os.path.abspath(os.path.commonprefix(folders))
	return commonPrefix

# Parses command paramters to get the list of input files and the output file.
# Defaults to 'result.pdf' for the output file, if not specified.
def getPDFFilesToMerge(cmdArgs):
	try:
		optionList, files = getopt.getopt(cmdArgs, ':o:')
	except getopt.GetoptError as err:
		print(err) 
		sys.exit(2)
	
	# Get output file and file count.
	output = None
	fileCount = len(files)

	for option, optionValue in optionList:
			if option in ('-o', '--output'):
				output = optionValue
			else:
				print('unhandled option: ' + option) 

	# Ensure the output file has the .pdf extension.
	if output != None:
		path, extension = os.path.splitext(output)
		if extension.lower() != '.pdf':
			output += '.pdf'

	# Input file list.
	validFiles = []
	defaultOutputName = 'result.pdf'

	if fileCount > 0:
		# Special case for single input parameter: it might be a directory or .txt
		if fileCount == 1:
			file_0 = files[0]
			filePath, fileExtension = os.path.splitext(file_0)
			if fileExtension == '':
				# Get all .pdf files in the directory.
				retrievedFiles = getPDFFilesInFolder(filePath)
				validFiles.extend(retrievedFiles)
				
				if output == None:
					# Output will be in the same directory.
					output = os.path.abspath(os.path.join(filePath + os.sep + output))
				
			elif fileExtension == '.txt':
				# Get all .pdf files in the .txt file.
				retrievedFiles = getPDFFilesInTextFile(os.path.abspath(file_0))
				validFiles.extend(retrievedFiles)

				if output == None:
					# Output will be the least common path.
					output = os.path.abspath(os.path.join(getCommonFolder(retrievedFiles) + os.sep + defaultOutputName))

		# Multiple files.
		else:
			for file in files:
				retrievedFiles = []
				# Get .pdf files.
				filePath, fileExtension = os.path.splitext(file)
				if fileExtension.lower() == '.pdf':
					retrievedFiles.append(file)
				else:
					print('ignored file: ' + file) 
				validFiles.extend(retrievedFiles)

				if output == None:
					# Output will be the least common path.
					output = os.path.abspath(os.path.join(getCommonFolder(retrievedFiles) + os.sep + defaultOutputName))

	return output, validFiles

# Main.
if __name__ == '__main__':
	print('---- AyonPDFMerger v1.0 ----')
	# Get params.
	result = getPDFFilesToMerge(sys.argv[1:])
	outputFile = result[0]
	inputFiles = result[1]

	# Print all input files that will be used.
	print('Input:')
	for inputFile in inputFiles:
		print(' << ' + inputFile)

	# Print output file.
	print('Output:')
	print(' >> ' + outputFile)
	
	# Merge files.
	print('Merging...')    
	mergePDFFiles(inputFiles, outputFile)
	print('Done.')
