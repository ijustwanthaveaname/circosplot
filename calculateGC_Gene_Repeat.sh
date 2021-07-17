#!/usr/bin/zsh
# Get gene information.
grep '[[:blank:]]gene[[:blank:]]' Gekko_japonicus_new_chr.gff | cut -f 1,4,5 | awk '{print $1"\t"$2"\t"$3}' > genes.bed
# Get 2 column file includes chrname and length.
cut -d ' ' -f 3,6 karyotype.gj.txt  | tr ' ' '\t' > gj.genome
# Generate sliding windows.
bedtools makewindows -g gj.genome -w 500000 > gj.windows
# Calculate gene density
bedtools coverage -a gj.windows -b genes.bed| cut -f 1-4 > genes_num.txt
# Get repeat information
gawk -F"\t" '$1~/^Superscaffold/{sub(/^Superscaffold/,"Chr");print $1,$4,$5}' all.gff.xls > repeats.bed
# Calculate repeat density
bedtools coverage -a gj.windows -b repeats.bed | cut -f 1-4 > repeats_num.txt
# Calculate bases content
bedtools nuc -fi ../../Gekko/Gekko_japonicus_new_chr.fna -bed gj.windows > gj_nuc.txt
# Extract gc content
gawk -F"\t" 'BEGIN{OFS="\t"}NR>1{print $1,$2,$3,$5}' gj_nuc.txt > gc_content.txt
