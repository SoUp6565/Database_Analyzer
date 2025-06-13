
import io
import pyodbc
import requests
import pandas as pd
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

# *** -> private datas, es: tables


# Parametri
server = 'YOUR SERVER'  # Es: 192.168.1.100\SQLEXPRESS
database = 'YOUR DATABASE'
username = 'YOUR USERNAME'
password = 'YOUR PWD'

# Stringa di connessione formattata

connect_string = ("DRIVER=ODBC Driver 18 for SQL Server;" +
                  "SERVER=" + server + ";" +
                  "DATABASE=" + database + ";" +
                  "UID=" + username + ";" +
                  "PWD=" + password + ";" +
                  "TrustServerCertificate=yes;" +
                  "MARS_Connection=yes;" +
                  "Pooling=no;"

                  )


def connection_creator():
    conn = pyodbc.connect(connect_string)
    return conn


def cursor_generator(conn):
    return conn.cursor()


def database_description(cursor):
    cursor.execute("SELECT * FROM ***")
    print("Campi nella tabella:")
    for column in cursor.description:
        print("-", column[0])

def print_text_from_bank():

    date = input("inserisci una data formato (YYYY-MM-DD): ")

    url = (
        # "https://tassidicambio.bancaditalia.it/terzevalute-wf-web/rest/v1.0/latestRates?lang="
        # "https://tassidicambio.bancaditalia.it/terzevalute-wf-web/rest/v1.0/QueryOneDateAllCur?lang=ita&rate=0&initDay=" + "04" + "&initMonth=" + "06" + "&initYear=2025" + "&refCur=euro&R1=csv"
        # "https://tassidicambio.bancaditalia.it/terzevalute-wf-web/rest/v1.0/rates/2024-06-04?lang=it"
        "https://tassidicambio.bancaditalia.it/terzevalute-wf-web/rest/v1.0/dailyRates?referenceDate="+date+"&currencyIsoCode=EUR&lang=it"
    )

    response = requests.get(url)
    if response.status_code == 200:
        contenuto_csv = response.text
        print(contenuto_csv)


def get_bank_info(cursor, conn):
    url = (
        #"https://tassidicambio.bancaditalia.it/terzevalute-wf-web/rest/v1.0/latestRates?lang="
        #"https://tassidicambio.bancaditalia.it/terzevalute-wf-web/rest/v1.0/QueryOneDateAllCur?lang=ita&rate=0&initDay=" + "04" + "&initMonth=" + "06" + "&initYear=2025" + "&refCur=euro&R1=csv"
        #"https://tassidicambio.bancaditalia.it/terzevalute-wf-web/rest/v1.0/rates/2024-06-04?lang=it"
        "https://tassidicambio.bancaditalia.it/terzevalute-wf-web/rest/v1.0/dailyRates?referenceDate=2025-06-04&currencyIsoCode=EUR&lang=it"
    )

    response = requests.get(url)
    if response.status_code == 200:
        contenuto_csv = response.text

        #print(contenuto_csv)

        df = pd.read_csv(io.StringIO(contenuto_csv))

        usa_row = df[df["Codice ISO"] == "USD"]

        value = float(usa_row["Quotazione"].iloc[0])
        date = usa_row[" Data di riferimento (CET)"].iloc[0]

        write_on_database(cursor, conn, date, value)

    else:
        print(" Errore nella richiesta:", response.status_code)

def find_row_using_iso():

    line = input("inserisci il codice ISO di cui vuoi trovare le sue informazioni: ")

    url = (
        # "https://tassidicambio.bancaditalia.it/terzevalute-wf-web/rest/v1.0/latestRates?lang="
        # "https://tassidicambio.bancaditalia.it/terzevalute-wf-web/rest/v1.0/QueryOneDateAllCur?lang=ita&rate=0&initDay=" + "04" + "&initMonth=" + "06" + "&initYear=2025" + "&refCur=euro&R1=csv"
        # "https://tassidicambio.bancaditalia.it/terzevalute-wf-web/rest/v1.0/rates/2024-06-04?lang=it"
        "https://tassidicambio.bancaditalia.it/terzevalute-wf-web/rest/v1.0/dailyRates?referenceDate=2025-06-04&currencyIsoCode=EUR&lang=it"
    )

    response = requests.get(url)
    if response.status_code == 200:
        contenuto_csv = response.text

        df = pd.read_csv(io.StringIO(contenuto_csv))

        print(df[df["Codice ISO" == line]])

def find_row_using_country():

    line = input("inserisci il codice ISO di cui vuoi trovare le sue informazioni: ")

    url = (
        # "https://tassidicambio.bancaditalia.it/terzevalute-wf-web/rest/v1.0/latestRates?lang="
        # "https://tassidicambio.bancaditalia.it/terzevalute-wf-web/rest/v1.0/QueryOneDateAllCur?lang=ita&rate=0&initDay=" + "04" + "&initMonth=" + "06" + "&initYear=2025" + "&refCur=euro&R1=csv"
        # "https://tassidicambio.bancaditalia.it/terzevalute-wf-web/rest/v1.0/rates/2024-06-04?lang=it"
        "https://tassidicambio.bancaditalia.it/terzevalute-wf-web/rest/v1.0/dailyRates?referenceDate=2025-06-04&currencyIsoCode=EUR&lang=it"
    )

    response = requests.get(url)
    if response.status_code == 200:
        contenuto_csv = response.text

        df = pd.read_csv(io.StringIO(contenuto_csv))

        print(df[df["Paese" == line]])


def write_on_database(cursor, conn, date, value):
    cursor.execute("INSERT INTO *** VALUES (?, ?, ?)", (date, 'CAD', value))
    conn.commit()
    print("Riga inserita.")


def read_on_database(cursor):
    cursor.execute("SELECT * FROM ***")
    rows = cursor.fetchall()
    print("Contenuto della tabella:")
    for row in rows:
        print(row)


def print_graphic(cursor):
    dates = []
    values = []

    code = input("inserisci il codice di cui vuoi adare ad analizzare il grafico, es: (USD, EUR,ecc..)--->")

    cursor.execute("SELECT * FROM *** ")
    rows = cursor.fetchall()

    for row in rows:
        if row[1] == code:
            data_str = row[0].strftime("%Y-%m-%d")
            dates.append(data_str)
            values.append(row[2])


    plt.figure(figsize = (25, 10))
    plt.plot(dates, values, linestyle='-')


    ticks_to_show = [dates[0], dates[len(dates) // 2], dates[-1]]
    plt.xticks(ticks_to_show)

    plt.xlabel("Date")
    plt.ylabel("Valori")
    plt.title("Grafico Valute")
    plt.grid(True)
    plt.savefig("grafico_valute.png")
    print("Grafico salvato come 'grafico_valute.png'")


def delete_on_database(cursor, conn):
    key1 = input("Inserisci la data (YYYY-MM-DD) della riga da eliminare: ")
    key2 = input("Inserisci il valore da eliminare (attenzione: deve combaciare): ")
    cursor.execute("DELETE FROM *** WHERE VAL_DATE = ? AND VAL_VALUE = ?", (key1, key2))
    conn.commit()
    print("Riga eliminata (se trovata).")


def delete_all(cursor, conn):
    cursor.execute("DELETE FROM ***")
    conn.commit()


def close_connection(conn):
    conn.close()
    print("onnessione chiusa.")


# === Menu interattivo ===
def menu():
    conn = connection_creator()
    cursor = cursor_generator(conn)

    while True:
        print("\n========== MENU ==========")
        print("1. Visualizza struttura tabella")
        print("2. Leggi tutto il contenuto")
        print("3. Elimina una riga")
        print("4. Elimina tutto")
        print("5. Mostra Grafico")
        print("6. Mostra testo")
        print("7. Esci")
        print("==========================")

        scelta = input("Scegli un'opzione (1-7): ")

        if scelta == "1":
            database_description(cursor)
        elif scelta == "2":
            read_on_database(cursor)
        elif scelta == "3":
            delete_on_database(cursor, conn)
        elif scelta == "4":
            delete_all(cursor, conn)
        elif scelta == "5":
            print_graphic(cursor)
        elif scelta == "6":
            print_text_from_bank()
        elif scelta == "7":
            break
        else:
            print("Scelta non valida. Riprova.")

    close_connection(conn)


if __name__ == "__main__":
    menu()
