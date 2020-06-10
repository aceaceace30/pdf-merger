from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
import os

pdf_files_path = 'pdf'
img_files_path = 'img'
img_extension = '.png'
blank_file = 'blank.pdf'

folder_of_stamp_files = 'output_files'

files = os.listdir(pdf_files_path)

for file in files:
	filename = file.split('.')[0]

	if not os.path.exists(os.path.join(img_files_path, filename + '.png')):
		print("No image available for DCR: %s" % (filename))
		continue

	print('Stamping DCR %s...' % (filename))

	output_file = PdfFileWriter()
	file_to_stamp = PdfFileReader(open(os.path.join(pdf_files_path, file), 'rb'))

	page_count = file_to_stamp.getNumPages()

	for page in range(page_count):
		c = canvas.Canvas(blank_file)
		image = os.path.join(img_files_path, filename + img_extension)
		c.drawImage(image, 405, 27, width=140, height=54)
		c.drawString(540, 35, str(page+1))
		c.save()

		watermark = PdfFileReader(open(blank_file, 'rb'))
		input_page = file_to_stamp.getPage(page)
		input_page.mergePage(watermark.getPage(0))
		output_file.addPage(input_page)

	new_filename = os.path.join(folder_of_stamp_files, '%s_superceded.pdf' % (filename))
	with open(new_filename, 'wb') as output:
		output_file.write(output)

	print('DCR %s has been stamped.' % (filename))
	print('***************************')