from Bio import Entrez
import sys, argparse

def main(argv):
    parser = argparse.ArgumentParser(description='Set email and max amount of results')
    parser.add_argument('-e',dest='email',default='',help='email')
    parser.add_argument('-r',dest='retmax',default='',help='retmax')
    args = parser.parse_args()
    filter = "severe+acute+respiratory+syndrome+coronavirus+2"
    Entrez.email = args.email
    handle = Entrez.esearch(db='Nucleotide', retmax=args.retmax, term=filter, idtype="acc")
    record = Entrez.read(handle)
    handle.close()

    def wrireResult(recordId):
        handle = Entrez.efetch(db="Nucleotide", id=recordId, rettype="gb", retmode="text")
        out_handle = open("record_{}".format(recordId), "w")
        for line in handle:
            out_handle.write(line)
        out_handle.close()
        handle.close()

    for r in record['IdList']:
        wrireResult(r)

if __name__ == "__main__":
   main(sys.argv[1:])
 
