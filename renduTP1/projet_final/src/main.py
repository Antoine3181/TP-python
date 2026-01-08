from utils.io import nettoyer_csv, collecter_erreurs


def main():
    print("Clean du CSV...")
    nettoyer_csv()

    print("Check des erreurs dans les logs...")
    collecter_erreurs()

    print("Script fini...")


if __name__ == "__main__":
    main()
