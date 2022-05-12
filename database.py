
#!/bin/python
import os
import mysql.connector as database


def databasemaken(cursor, connection):
    """
    Creates the tables for the database in SQL command format.
    Desired values for the tables are given and are put in a list.
    Looping through all SQL tables in the list, the tables will be created with
    cursor.execute(...).

    This function is not called when the data tables already exist!

    :param cursor: a variable to communicate with the database.
    :param connection: a variable to communicate with the database.
    :return: N/A
    """

    sql_lijst = []
    sql1 = """
    CREATE TABLE CANCER (
        cancer_id VARCHAR(25) PRIMARY KEY,
        name TEXT
        );
    """
    sql_lijst.append(sql1)
    sql2 = """
        CREATE TABLE SAMPLE (
            sample_id VARCHAR(50) PRIMARY KEY,
            cancer_id VARCHAR(25) REFERENCES CANCER(cancer_id),
            normal BOOLEAN,
            tumor BOOLEAN);
        """
    sql_lijst.append(sql2)

    sql3 = """
            CREATE TABLE GENES (
                gene_id INT PRIMARY KEY,
                gene_name VARCHAR(30));
            """
    sql_lijst.append(sql3)

    sql4 = """
        CREATE TABLE GENE_EXP (
            gene_id INT REFERENCES GENES(gene_id),
            sample_id VARCHAR(50) REFERENCES SAMPLE(sample_id),
            gene_expression FLOAT);
        """
    sql_lijst.append(sql4)

    sql5 = """
        CREATE TABLE COUNTS (
            substitution VARCHAR(2), 
            sample_id VARCHAR(50) REFERENCES SAMPLE(sample_id),
            count INT);
        """
    sql_lijst.append(sql5)

    sql6 = """
        CREATE TABLE CLUSTER_NORMAL (
            cancer_id VARCHAR(25) REFERENCES CANCER(cancer_id),
            gene_id INT REFERENCES GENES(gene_id),       
            wf_up FLOAT,
            wf_down FLOAT,
            wy_up FLOAT,
            wy_down FLOAT,
            num_up FLOAT,
            num_down FLOAT);
        """
    sql_lijst.append(sql6)

    sql7 = """
       CREATE TABLE CLUSTER_TUMOR (
           cancer_id VARCHAR(25) REFERENCES CANCER(cancer_id),
           gene_id INT REFERENCES GENES(gene_id),
	       wf_up FLOAT,
           wf_down FLOAT,
           wy_up FLOAT,
           wy_down FLOAT,
           num_up FLOAT,
           num_down FLOAT);
       """
    sql_lijst.append(sql7)

    for z in sql_lijst:
        cursor.execute(z)
    connection.commit()


def dictionaries():
    """
    Creates dictionaries for all data required for each table.

    (With each cancer type there will be common genes, but also other (new)
    genes not found in other cancer type data. To only add new genes to the
    database and avoid errors, all unique (new) genes will be written to
    'genes.txt' file. When a gene is not already in the 'genes.txt' file,
    the gene will be added to the database and also to the 'genes.txt' file.)

    :return:
    cancer_dict: Dictionary for CANCER table
    sample_dict: Dictionary for SAMPLE table
    counts_dict: Dictionary for COUNTS table
    genes_exp_dict: Dictionary for GENE_EXP table
    new_genes_dict: Dictionary for GENES table
    cluster_normal: Dictionary for CLUSTER_NORMAL table
    cluster_tumor: Dictionary for CLUSTER_TUMOR table

    """
    cancer_dict = {'LSCC': ['LSCC', 'Lung Squamous Cell Carcinoma']}
    sample_dict = {}
    genes_exp_dict = {}
    genes_dict = {}
    new_genes_dict = {}
    counts_dict = {}
    cluster_normal = {}
    cluster_tumor = {}

    dict = {}
    dict2 = {}
    count2 = 1
    count3 = 1

    file_genes1 = open('genes.txt', 'r')
    for gene in file_genes1.readlines():
        count = int(gene.strip().split('\t')[0])
        genes_dict[gene.strip().split('\t')[1]] = gene.strip().split('\t')
    file_genes1.close()
    file_genes2 = open('genes.txt', 'a')

    with open("/DATA/Jasmine/LSCC/cluster_tumor/TUMOR.txt") as file:
        while True:
            line = file.readline()
            if not line:
                break

            if line.split('\t')[0].startswith('id'):
                for column in line.split('\t'):
                    if not column.startswith('id') and len(column) == 2 and column.startswith('w'):
                        dict[str(line.split('\t').index(column))] = column.upper()
                    if not column.startswith('id') and not column.startswith('w'):
                        dict2[str(line.split('\t').index(column))] = column.rstrip('\n')
                        if column.rstrip('\n') not in genes_dict.keys():
                            count += 1
                            genes_dict[column.rstrip('\n')] = [count, column.rstrip('\n')]
                            file_genes2.write(str(count) + "\t" + column.rstrip('\n') +"\n")
                            new_genes_dict[column.rstrip('\n')] = [count, column.rstrip('\n')]

            if not line.split('\t')[0].startswith('id'):
                sample_dict[line.split('\t')[0]] = [line.split('\t')[0], 'LSCC', 0, 1]
                for key, value in dict.items():
                    counts_dict[count2] = [dict[key], line.split('\t')[0], int(line.split('\t')[int(key)])]
                    count2 += 1
                for key, value in dict2.items():
                    try:
                        genes_exp_dict[count3] = [genes_dict[value][0], line.split('\t')[0],
                                               float(line.split('\t')[int(key)])]
                    except ValueError:
                        genes_exp_dict[count3] = [genes_dict[value][0], line.split('\t')[0], None]
                    count3 += 1

    with open("/DATA/Jasmine/LSCC/cluster_normal/Normal.txt") as file:
        while True:
            line = file.readline()
            if not line:
                break
            if not line.split('\t')[0].startswith('id'):
                sample_dict[line.split('\t')[0]] = [line.split('\t')[0], 'LSCC', 1, 0]
                for key, value in dict.items():
                    counts_dict[count2] = [dict[key], line.split('\t')[0], int(line.split('\t')[int(key)])]
                    count2 += 1
                for key, value in dict2.items():
                    count3 += 1
                    try:
                        genes_exp_dict[count3] = [genes_dict[value][0], line.split('\t')[0],
                                                  float(line.split('\t')[int(key)])]
                    except ValueError:
                        genes_exp_dict[count3] = [genes_dict[value][0], line.split('\t')[0], None]

    with open("/DATA/Jasmine/LSCC/cluster_tumor/GENES_WF_WY_expe_added_2.txt") as file:
        while True:
            line = file.readline()
            if not line:
                break
            lijst = line.strip().split('\t')
            if line.strip().split('\t')[1] == 'NA':
                lijst[1] = None

            if line.strip().split('\t')[2] == 'NA':
                lijst[2] = None

            if line.strip().split('\t')[3] == 'NA':
                lijst[3] = None

            if line.strip().split('\t')[4] == 'NA':
                lijst[4] = None

            if line.strip().split('\t')[5] == 'NA':
                lijst[5] = None

            if line.strip().split('\t')[6] == 'NA':
                lijst[6] = None

            try:
                cluster_tumor[lijst[0]] = ['LSCC', genes_dict[lijst[0]][0],
                                            lijst[1], lijst[2],
                                            lijst[3], lijst[4],
                                            lijst[5], lijst[6]]
            except KeyError:
                pass

    with open("/DATA/Jasmine/LSCC/cluster_normal/GENES_WF_WY_expe_added.txt") as file:
        while True:
            line = file.readline()
            if not line:
                break

            lijst = line.strip().split('\t')
            if line.strip().split('\t')[1] == 'NA':
                lijst[1] = None

            if line.strip().split('\t')[2] == 'NA':
                lijst[2] = None

            if line.strip().split('\t')[3] == 'NA':
                lijst[3] = None

            if line.strip().split('\t')[4] == 'NA':
                lijst[4] = None

            if line.strip().split('\t')[5] == 'NA':
                lijst[5] = None

            if line.strip().split('\t')[6] == 'NA':
                lijst[6] = None

            try:
                cluster_normal[lijst[0]] = ['LSCC', genes_dict[lijst[0]][0],
                                            lijst[1], lijst[2],
                                            lijst[3], lijst[4],
                                            lijst[5], lijst[6]]
            except KeyError:
                pass
    return cancer_dict, sample_dict, counts_dict, genes_exp_dict, \
           new_genes_dict, cluster_normal, cluster_tumor


def wegschrijven(cursor, connection, cancer_dict, sample_dict, counts_dict,
                 genes_exp_dict, genes_dict, cluster_normal, cluster_tumor):
    """
    Loops through dictionary and creates the insert commands for the
    corresponding table. Data in the dictionary will also be inserted in this
    loop with cursor.execute(sql, ...).

    :param cursor: a variable to communicate with the database.
    :param connection: a variable to communicate with the database.
    :param cancer_dict: Dictionary with data to insert in CANCER table
    :param sample_dict: Dictionary with data to insert in SAMPLE table
    :param counts_dict: Dictionary with data to insert in COUNTS table
    :param genes_exp_dict: Dictionary with data to insert in GENE_EXP table
    :param genes_dict: Dictionary with data to insert in GENES table
    :param cluster_normal: Dictionary with data to insert in CLUSTER_NORMAL
    table
    :param cluster_tumor: Dictionary with data to insert in CLUSTER_TUMOR
    table
    :return: N/A
    """

    sql = """
    INSERT INTO CANCER VALUES (%s, %s);
    """
    for i in cancer_dict:
        cursor.execute(sql, cancer_dict[i])
        print(cancer_dict[i])

    sql = """
    INSERT INTO SAMPLE VALUES (%s, %s, %s, %s);
    """
    for j in sample_dict:
        cursor.execute(sql, sample_dict[j])
        print(sample_dict[j])

    sql = """
        INSERT INTO GENES VALUES (%s, %s);
        """
    for i in genes_dict:
        cursor.execute(sql, genes_dict[i])
        print(genes_dict[i])

    sql = """
    INSERT INTO GENE_EXP VALUES (%s, %s, %s);
    """
    for k in genes_exp_dict:
        cursor.execute(sql, genes_exp_dict[k])
        print(genes_exp_dict[k])


    sql = """
    INSERT INTO COUNTS VALUES (%s, %s, %s)
    """
    for i in counts_dict:
        cursor.execute(sql, counts_dict[i])
        print(counts_dict[i])

    sql = """
        INSERT INTO CLUSTER_NORMAL VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
    for j in cluster_normal:
        cursor.execute(sql, cluster_normal[j])
        print(cluster_normal[j])

    sql = """
        INSERT INTO CLUSTER_TUMOR VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
    for j in cluster_tumor:
        cursor.execute(sql, cluster_tumor[j])
        print(cluster_tumor[j])

    print("Done")
    connection.commit()


def main():
    """
    Opens connection with the database. Function databasemaken(...) creates the
    database. This function won't be called when the database already exists.
    Function dictionaries()
    :return: N/A
    """
    connection = database.connect(
        user="agami-admin",
        password="XMCpw9F5",
        host="localhost",
        database="substitutions")

    cursor = connection.cursor()
    print("Connected!\n")
    #databasemaken(cursor, connection)
    cancer_dict, sample_dict, counts_dict, genes_exp_dict, genes_dict, \
    cluster_normal, cluster_tumor = dictionaries()
    wegschrijven(cursor, connection, cancer_dict, sample_dict, counts_dict,
                 genes_exp_dict, genes_dict,
                 cluster_normal, cluster_tumor)
    connection.close()


main()
