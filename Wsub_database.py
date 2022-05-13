from Bio import SeqIO
import os


def TRYPSIN(seq):
    """
    This function takes the given protein sequence and tryptic digests it into
    peptides. For each given protein sequence, a peptide list is returned.
    Also, a list with the positions of digestion is returned for each given
    protein sequence.
    :param seq: Protein sequence to be tryptic digested
    :return:
    peptides: List of tryptic peptides
    sites: list of cutting sites
    """
    peptides = []
    sites = []
    cut_sites = [0]
    # trypsin cuts after K and R but not if next is P
    for i in range(0, len(seq) - 1):
        if seq[i] == 'K' and seq[i + 1] != 'P':
            cut_sites.append(i + 1)
        elif seq[i] == 'R' and seq[i + 1] != 'P':
            cut_sites.append(i + 1)

    if cut_sites[-1] != len(seq):
        cut_sites.append(len(seq))

    if len(cut_sites) > 2:
        for j in range(0, len(cut_sites) - 1):
            peptides.append(seq[cut_sites[j]: cut_sites[j + 1]])
            sites.append(str(cut_sites[j]) + "-" + str(cut_sites[j + 1]))

    else:  # there is no trypsin site in the protein sequence
        peptides.append(seq)
    return peptides, sites

def make_fasta(essential_aa):
    """
    This function takes the human proteome and changed all W codons to all other codons.
    The new fasta file is created for the W-substitutant protein sequence database.
    :param essential_aa: Tryptophan > 'W' (amino acid to be substituted)
    """
    aa_list = ['A', 'C', 'D', 'E', 'M', 'G', 'V', 'H', 'I', 'N', 'P',
             'Q', 'S', 'F', 'T', 'Y', 'L', 'W']
    filename = 'uniprot_human_Wsub.fasta'

    new_fasta = open(filename, 'w')

    # each header has a unique number to it (count) to keep sequences distinguishable 
    count = 1
    for y in aa_list:
        if essential_aa != y:
            for record in SeqIO.parse("uniprot_human.fasta", "fasta"):
                header = '>' + record.description
                sequentie = record.seq
                pos_string = ''
                pos = 1
                new_seq = ''
                for aa in sequentie:
                    if aa == essential_aa:
                        new_seq += y
                        pos_string += '_' + (str(pos))
                    else:
                        new_seq += aa
                    pos += 1
                if pos_string == '':
                    pos_string = ''
                elif pos_string != '':
                    peptide_list, sites_list = TRYPSIN(new_seq)
                    for peptide in peptide_list:
                        try:
                            pep_not_sub = sequentie.index(peptide)
                        except ValueError:
                            if y in peptide and 5 < len(peptide) < 51:
                                string = ">" + essential_aa + '_' + y + "_" + str(count)
                                new_fasta.write("%s\n%s\n" % (string, peptide))
                                count += 1


def main():
    make_fasta('W')


main()
