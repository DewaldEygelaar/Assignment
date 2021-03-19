trimmomatic = "/home/dewald/bin"
maxthreads = 2

SAMPLES = ["HyperPlus","HyperPrep"]

QCED = ['fastQC/combined_'+f+'_fastqc.zip' for f in SAMPLES]
MERGED = ['data/samples/combined/combined_'+f+'.fastq' for f in SAMPLES]
METRICS = ['metrics/'+f+'.bam.csv' for f in SAMPLES]

rule all:
    input:
        "PDF/Report.pdf",
        "plots/cov.png",
        "plots/mapped.png",
        "plots/depth.png",
        "plots/align.png",
        METRICS,
        QCED, 
        MERGED,
        expand("data/trimmed/{sample}_R1.trim.final.fastq", sample=SAMPLES),
        expand("data/trimmed/{sample}_R2.trim.final.fastq", sample=SAMPLES),
        expand("data/trimmed/{sample}_R1.trim.unpaired.fastq", sample=SAMPLES),
        expand("data/trimmed/{sample}_R2.trim.unpaired.fastq", sample=SAMPLES)
       
                
#####TRiMMING#####
rule trim_forward:
    input:
        fastq = "data/samples/{sample}_R1.fastq",
        trim_jar = os.path.join(trimmomatic, "trimmomatic.jar")
    output:
        temp("data/trimmed/{sample}_R1.trim.fastq")
    threads:
        maxthreads
    message:
        "Trimming the first 24 bases from {input.fastq}"
    shell:
        """java -jar {input.trim_jar} SE -threads {threads} \
        {input.fastq} {output} HEADCROP:24"""

rule trim_reverse:
    input:
        fastq = "data/samples/{sample}_R2.fastq",
        trim_jar = os.path.join(trimmomatic, "trimmomatic.jar")
    output:
        temp("data/trimmed/{sample}_R2.trim.fastq")
    threads:
        maxthreads
    message:
        "Trimming the first 3 bases from {input.fastq}"
    shell:
        """java -jar {input.trim_jar} SE -threads {threads} \
        {input.fastq} {output} HEADCROP:3"""

rule trim_pairs:
    input:
        f1 = "data/trimmed/{sample}_R1.trim.fastq",
        f2 = "data/trimmed/{sample}_R2.trim.fastq",
        trim_jar = os.path.join(trimmomatic, "trimmomatic.jar"),
        adapter_path = "resources/adapters.fa"
    output:
        f_paired =   "data/trimmed/{sample}_R1.trim.final.fastq",
        r_paired =   "data/trimmed/{sample}_R2.trim.final.fastq",
        f_unpaired = "data/trimmed/{sample}_R1.trim.unpaired.fastq",
        r_unpaired = "data/trimmed/{sample}_R2.trim.unpaired.fastq"
    threads:
        maxthreads
    message:
        "Trimming {input.f1} and {input.f2} as a pair."
    shell:
        """java -jar {input.trim_jar} PE \
        -threads {threads} \
        -phred33 {input.f1} {input.f2} \
        {output.f_paired} \
        {output.f_unpaired} \
        {output.r_paired} \
        {output.r_unpaired} \
        ILLUMINACLIP:{input.adapter_path}:2:30:10:1:TRUE\
        LEADING:3 TRAILING:3 \
        SLIDINGWINDOW:4:15 MINLEN:36"""

#####MERGE PAIRS#####
rule merge_fastq:
    input:
        r1 = 'data/trimmed/{sample}_R1.trim.final.fastq',
        r2 = 'data/trimmed/{sample}_R2.trim.final.fastq'

    output:
        "data/samples/combined/combined_{sample}.fastq"
    shell:
        'cat {input.r1} {input.r2} > {output}'

#####FASTQC#####
rule fastqc:
    input: "data/samples/combined/combined_{sample}.fastq"
	output: "fastQC/combined_{sample}_fastqc.zip"
	shell: "/home/dewald/software/FastQC/fastqc -o fastQC {input}"


#####ALIGNMENT#####
rule minimap2:
    input:
        "data/Ecoli.fa",
        "data/samples/combined/combined_{sample}.fastq"

    output:
        "data/samples/combined/combined_{sample}.sam"

    shell:
        "/home/dewald/software/minimap2/minimap2 -a {input} > {output}"

rule samtools:
    input:
        "data/samples/combined/combined_{sample}.sam"
    output:
        "data/mapped_reads/combined_{sample}.bam"

    shell:
        "samtools view -Sb {input} > {output}"

#####SORTING#####
rule samtools_sort:
    input:
        "data/mapped_reads/combined_{sample}.bam"
    output:
        "data/sorted_reads/combined_{sample}.bam"
    shell:
        "samtools sort -T sorted_reads/{wildcards.sample} "
        "-O bam {input} > {output}"

#####INDEX#####
rule samtools_index:
    input:
        "data/sorted_reads/combined_{sample}.bam"
    output:
        "data/sorted_reads/combined_{sample}.bam.bai"
    shell:
        "samtools index {input}"

#####METRICS#####
rule metrics:
    input:
       "data/sorted_reads/combined_{sample}.bam",
       "data/samples/combined/combined_{sample}.sam"
    output:
       "metrics/{sample}.bam.csv",
       #"metrics/metrics.csv"
    script:
        "scripts/metrics.py"

#####PLOTTING#####
rule plot:
    input:
        "metrics/metrics.csv"
    output:
        "plots/cov.png",
        "plots/depth.png",
        "plots/mapped.png",
        "plots/align.png"
    script:
        "scripts/plot.py"

######PDF#####
rule pdf:
    output:
        "PDF/Report.pdf"
    script:
        "scripts/pdf.py"

