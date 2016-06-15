# import Bio
from Bio import SeqIO, SeqFeature

def read_annotation(annot_file, file_format='genbank'):
    # record = SeqIO.read("NC_005816.fna", "fasta")
    record = SeqIO.read(annot_file, file_format)
    for feature in record.features:
        print(feature.location.start, feature.location.end, feature.location.strand)


read_annotation("oti.gb", "genbank")