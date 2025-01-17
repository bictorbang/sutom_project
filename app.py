from argparse import ArgumentParser

def solver():
    return

def main(args):
    solver(my_pdf = args.pdf, df_csv_raw = args.df_csv_raw, bloc = args.bloc)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-p", "--pdf", help = "Chemin du pdf d'origine.")
    parser.add_argument("-d", "--df_csv_raw", help = "DataFrame brut")
    parser.add_argument("-b", "--bloc", help = "0 pour MLE. 1, 2 pour DPM. 3 pour DA/DS. 4 Pour DE)")
    args = parser.parse_args()
    main(args)