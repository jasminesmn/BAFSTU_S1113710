

def functie(path_db, path_ms, path_tmt, input_file, output_file):
    """
    Reads the original parameter file and adjust settings as desired.
    Dictionary 'setting_dict' contains all the settings which need to be
    adjusted. For each setting in the dictionary, the parameter will be
    adjusted, resulting in a custom parameter file ready for use.
    :param path_db: Path of human proteome fasta file
    :param path_ms: Path of MSFragger software
    :param path_tmt: Path of TMTIntegrator software
    :param input_file: Original parameter file
    :param output_file: Adjusted parameter file
    :return: N/A
    """
    path_database = path_db
    path_MSFragger = path_ms
    path_TMTintegrator = path_tmt

    settings_dict = {'  Database Search': 'yes', '  Peptide Validation': 'yes',
                     '  Label-Free Quantification': 'yes',
                     '  Isobaric Quantification': 'yes',
                     '  FDR Filtering': 'yes',
                     '  Individual Reports': 'yes',
                     '  Integrated Reports': 'yes',
                     '  Integrated Isobaric Quantification': 'yes',
                     'protein_database': path_database,
                     'search_engine': 'msfragger',
                     'precursor_mass_lower': '-20',
                     'precursor_mass_upper': '20',
                     'isotope_error': '-1/0/1/2/3',
                     'search_enzyme_name': 'stricttrypsin',
                     'search_enzyme_cutafter': 'KR',
                     'allowed_missed_cleavage': '2',
                     'variable_mod_03': '229.162932 n^ 1',
                     'variable_mod_04': '229.162932 S 1',
                     'precursor_charge': '1 6',
                     'use_topN_peaks': '300',
                     'clear_mz_range': '125.5 131.5',
                     'add_K_lysine': '229.162932',
                     'bestPSM': 'true', 'plex': '11', 'removeLow': '0.05',
                     'razor': 'true', 'picked': 'true', 'mapMods': 'true',
                     'models': 'true', 'sequential': 'true', 'memory': '32',
                     'channel_num': '11', 'ref_tag': 'Pool',
                     'Y_type_masses': '0'}
    outfile = open(output_file, 'w')
    with open(input_file) as file:
        while True:
            line = file.readline()
            if not line:
                break
            params = line.split('#')[0].split(':')

            try:
                param = params[0].split('\t')
                value = params[1].split()
                for key in settings_dict:
                    if key in param[0]:
                        if value:
                            value.clear()
                            value.append(settings_dict[key])
                        else:
                            value.append(settings_dict[key])

                if ' path to TMT-Integrator jar' in line.split('#')[1]:
                    if value:
                        value.clear()
                        value.append(path_TMTintegrator)
                    else:
                        value.append(path_TMTintegrator)
                elif ' path to MSFragger jar' in line.split('#')[1]:
                    if value:
                        value.clear()
                        value.append(path_MSFragger)
                    else:
                        value.append(path_MSFragger)
                elif ' the location of output files' in line.split('#')[1]:
                    if value:
                        value.clear()
                        value.append('TMTIntegrator_output')
                    else:
                        value.append('TMTIntegrator_output')
                line = param[0] + ': ' + ' '.join(value) + \
                       '\t\t\t\t\t\t\t#' + line.split('#')[1]
                outfile.write(line)
            except IndexError:
                outfile.write(line)



if __name__ == '__main__':
    functie(snakemake.input.path_database, snakemake.input.path_MSFragger,
            snakemake.input.path_TMTintegrator, snakemake.input.input_file,
            snakemake.output.params)
