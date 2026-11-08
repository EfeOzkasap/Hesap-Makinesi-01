import sys
import customtkinter as ctk
import re
import json
from pathlib import Path

ctk.set_appearance_mode("dark")

pencere = ctk.CTk()
def kaynak_yolu(dosya):
    if hasattr(sys, "_MEIPASS"):
        return str(Path(sys._MEIPASS) / dosya)
    return str(Path(__file__).parent / dosya)

pencere.iconbitmap(kaynak_yolu("hesap_makinesi.ico"))
pencere.title("Modern Calculator")
pencere.geometry("380x720")
pencere.resizable(False, False)
pencere.configure(fg_color="#151515")

ifade = ""
gecmis = []

DOSYA = Path(__file__).with_name("gecmis.json")


# KAYITLI GEÇMİŞİ YÜKLE
def gecmisi_yukle():
    try:
        with open(DOSYA, "r", encoding="utf-8") as dosya:
            veriler = json.load(dosya)
            if isinstance(veriler, list):
                return veriler
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    return []


gecmis = gecmisi_yukle()


# GEÇMİŞİ KAYDET
def gecmisi_kaydet():
    with open(DOSYA, "w", encoding="utf-8") as dosya:
        json.dump(gecmis, dosya, ensure_ascii=False, indent=4)


# EKRANI GÜNCELLE
def guncelle():
    gorunen = ifade.replace("*", "×").replace("/", "÷")
    ekran.configure(text=gorunen if gorunen else "0")


# GEÇMİŞTEKİ İŞLEME TIKLAMA
def islemi_yukle(index):
    global ifade

    secilen = gecmis[index]

    # "25 + 30 = 55" içinden işlemi al
    ifade = secilen.split(" = ")[0]

    guncelle()


# GEÇMİŞİ GÜNCELLE
def gecmisi_guncelle():
    for widget in gecmis_alan.winfo_children():
        widget.destroy()

    for index in range(len(gecmis) - 1, -1, -1):

        kayit = gecmis[index]

        buton = ctk.CTkButton(
            gecmis_alan,
            text=kayit,
            anchor="w",
            fg_color="#292929",
            hover_color="#454545",
            text_color="white",
            font=("Arial", 13),
            corner_radius=8,
            height=35,
            command=lambda i=index: islemi_yukle(i)
        )

        buton.pack(fill="x", padx=5, pady=3)


# GEÇMİŞİ TEMİZLE
def gecmisi_temizle():
    gecmis.clear()
    gecmisi_kaydet()
    gecmisi_guncelle()


# HESAPLAMA
def hesapla():
    global ifade

    try:
        if not ifade:
            return

        if not re.fullmatch(r"[0-9+\-*/(). ]+", ifade):
            raise ValueError

        eski_ifade = ifade
        sonuc = eval(ifade, {"__builtins__": None}, {})

        gorunen = eski_ifade.replace("*", "×").replace("/", "÷")

        gecmis.append(f"{gorunen} = {sonuc}")

        gecmisi_kaydet()
        gecmisi_guncelle()

        ifade = str(sonuc)
        guncelle()

    except ZeroDivisionError:
        ekran.configure(text="Sıfıra bölünemez")
        ifade = ""

    except:
        ekran.configure(text="Hatalı işlem")
        ifade = ""


# TUŞ İŞLEMLERİ
def tus_bas(deger):
    global ifade

    if deger == "C":
        ifade = ""

    elif deger == "⌫":
        ifade = ifade[:-1]

    elif deger == "=":
        hesapla()
        return

    elif deger == "%":
        ifade += "/100"

    else:
        ifade += deger

    guncelle()


# KLAVYE
def klavye(event):
    tus = event.keysym
    karakter = event.char

    if tus in ("Return", "KP_Enter"):
        hesapla()

    elif tus == "BackSpace":
        tus_bas("⌫")

    elif tus in ("Escape", "Delete"):
        tus_bas("C")

    elif karakter in "0123456789+-*/().":
        tus_bas(karakter)

    elif karakter == "%":
        tus_bas("%")

    elif karakter == ",":
        tus_bas(".")

    return "break"


# BAŞLIK
baslik = ctk.CTkLabel(
    pencere,
    text="CALCULATOR",
    font=("Arial", 18, "bold"),
    text_color="#A78BFA"
)
baslik.pack(pady=(20, 10))


# SONUÇ EKRANI
ekran = ctk.CTkLabel(
    pencere,
    text="0",
    font=("Arial", 38, "bold"),
    text_color="white",
    anchor="e"
)
ekran.pack(fill="x", padx=20, pady=20)


# TUŞLAR
alan = ctk.CTkFrame(pencere, fg_color="transparent")
alan.pack(fill="both", expand=True, padx=12, pady=5)

butonlar = [
    ["C", "⌫", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["00", "0", ".", "="]
]

for satir_no, satir in enumerate(butonlar):
    for sutun_no, deger in enumerate(satir):

        renk = "#292929"
        hover = "#414141"

        if deger in ["÷", "×", "-", "+", "="]:
            renk = "#7048C8"
            hover = "#8963DF"

        elif deger == "C":
            renk = "#A13C55"
            hover = "#C04D69"

        komut = (
            "/" if deger == "÷" else
            "*" if deger == "×" else
            deger
        )

        buton = ctk.CTkButton(
            alan,
            text=deger,
            font=("Arial", 18, "bold"),
            fg_color=renk,
            hover_color=hover,
            corner_radius=12,
            height=55,
            command=lambda x=komut: tus_bas(x)
        )

        buton.grid(
            row=satir_no,
            column=sutun_no,
            padx=4,
            pady=4,
            sticky="nsew"
        )

for i in range(5):
    alan.rowconfigure(i, weight=1)

for i in range(4):
    alan.columnconfigure(i, weight=1)


# İŞLEM GEÇMİŞİ BAŞLIĞI
gecmis_baslik = ctk.CTkLabel(
    pencere,
    text="İŞLEM GEÇMİŞİ  •  İşleme tıkla",
    font=("Arial", 14, "bold"),
    text_color="#A78BFA"
)
gecmis_baslik.pack(pady=(12, 5))


# GEÇMİŞ LİSTESİ
gecmis_alan = ctk.CTkScrollableFrame(
    pencere,
    height=110,
    fg_color="#202020",
    corner_radius=10
)
gecmis_alan.pack(fill="x", padx=15, pady=5)


# GEÇMİŞİ TEMİZLE
temizle = ctk.CTkButton(
    pencere,
    text="Geçmişi Temizle",
    fg_color="#A13C55",
    hover_color="#C04D69",
    height=35,
    corner_radius=10,
    command=gecmisi_temizle
)
temizle.pack(fill="x", padx=15, pady=(5, 15))


# ESKİ KAYITLARI GÖSTER
gecmisi_guncelle()

pencere.bind("<Key>", klavye)

pencere.mainloop()
