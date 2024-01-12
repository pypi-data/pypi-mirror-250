import datetime

def je_streda():
    today = datetime.datetime.now()

    if today.weekday() == 2:
        print("Ano")
    else:
        print("Ne")

