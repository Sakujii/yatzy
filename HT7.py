""" TIE-02100 Johdatus ohjelmointiin S2015      Saku Jussila 14.12.2015

    Opiskelijanumero: 240184, Sähköposti: saku.jussila@student.tut.fi

    Ohjelmointitehtävä T7
    Kahden pelaajan Yatzy

Säännöt:
        Kaksi pelaajaa heittää omalla vuorollaan viittä noppaa.
        Yhdellä pelivuorolla pelaajalla on kolme heittoa. Noppia voi heittojen
        välillä lukita, ja lukituksia saa vaihtaa. Kolmannen heiton jälkeen
        pelaajan tulee valita, mihin pistesarakkeeseen haluaa heittämänsä
        pisteet syöttää. Vaihtoehtoisesti pisteet voi syöttää aiemminkin, vaikka
        jo ensimmäisen heiton jälkeen. Pelaajat heittävät vuorotellen kunnes
        kaikki pistesarakkeet on täytetty. Jo täytettyä pistesaraketta ei voi
        muuttaa, vaikka sattuisikin saamaan paremmat pisteet kyseiseen kohtaan.

Pistelasku:
        Noppien järjestyksellä ei ole merkitystä.

        Ykköset: laskee 1-silmäluvut yhteen
        Kakkoset: laskee 2-silmäluvut yhteen
        Kolmoset: laskee 3-silmäluvut yhteen
        Neloset: laskee 4-silmäluvut yhteen
        Vitoset: laskee 5-silmäluvut yhteen
        Kutoset: laskee 6-silmäluvut yhteen
        Tässä vaiheessa lasketaan välisumma. Jos pelaaja saa ym. kohdista
        yhteensä 63 pistettä (heittämällä kolme osumaa jokaista numeroa)
        tai enemmän, saa hän 50 pisteen bonuksen. Bonus ilmaantuu bonus-
        sarakkeen lisäksi myös alimpana olevaan yhteispiste-sarakkeeseen.

        Pari: kaksi samaa silmälukua        esim. 1-3-4-6-6 = 12 pistettä
        Kaksi paria: kaksi eri paria        esim. 1-5-5-4-4 = 18 pistettä
        Kolmoset: kolme samaa silmälukua    esim. 1-6-6-6-2 = 9  pistettä
        Neloset: neljä samaa silmälukua     esim. 1-1-1-1-6 = 4  pistettä
        Täyskäsi: kolme samaa silmälukua ja eriävän silmäluvun pari
                                            esim.    555-22 = 19 pistettä
        Pieni suora: Silmäluvut 1-2-3-4-5,               aina 15 pistettä
        Iso suora: Silmäluvut 2-3-4-5-6,                 aina 20 pistettä
        Satumma: Mikä tahansa silmälukuyhdistelmä
                                            esim. 6-6-2-5-1 = 20 pistettä
        Yatzy: Viisi samaa silmälukua,                   aina 50 pistettä

        Pisteet: Pistesarakkeet summattu yhteen. Maksimipistemäärä on 374.
        """


from tkinter import *
from tkinter import messagebox
import random, time

nopan_kuvat = ["noppa1.gif", "noppa2.gif", "noppa3.gif", "noppa4.gif",
              "noppa5.gif", "noppa6.gif"]

pelaajien_lkm = 2
noppien_lkm = 5
heittovuorot = 3

otsikko = ("Helvetica", 18, "bold")
bold = ("Helvetica", 14, "bold")

class Yatzy:
    def __init__(self):
        self.__ikkuna = Tk()
        self.__ikkuna.title("Yatzy")

        self.__pelivuoro = 0

        self.__nopan_kuvat = []
        for tiedosto in nopan_kuvat:
            kuva = PhotoImage (file=tiedosto)
            self.__nopan_kuvat.append (kuva)

        self.__nopan_paikat = []
        for i in range (noppien_lkm):
            noppalabel = Label (self.__ikkuna)
            noppalabel.grid (row=12, rowspan=3, column=3+i, padx=5, pady=5)
            self.__nopan_paikat.append(noppalabel)

        self.__lukitusnappulat = []
        for i in range (noppien_lkm):
            lukitusnappula = Button (self.__ikkuna, text = "Lukitse",
                                    command=lambda x=i: self.lukitus(x))
            lukitusnappula.grid (row=11, column=3+i)
            self.__lukitusnappulat.append (lukitusnappula)

        self.__vuoro_teksti = Label (self.__ikkuna)
        self.__vuoro_teksti.grid (row=8, column=5)

        self.__heittonappula = Button (self.__ikkuna, text="Heitä nopat",
                                       font=otsikko, command=self.heitä)
        self.__heittonappula.grid (row=16, column=5)

        self.__pelaaja1 = Label (self.__ikkuna, text = "Pelaaja 1",
                                font=otsikko)
        self.__pelaaja1.grid (row=1, column=1, columnspan=2)
        self.__pelaaja1_välisumma = Label (self.__ikkuna, text = "Välisumma:",
                                          font=bold)
        self.__pelaaja1_välisumma.grid (row=8, column=1, sticky=W)
        self.__pelaaja1_bonus = Label (self.__ikkuna, text = "Bonus:",
                                      font=bold)
        self.__pelaaja1_bonus.grid (row=9, column=1, sticky=W)
        self.__pelaaja1_pisteet = Label (self.__ikkuna, text = "Pisteet:",
                                        font=bold)
        self.__pelaaja1_pisteet.grid (row=19, column=1, sticky=W)


        self.__pelaaja2 = Label (self.__ikkuna, text = "Pelaaja 2",
                                font=otsikko)
        self.__pelaaja2.grid (row=1, column=8, columnspan=2)
        self.__pelaaja2_välisumma = Label (self.__ikkuna, text = "Välisumma:",
                                          font=bold)
        self.__pelaaja2_välisumma.grid (row=8, column=8, sticky=W)
        self.__pelaaja2_bonus = Label (self.__ikkuna, text = "Bonus:",
                                      font=bold)
        self.__pelaaja2_bonus.grid (row=9, column=8, sticky=W)
        self.__pelaaja2_pisteet = Label (self.__ikkuna, text = "Pisteet:",
                                        font=bold)
        self.__pelaaja2_pisteet.grid (row=19, column=8, sticky=W)

        self.__pelaaja1_nappulat = []

        for i in range (6):
            pelaaja1_nappula = Button (self.__ikkuna,
                                      command=lambda x=i: self.pistelasku(x))
            pelaaja1_nappula.grid (row=i+2, column=1, sticky=W+E)
            self.__pelaaja1_nappulat.append (pelaaja1_nappula)
        i=8
        while i<=16:
            pelaaja1_nappula = Button (self.__ikkuna,
                                      command=lambda x=i: self.pistelasku(x))
            pelaaja1_nappula.grid (row=i+2, column=1, sticky=W+E)
            self.__pelaaja1_nappulat.append (pelaaja1_nappula)
            i+=1

        self.__pelaaja2_nappulat = []

        for i in range (6):
            pelaaja2_nappula = Button (self.__ikkuna,
                                      command=lambda x=i: self.pistelasku(x))
            pelaaja2_nappula.grid (row=i+2, column=8, sticky=W+E)
            self.__pelaaja2_nappulat.append (pelaaja2_nappula)
        i=8
        while i<=16:
            pelaaja2_nappula = Button (self.__ikkuna,
                                      command=lambda x=i: self.pistelasku(x))
            pelaaja2_nappula.grid (row=i+2, column=8, sticky=W+E)
            self.__pelaaja2_nappulat.append (pelaaja2_nappula)
            i+=1

        self.__pelaajien_nappulat = [self.__pelaaja1_nappulat,
                                     self.__pelaaja2_nappulat]

        self.__pelaaja1_syötteet = []
        for i in range (18):
            pelaaja1_syöte = Entry (self.__ikkuna)
            pelaaja1_syöte.grid (row=i+2, column=2)
            self.__pelaaja1_syötteet.append (pelaaja1_syöte)

        self.__pelaaja2_syötteet = []
        for i in range (18):
            pelaaja2_syöte = Entry (self.__ikkuna)
            pelaaja2_syöte.grid (row=i+2, column=9)
            self.__pelaaja2_syötteet.append (pelaaja2_syöte)

        uusi_peli_nappula = Button (self.__ikkuna, text="Uusi peli",
                            command=self.alusta)
        uusi_peli_nappula.grid (row=2, column=5, sticky=W+E+N)
        lopetusnappula = Button (self.__ikkuna, text="Lopeta",
                                command=self.__ikkuna.destroy)
        lopetusnappula.grid (row=3, column=5, sticky=W+E+S)

        self.alusta()
        self.__ikkuna.mainloop()



    def alusta(self):
        """Muuttaa pelin elementit alkutilaan."""


        for i in range (18):
            self.__pelaaja1_syötteet[i].delete(0, END)
            self.__pelaaja2_syötteet[i].delete(0, END)

        for pelaaja in self.__pelaajien_nappulat:
            pelaaja[0].configure(text = "Ykköset")
            pelaaja[1].configure(text = "Kakkoset")
            pelaaja[2].configure(text = "Kolmoset")
            pelaaja[3].configure(text = "Neloset")
            pelaaja[4].configure(text = "Vitoset")
            pelaaja[5].configure(text = "Kutoset")
            pelaaja[6].configure(text = "Pari")
            pelaaja[7].configure(text = "Kaksi paria")
            pelaaja[8].configure(text = "Kolme samaa")
            pelaaja[9].configure(text = "Neljä samaa")
            pelaaja[10].configure(text = "Täyskäsi")
            pelaaja[11].configure(text = "Pieni suora")
            pelaaja[12].configure(text = "Iso suora")
            pelaaja[13].configure(text = "Sattuma")
            pelaaja[14].configure(text = "Yatzy")


        self.__nopat_vapaana = [True]* noppien_lkm

        for noppakuva in self.__nopan_paikat:
            noppakuva.configure(image=self.__nopan_kuvat[0],
                                background="Black")

        self.nollaa_nappulat()

        self.__pelivuoro = 1
        self.__vuoro_teksti.configure(text="Pelaajan 1 vuoro", font=bold)

        self.__heitot = heittovuorot
        self.__pisteet = [0,0]

        self.__silmäluvut = [1] * noppien_lkm


    def heitä(self):
        """ Heittää nopat ja aukaisee tarvittavat nappulat ensimmäisen heiton
        jälkeen. Kun heitot ovat loppu, nappulat lukitaan seuraavaa pelaajaa
        varten."""

        self.__heitot -= 1
        for i in range(noppien_lkm):
            if self.__heitot==heittovuorot-1:
                for lukitusnappula in self.__lukitusnappulat:
                    lukitusnappula.configure(state=NORMAL)
                if self.__pelivuoro%2==0:
                    for pistenappula in self.__pelaaja2_nappulat:
                        pistenappula.configure(state=NORMAL)
                else:
                    for pistenappula in self.__pelaaja1_nappulat:
                        pistenappula.configure(state=NORMAL)

            if self.__nopat_vapaana[i]:
                for j in range(0, 10):
                    silmäluku = random.randint(1, 6)
                    self.__silmäluvut[i] = silmäluku
                    self.__nopan_paikat[i].configure\
                        (image=self.__nopan_kuvat[silmäluku - 1])
                    self.__ikkuna.update_idletasks()
                    time.sleep(0.05)

        if self.__heitot == 0:
            self.__heittonappula.configure(state=DISABLED)
            for lukitusnappula in self.__lukitusnappulat:
                lukitusnappula.configure(state=DISABLED)



    def pistelasku(self, indeksi):
        """Laskee pisteet riippuen siitä, mihin sarakkeeseen pelaaja haluaa
        pisteet syöttää.
        :param indeksi: painetun pistenappulan indeksi """


        tulos = 0
        silmäluvut = sorted(self.__silmäluvut)

        try:
            if 0 <= indeksi <= 5:
                for silmäluku in silmäluvut:
                    if indeksi+1 == silmäluku:
                        tulos += silmäluku

            elif indeksi==8:
                i=6
                while i>0:
                    samat = silmäluvut.count(i)
                    if samat >= 2:
                        tulos += i*2
                        break
                    i -= 1

            elif indeksi==9:
                laskuri=0
                for i in range (6):
                    samat = silmäluvut.count(i+1)
                    if samat >= 2:
                        laskuri += 1
                        tulos +=(i+1)*2
                if laskuri < 2:
                    tulos = 0

            elif indeksi==10:
                for i in range (6):
                    samat = silmäluvut.count(i+1)
                    if samat >= 3:
                        tulos += (i+1)*3

            elif indeksi==11:
                for i in range (6):
                    samat = silmäluvut.count(i+1)
                    if samat >= 4:
                        tulos += (i+1)*4

            elif indeksi==12:
                if silmäluvut[0]==silmäluvut[1]==silmäluvut[2] or \
                    silmäluvut[2]==silmäluvut[3]==silmäluvut[4]:
                    tulos += sum(self.__silmäluvut)

                for i in range (6):
                    samat = silmäluvut.count(i+1)
                    if samat>3:
                        tulos = 0

            elif indeksi==13:
                if silmäluvut[0]==1 and silmäluvut[1]==2 and silmäluvut[2]==3 \
                        and silmäluvut[3]==4 and silmäluvut[4]==5:
                    tulos += sum(self.__silmäluvut)

            elif indeksi==14:
                if silmäluvut[0]==2 and silmäluvut[1]==3 and silmäluvut[2]==4 \
                    and silmäluvut[3]==5 and silmäluvut[4]==6:
                    tulos += sum(self.__silmäluvut)

            elif indeksi==15:
                tulos += sum(self.__silmäluvut)

            elif indeksi==16:
                for i in range (6):
                    samat = silmäluvut.count(i+1)
                    if samat==5:
                        tulos = 50
                        pass

        except:
            pass


        if tulos==0:

            vastaus = messagebox.askquestion("Varoitus!", "Haluatko varmasti "
                  "syöttää sarakkeeseen nolla pistettä?")

            if vastaus == "yes":
                self.syötä_tulokset(indeksi, tulos)
                self.summat()
                self.vaihda_vuoro()
                self.tarkista_lopetus()
            else:
                pass

        else:
            self.syötä_tulokset(indeksi, tulos)
            self.summat()
            self.vaihda_vuoro()
            self.tarkista_lopetus()



    def syötä_tulokset(self, indeksi, tulos):
        """Syöttää tulokset oikeaan pistesarakkeeseen ja
        deaktivoi painetun nappulan."""

        if self.__pelivuoro%2==0:
            self.__pelaaja2_syötteet[indeksi].insert(0, tulos)
            if indeksi<6:
                self.__pelaaja2_nappulat[indeksi].configure(command=0)
            elif indeksi>5:
                self.__pelaaja2_nappulat[indeksi-2].configure(command=0)
        else:
            self.__pelaaja1_syötteet[indeksi].insert(0, tulos)
            if indeksi<6:
                self.__pelaaja1_nappulat[indeksi].configure(command=0)
            elif indeksi>5:
                self.__pelaaja1_nappulat[indeksi-2].configure(command=0)



    def summat(self):
        """Laskee ja syöttää välisummat, bonukset ja yhteispisteet."""

        bonus = 50
        välisumma1 = summa1 = välisumma2 = summa2 = 0

        if self.__pelivuoro%2 != 0:
            self.__pelaaja1_syötteet[17].delete(0, END)
            self.__pelaaja1_syötteet[6].delete(0, END)

            for i in range (17):
                try:
                    tulos = int(self.__pelaaja1_syötteet[i].get())

                    if i<6:
                        välisumma1 += tulos

                    summa1 += tulos

                except ValueError:
                    continue

            if välisumma1 >= 63 and not self.__pelaaja1_syötteet[7].get():
                self.__pelaaja1_syötteet[7].insert(0, bonus)
                summa1 += bonus
            if välisumma1 > 0:
                self.__pelaaja1_syötteet[6].insert(0, välisumma1)
            if summa1 >0:
                self.__pelaaja1_syötteet[17].insert(0, summa1)

        else:
            self.__pelaaja2_syötteet[17].delete(0, END)
            self.__pelaaja2_syötteet[6].delete(0, END)

            for i in range (17):
                try:
                    tulos = int(self.__pelaaja2_syötteet[i].get())

                    if i<6:
                        välisumma2 += tulos

                    summa2 += tulos

                except ValueError:
                    continue

            if välisumma2 >= 63 and not self.__pelaaja2_syötteet[7].get():
                self.__pelaaja2_syötteet[7].insert(0, bonus)
                summa2 += bonus
            if välisumma2 > 0:
                self.__pelaaja2_syötteet[6].insert(0, välisumma2)
            if summa2 > 0:
                self.__pelaaja2_syötteet[17].insert(0, summa2)



    def nollaa_nappulat(self):
        """Asettaa lukitus- ja pistenappulat sekä nopat alkutilaan."""

        for lukitusnappula in self.__lukitusnappulat:
                lukitusnappula.configure(state=DISABLED)
        for pistenappula in self.__pelaaja1_nappulat:
                pistenappula.configure(state=DISABLED)
        for pistenappula in self.__pelaaja2_nappulat:
                pistenappula.configure(state=DISABLED)
        for i in range(noppien_lkm):
            self.__nopan_paikat[i].configure(background="black")
            self.__nopat_vapaana[i] = True



    def lukitus(self, i):
        """ Muuttaa nopan tilan vapaasta lukituksi tai päinvastoin.
        :param i: Monettako noppaa muutetaan"""

        if self.__nopat_vapaana[i]:
            self.__nopan_paikat[i].configure(background="red")
            self.__nopat_vapaana[i] = False

        else:
            self.__nopan_paikat[i].configure(background="black")
            self.__nopat_vapaana[i] = True


    def vaihda_vuoro(self):
        """Vaihtaa pelivuoron."""

        self.nollaa_nappulat()
        self.__pelivuoro +=1
        if self.__pelivuoro%2==0:
            self.__vuoro_teksti.configure(text="Pelaajan 2 vuoro", font=bold)
        else:
            self.__vuoro_teksti.configure(text="Pelaajan 1 vuoro", font=bold)

        self.__heittonappula.configure(state=NORMAL)
        self.__heitot = heittovuorot



    def tarkista_lopetus(self):
        """Tarkistaa onko kaikki vuorot käytetty. Jos on, suorittaa tarvittavat
        komennot pelin lopettamiseksi."""

        if self.__pelivuoro==30:
            self.nollaa_nappulat()
            self.__heittonappula.configure(state=DISABLED)
            self.__vuoro_teksti.configure(text="Peli loppui", font=bold)

            try:
                self.__loppupisteet = [int(self.__pelaaja1_syötteet[17]
                            .get()),int(self.__pelaaja2_syötteet[17].get())]

            except ValueError:
                pass

            voittopisteet = max(self.__loppupisteet)
            voittajien_lkm = self.__loppupisteet.count(voittopisteet)

            if voittajien_lkm == 1:
                messagebox.showinfo("Peli loppui!", "Onnittelut Pelaaja " + \
                    str(self.__loppupisteet.index(voittopisteet)+1) + \
                    ", voitit pelin!")
            else:
                self.__pelitilanneteksti = "Tuli tasapeli!"

def main():

    Yatzy()

main()