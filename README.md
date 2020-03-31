# COVIDDataPull
Description:

Python script for pulling the sequence data from the National Center for Biotechnology Information (NCBI) database 
based on filter "severe+acute+respiratory+syndrome+coronavirus+2" using Entrez Programming Utilities.

For each entry, it creates two files: one with the actual sequence and another with the features data, including qualifiers. 

Use:
script.py -e "email" -r "retmax"

Email is the email address of the E-utility user, it is optional, however, it is recommended to use a valid email.

Retmax parameter sets the maximum amount of entries to be processed, if not set, the first 20 entries found 
based on the filtering would be processed.
