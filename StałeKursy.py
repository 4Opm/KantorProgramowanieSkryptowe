import tkinter as tk
from tkinter import messagebox

KURSY = {
    "EUR": ("Euro",                  0.2330),
    "USD": ("Dolar Amerykański",     0.2463),
    "CZK": ("Korona czeska",         5.7840),
    "SBD": ("Dolar Wysp Salomona",   0.8821),
    "SEK": ("Korona szwedzka",       2.5310),
    "LKR": ("Rupia lankijska",      73.4500),
    "JPY": ("Jen",                  37.1200),
    "PEN": ("Sol peruwiański",       0.9120),
}

def przelicz():
    raw = entry.get().strip().replace(",", ".")
    if not raw:
        messagebox.showwarning("Błąd", "Podaj kwotę w PLN.")
        return
    try:
        kwota = float(raw)
        if kwota < 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Błąd", "Podaj poprawną, nieujemną liczbę.")
        return

    for kod, var in wyniki.items():
        kurs = KURSY[kod][1]
        var.set(f"{kwota * kurs:.4f} {kod}")

root = tk.Tk()
root.title("Konwerter PLN - stałe kursy")

tk.Label(root, text="Kwota w PLN:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry = tk.Entry(root, width=20)
entry.grid(row=0, column=1, padx=10, pady=10)
entry.bind("<Return>", lambda _: przelicz())

tk.Button(root, text="Przelicz", command=przelicz).grid(row=0, column=2, padx=10)

wyniki = {}
for i, (kod, (nazwa, _)) in enumerate(KURSY.items()):
    tk.Label(root, text=f"{kod} – {nazwa}:").grid(row=i+1, column=0, padx=10, pady=4, sticky="w")
    var = tk.StringVar(value="-")
    wyniki[kod] = var
    tk.Label(root, textvariable=var, width=20, anchor="w").grid(row=i+1, column=1, padx=10)

root.mainloop()