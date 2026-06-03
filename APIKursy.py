import tkinter as tk
from tkinter import messagebox
import threading
import requests

WALUTY = {
    "eur": ("Euro",                  "EUR"),
    "usd": ("Dolar Amerykański",     "USD"),
    "czk": ("Korona czeska",         "CZK"),
    "sbd": ("Dolar Wysp Salomona",   "SBD"),
    "sek": ("Korona szwedzka",       "SEK"),
    "lkr": ("Rupia lankijska",       "LKR"),
    "jpy": ("Jen",                   "JPY"),
    "pen": ("Sol peruwiański",       "PEN"),
}
API_URL = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/pln.json"

kursy = {}

def pobierz_kursy():
    status_var.set("Pobieranie kursów...")
    btn_przelicz.config(state="disabled")
    def fetch():
        try:
            r = requests.get(API_URL, timeout=10)
            r.raise_for_status()
            data = r.json().get("pln", {})
            root.after(0, lambda: on_ok(data))
        except Exception as e:
            root.after(0, lambda: on_err(str(e)))
    threading.Thread(target=fetch, daemon=True).start()

def on_ok(data):
    kursy.update(data)
    status_var.set("✔ Kursy pobrane")
    btn_przelicz.config(state="normal")

def on_err(msg):
    status_var.set("✗ Błąd pobierania")
    messagebox.showerror("Błąd", f"Nie udało się pobrać kursów:\n{msg}")

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
        kurs = kursy.get(kod)
        sym = WALUTY[kod][1]
        var.set(f"{kwota * kurs:.4f} {sym}" if kurs else "N/A")

root = tk.Tk()
root.title("Konwerter PLN - API")

status_var = tk.StringVar(value="-")
tk.Label(root, textvariable=status_var).grid(row=0, column=0, columnspan=3, pady=6)

tk.Label(root, text="Kwota w PLN:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
entry = tk.Entry(root, width=20)
entry.grid(row=1, column=1, padx=10, pady=10)
entry.bind("<Return>", lambda _: przelicz())

btn_przelicz = tk.Button(root, text="Przelicz", command=przelicz, state="disabled")
btn_przelicz.grid(row=1, column=2, padx=4)
tk.Button(root, text="Odśwież kursy", command=pobierz_kursy).grid(row=1, column=3, padx=4)

wyniki = {}
for i, (kod, (nazwa, sym)) in enumerate(WALUTY.items()):
    tk.Label(root, text=f"{sym} – {nazwa}:").grid(row=i+2, column=0, padx=10, pady=4, sticky="w")
    var = tk.StringVar(value="-")
    wyniki[kod] = var
    tk.Label(root, textvariable=var, width=20, anchor="w").grid(row=i+2, column=1, padx=10)

pobierz_kursy()
root.mainloop()