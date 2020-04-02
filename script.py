from Bio import Entrez,SeqIO
import sys, argparse, os

def main(argv):
    parser = argparse.ArgumentParser(description='Set email and max amount of results')
    parser.add_argument('-e',dest='email',default='',help='email')
    parser.add_argument('-r',dest='retmax',default='100000',help='retmax')
    parser.add_argument('-o',dest='out',default='',help='output dir')
    args = parser.parse_args()
    filter = "severe+acute+respiratory+syndrome+coronavirus+2"
    Entrez.email = args.email
    handle = Entrez.esearch(db='Nucleotide', retmax=args.retmax, term=filter, idtype="acc")
    record = Entrez.read(handle)
    handle.close()

    def writeDataToFiles(recordId):
        handle = Entrez.efetch(db="Nucleotide", id=recordId, rettype="gb", retmode="text")
        record = SeqIO.read(handle, "genbank")

        outSeq = os.path.join(str(args.out) + "/","sequence_{}.txt".format(recordId)) if args.out else "sequence_{}.txt".format(recordId)
        with open(outSeq,"w") as out_seq:
            for line in record.seq:
                out_seq.write(line)

        gb_features = record.features
        feats = [feat for feat in gb_features if feat.type == "CDS"]
        outFeat = os.path.join(str(args.out) + "/","features_{}.txt".format(recordId)) if args.out else "features_{}.txt".format(recordId)
        with open(outFeat,"w") as out_handle:
            for feat in feats:
                feature_str = " ".join(['type:'+str(feat.type),'location:'+str(feat.location)])
                qual_str = " ".join(["{}:{}".format(k, v) for k, v in feat.qualifiers.items() if k != "translation"])
                translation_str = feat.qualifiers["translation"][0]
                out_handle.write(">" + recordId + " " + feature_str + " " + qual_str + "\n" + translation_str + "\n")
        handle.close()

    for r in record['IdList']:
        writeDataToFiles(r)

if __name__ == "__main__":
   main(sys.argv[1:])
