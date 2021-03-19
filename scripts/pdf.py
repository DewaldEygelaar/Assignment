from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.pagesizes import letter


#Resources
logo = "resources/roche.png"
qc_icon = "resources/QC.png"
avg_depth = "plots/depth.png"
mapped = "plots/mapped.png"
coverage = "plots/cov.png"
align = "plots/align.png"


styles = getSampleStyleSheet()
style = styles['Title']
styleN = styles['Normal']

pdf_name = "PDF/Report.pdf"
doc = SimpleDocTemplate(
    pdf_name,
    pagesize=letter,
    bottomMargin=.4 * inch,
    topMargin=.6 * inch,
    rightMargin=.8 * inch,
    leftMargin=.8 * inch)

items = []
link = '../fastQC/combined_HyperPlus_fastqc.html'
link2 = '../fastQC/combined_HyperPrep_fastqc.html'
items.append(Paragraph(link, style))
items.append(Paragraph(link2, style))

#Use canvas to build PDF
c = canvas.Canvas("PDF/Report.pdf")

#Import basic stats from samtools

#my_file = open(bam_stats, 'r')
#lines = my_file.readlines()
#file_contents = my_file.read()

#P = Paragraph(file_contents, styleN)
#items.append(P)

#doc.build(
#    items,
#)

#Headers
c.setFont('Helvetica-Bold', 15)
c.drawString(180, 820, "Assigment Report: Dewald Eygelaar")

#Sub headers
c.setFont('Helvetica-Bold', 9)
c.drawString(100,790, "Report to: Roche")
c.drawString(100, 730, "FastQC reports:")
c.drawString(100, 690, "Bam basic stats:")

c.setFont('Helvetica', 8)


#c.drawString(100, 720, file_contents)

#FastQC data

c.drawString(100, 710, "HyperPlus_fastqc  >")
c.drawString(230, 710, "HyperPrep_fastqc  >")

c.drawInlineImage(qc_icon, 180, 705, 15,15)
c.drawInlineImage(qc_icon, 320, 705,15,15)

r1 = (2.47*inch, 10.03*inch, 2.74*inch, 9.77*inch) # this is x1,y1,x2,y2
c.linkURL(link, r1, thickness=1)

r1 = (4.44*inch, 10.03*inch, 4.71*inch, 9.77*inch) # this is x1,y1,x2,y2
c.linkURL(link2, r1, thickness=1)



c.drawImage(logo, 20, 750, 75, 75)
c.drawImage(logo, 500, 20, 75, 75)

c.drawImage(avg_depth, x=50, y=450, width=200, height=200)
c.drawImage(mapped, x=310, y=450, width=200, height=200)
c.drawImage(coverage, x=50, y=240, width=200, height=200)
c.drawImage(align, x=310, y=240, width=200, height=200)


#Text to be added to pdf
c.drawString(100, 675, "Bam statistics saved to metrics/{sample}_stats.txt")

c.drawString(100, 660, "Soft-clip rate was calculated as soft-clipped bases / total bases * 100 = 10% for both samples")

c.drawString(60,234, "After an initial check using a QC program, the reads needed trimming as well as adpater removal. According to QC it")
c.drawString(60,226, "the universal Illumina adapter that was used. The HyperPrep sample has roughly twice as many soft-clipped. Soft-clipping")
c.drawString(60,218, "may force reads to align at the wrong location, mostly seen at repetitive regions. This may the explain the double amount")
c.drawString(60,210, "of mismatches in HyperPrep vs HyperPlus. ")
c.drawString(60,198, "The HyperPlus sample contains overrepresentation that may point to some form of contaminant, this corresponds with the sharper")
c.drawString(60,190, "per sequence GC content. Even after adapter trimming, fastQC still failed on Adapter content, which again point to ")
c.drawString(60,182, "over-representation of sequences maybe contamination. The reduced coverage in HyperPlus may be explained by the PCR step not")
c.drawString(60,174, "having enough cycles or the PCR was prematurely stop or ran out of dNTPS. Geneious inspection of the alignments as well as")
c.drawString(60,166, "the reference fasta, showed that the reference contains some ambigious N's and reads will not map to these parts.")


c.save()
