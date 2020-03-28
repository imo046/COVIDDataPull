from Bio import Entrez,SeqIO
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

    def writeSeqAndFeatures(recordId):
        handle = Entrez.efetch(db="Nucleotide", id=recordId, rettype="gb", retmode="text")
        record = SeqIO.read(handle, "genbank")
        with open("sequence_{}.txt".format(recordId),"w") as out_seq:
            for line in record.seq:
                out_seq.write(line)
        gb_features = record.features
        feats = [feat for feat in gb_features if feat.type == "CDS"]
        with open("features_{}.txt".format(recordId),"w") as out_handle:
            for feat in feats:
                seq_string = 'type:' + str(feat.type) + '\n' + 'location:' + str(feat.location) + '\n'
                qual_string = "\n".join(["{}:{}".format(k, v) for k, v in feat.qualifiers.items()])
                out_handle.write(seq_string + qual_string)
        handle.close()

    for r in record['IdList']:
        writeSeqAndFeatures(r)

if __name__ == "__main__":
   main(sys.argv[1:])
