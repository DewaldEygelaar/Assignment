import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(snakemake.input[0], header=None, skiprows=[0,2])
df.columns = ["Sample","Average depth", "%Reference covered", "Total_mapped bases", "Soft-clipped basses", 'Soft-clipped rate','Max AlignmentScore','Min AlignmentScore','Avg AlignmentScore']

df.plot(title = 'Average depth',x ='Sample', y='Average depth', kind = 'bar', color='green')
plt.tight_layout()

plt.savefig(snakemake.output[0])

df.plot(title = 'Percentage of refencence covered',x ='Sample', y='%Reference covered', kind = 'bar', color='yellow')
plt.tight_layout()

plt.savefig(snakemake.output[1])

df.plot(title = 'Mapped versus soft-clipped bases',x ='Sample', y=['Total_mapped bases', 'Soft-clipped basses'], kind = 'barh', color=['red','blue'])
plt.tight_layout()

plt.savefig(snakemake.output[2])

df.plot(title = 'Sam Alignment scores',x ='Sample', y=['Max AlignmentScore','Min AlignmentScore','Avg AlignmentScore'], kind = 'bar', color=['red','orange','yellow'])
plt.tight_layout()

plt.savefig(snakemake.output[3])
