import csv
import subprocess
from os import path
import pandas as pd
import numpy as np
#import pysam

file = snakemake.input[0].replace("data/sorted_reads/combined_","")

basics = subprocess.Popen(('samtools stats ' + snakemake.input[0] + ' | grep ^SN | cut -f 2- > metrics/' + file + '_stats.txt'),shell=True, stdout=subprocess.PIPE, universal_newlines=True)
basic_stats = str(basics.communicate()[0])

total_bases = subprocess.Popen(('samtools stats ' + snakemake.input[0] + ' | grep ^SN | cut -f 2- | grep "total length" | cut -f2'),shell=True, stdout=subprocess.PIPE, universal_newlines=True)
total = str(total_bases.communicate()[0])

depth = subprocess.Popen(('samtools depth ' + snakemake.input[0] + '| awk "{sum+=\$3} END { print sum/NR}"'),shell=True, stdout=subprocess.PIPE, universal_newlines=True)
avg_depth = str(depth.communicate()[0])


coverage = subprocess.Popen(('samtools depth -a ' + snakemake.input[0] + ' | awk "{c++; if(\$3>0) total+=1}END{print (total/c)*100}"'), shell=True, stdout=subprocess.PIPE, universal_newlines=True)
covered = str(coverage.communicate()[0])


total_mapped = subprocess.Popen(('samtools depth ' + snakemake.input[0] + ' | awk "{if(\$3>0) total+=1}END{print total}"'),shell=True, stdout=subprocess.PIPE, universal_newlines=True)
mapped = str(total_mapped.communicate()[0])


soft = subprocess.Popen(('cat ' + snakemake.input[1] + ' | cut -f6 | grep -o -P ".{0,2}S" | tr "M" "0" | sed "s/S$//" | paste -sd+ | bc'),shell=True, stdout=subprocess.PIPE, universal_newlines=True)
soft_clipped = str(soft.communicate()[0])

max_alignment_score = subprocess.Popen(('cat ' + snakemake.input[1] + ' | cut -f14 | awk "{if(\$1)print substr(\$1,6,15)}" | sort -n | tail -1'),shell=True, stdout=subprocess.PIPE, universal_newlines=True)
max_align = str(max_alignment_score.communicate()[0])

min_alignment_score = subprocess.Popen(('cat ' + snakemake.input[1] + ' | cut -f14 | awk "{if(\$1)print substr(\$1,6,15)}" | sort -n | head -1'),shell=True, stdout=subprocess.PIPE, universal_newlines=True)
min_align = str(min_alignment_score.communicate()[0])

avg_alignment_score = subprocess.Popen(('cat ' + snakemake.input[1] + ' | cut -f14 | awk "{if(\$1)print substr(\$1,6,15)}" | awk "{ total += \$1; count++ } END { print total/count }"'),shell=True, stdout=subprocess.PIPE, universal_newlines=True)
avg_align = str(avg_alignment_score.communicate()[0])

soft_rate = (int(soft_clipped) / int(total)) * 100

panda_columns = ['Sample_name', 'Average depth', '% Reference covered', 'Total_mapped', 'Unmapped_reads', 'Soft_clipped bases', 'Soft-clipped rate', 'Max AlignmentScore','Min AlignmentScore','Avg AlignmentScore']
data = [[file, float(avg_depth), float(covered), int(mapped), int(soft_clipped), int(soft_rate), int(max_align), int(min_align), float(avg_align)]]

df_single = pd.DataFrame(data, columns=['Sample name', 'Average depth', '% Reference covered', 'Total_mapped', 'Soft_clipped bases', 'Soft-clipped rate', 'Max AlignmentScore','Min AlignmentScore','Avg AlignmentScore'])

df_combined = pd.DataFrame(data)

df_single.to_csv('./metrics/' + file + '.csv')

authenticate = path.exists("./metrics/metrics.csv")

csv_mode='w'


if authenticate:
    df_combined.append(data,ignore_index=True)
    csv_mode = 'a'

df_combined.to_csv('./metrics/metrics.csv',mode=csv_mode,index=False)  
