import os


def create(infile):
    """
    Reads the sample mapping file corresponding to the MS/MS data. For each
    proteome plex dataset a directory will be created with an annotation.txt
    file.  The annotation file is a simple text file with mappings between the
    TMT channels and the sample labels, which is needed to generate final
    reports in the Philosopher run.
    :param infile: Sample mapping file
    :return: N/A
    """
    with open(infile) as file:
        while True:
            line = file.readline()
            if not line:
                break
            try:
                if line.split(';')[1].split('_')[2] == 'Proteome':
                    os.mkdir(line.split(';')[1])
                    name = line.split(';')[1] + '/annotation.txt'
                    outfile = open(name, 'w')
                    tmt_126 = 'Pool'
                    tmt_127n = line.split(';')[5]
                    tmt_127c = line.split(';')[7]
                    tmt_128n = line.split(';')[9]
                    tmt_128c = line.split(';')[11]
                    tmt_129n = line.split(';')[13]
                    tmt_129c = line.split(';')[15]
                    tmt_130n = line.split(';')[17]
                    tmt_130c = line.split(';')[19]
                    tmt_131n = line.split(';')[21]
                    tmt_131c = line.split(';')[23]

                    outfile.write('tmt_126 ' + tmt_126 + '\n' +
                                  'tmt_127n ' + tmt_127n + '\n' +
                                  'tmt_127c ' + tmt_127c + '\n' +
                                  'tmt_128n ' + tmt_128n + '\n' +
                                  'tmt_128c ' + tmt_128c + '\n' +
                                  'tmt_129n ' + tmt_129n + '\n' +
                                  'tmt_129c ' + tmt_129c + '\n' +
                                  'tmt_130n ' + tmt_130n + '\n' +
                                  'tmt_130c ' + tmt_130c + '\n' +
                                  'tmt_131n ' + tmt_131n + '\n' +
                                  'tmt_131c ' + tmt_131c)

            except IndexError:
                pass


if __name__ == '__main__':
    create(snakemake.input.sample_mapping)
