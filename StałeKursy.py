import tkinter as tk
from tkinter import  messagebox


class Waluta:
    def __init__(self, kod: str, nazwa: str, kurs: float):
        self.kod = kod
        self.nazwa = nazwa
        self.kurs = kurs

    def przelicz(self, kwota_pln: float) -> float:
        return kwota_pln * self.kurs

    def __str__(self):
        return f"{self.kod} - {self.nazwa} (kurs: {self.kurs})"


class KonwerterPLN(tk.Tk):

    WALUTY = [
        Waluta("EUR", "Euro", 0.2330),
        Waluta("USD", "Dolar Amerykański", 0.2463),
        Waluta("CZK", "Korona czeska", 5.7840),
        Waluta("SBD", "Dolar Wysp Salomona", 0.8821),
        Waluta("SEK", "Korona szwedzka", 2.5310),
        Waluta("LKR", "Rupia lankijska", 73.4500),
        Waluta("JPY", "Jen", 37.1200),
        Waluta("PEN", "Sol peruwiański", 0.9120),
    ]

    def __init__(self):
        super().__init__()

        self.title("Konwerter PLN")
        self.resizable(False, False)
        self.configure(bg="#eef2f7")
        self._zmienne: dict[str, tk.StringVar] = {}
        self._zbuduj_interfejs()


    def _zbuduj_interfejs(self):

        tk.Label(
            self,
            text=" Kantor Walut",
            font=("Arial", 18, "bold")
        ).pack(pady=(15, 10))

        ramka_gorna = tk.Frame(self,pady=10, padx=10)
        ramka_gorna.pack(fill="x")

        tk.Label(ramka_gorna, text="Kwota w PLN:").grid(row=0, column=0, sticky="w")
        self._entry = tk.Entry(ramka_gorna, width=20)
        self._entry.grid(row=0, column=1, padx=8)
        self._entry.bind("<Return>", lambda _: self.przelicz())
        self._entry.focus()

        tk.Button(ramka_gorna,text="Przelicz",command=self.przelicz).grid(row=0, column=2, padx=5)

        tk.Button(ramka_gorna,text="Wyczyść",command=self.wyczysc).grid(row=0, column=3)

        ramka_wyniki = tk.LabelFrame(self,text="Wyniki przeliczeń",padx=10, pady=5)
        ramka_wyniki.pack(fill="x")

        for i, waluta in enumerate(self.WALUTY):

            tk.Label(ramka_wyniki,text=f"{waluta.kod} - {waluta.nazwa} ({waluta.kurs})").grid(row=i,column=0,sticky="w",pady=4)
            zmienna = tk.StringVar(value="-")
            self._zmienne[waluta.kod] = zmienna
            tk.Label(ramka_wyniki,textvariable=zmienna,font=("Consolas", 11, "bold"),fg="darkgreen",width=20,anchor="w").grid(row=i,column=1,padx=10)

    def _pobierz_kwote(self) -> float | None:
        raw = self._entry.get().strip().replace(",", ".")
        if not raw:
            messagebox.showwarning("Błąd", "Podaj kwotę w PLN.")
            return None
        try:
            kwota = float(raw)
            if kwota < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Błąd", "Podaj poprawną, nieujemną liczbę.")
            return None
        return kwota

    def przelicz(self):
        kwota = self._pobierz_kwote()
        if kwota is None:
            return
        for waluta in self.WALUTY:
            wynik = waluta.przelicz(kwota)
            self._zmienne[waluta.kod].set(f"{wynik:.4f} {waluta.kod}")

    def wyczysc(self):
        self._entry.delete(0, tk.END)
        for zmienna in self._zmienne.values():
            zmienna.set("-")
        self._entry.focus()


if __name__ == "__main__":
    app = KonwerterPLN()
    app.mainloop()