from argparse import ArgumentParser

def solver():
    print("hello world")
    return 1

def main(args):
    solver()
    return


print("oups")

if __name__ == "__main__":
    
    parser = ArgumentParser()
    parser.add_argument("-p", "--pdf", help = "Chemin du pdf d'origine.")
    parser.add_argument("-d", "--df_csv_raw", help = "DataFrame brut")
    parser.add_argument("-b", "--bloc", help = "0 pour MLE. 1, 2 pour DPM. 3 pour DA/DS. 4 Pour DE)")
    args = parser.parse_args()

    main(args)

print("test")