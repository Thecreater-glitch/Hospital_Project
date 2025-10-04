import tkinter as tk
from tkinter import Menu 
import sqlite3
from tkinter import messagebox
from tkcalendar import Calendar



secilenHasta=None
secilenDoktor=None
secilenTakvim=None
#--------- Ana Pencere ---------------
root=tk.Tk()
root.title("---- HASTA KAYIT PROGRAMI -----")
root.geometry("1000x800+150+10")
#-------------------------------------
#VERİTABANI OLUŞTURMA ALANI
# hastaneVeritabani=sqlite3.connect("hastaneKayitVerileri.db")
# veri=hastaneVeritabani.cursor()

# # Bu kısım her işlem için değişecek - SQL kodları gelecek

# hastaneVeritabani.commit()
# hastaneVeritabani.close()

doktorVeritabani=sqlite3.connect("doktorKayitVerileri.db")
veri=doktorVeritabani.cursor()

veri.execute('''          
         CREATE TABLE  IF NOT EXISTS doktor( 
         kimlik INTEGER PRIMARY KEY AUTOINCREMENT,
         ad TEXT,
         soyad TEXT,
         yas INTEGER,
         cinsiyet TEXT
         )    
             
             ''' )

doktorVeritabani.commit()
doktorVeritabani.close()


hastaneVeritabani=sqlite3.connect("hastaneKayitVerileri.db")
veri=hastaneVeritabani.cursor()

veri.execute('''          
         CREATE TABLE  IF NOT EXISTS hastane( 
         kimlik INTEGER PRIMARY KEY AUTOINCREMENT,
         ad TEXT,
         soyad TEXT,
         yas INTEGER,
         cinsiyet TEXT
         )    
             
             ''' )

hastaneVeritabani.commit()
hastaneVeritabani.close()


#------------------------------


def hastaKayit():
    hastaKayitEkrani=tk.Toplevel()
    hastaKayitEkrani.title("HASTA KAYIT EKRANI")
    hastaKayitEkrani.geometry("500x400+300+200")
    #---- Kaydetme işlemi----
    def kaydet():
        ad=hastaAdiEntry.get()
        soyad=hastasoyadEntry.get()
        yas=hastayasEntry.get()
        cinsiyet=hastacinsiyetEntry.get()        
  
        hastaneVeritabani=sqlite3.connect("hastaneKayitVerileri.db")
        veri=hastaneVeritabani.cursor()
        veri.execute('''                 
                INSERT INTO hastane(ad,soyad,yas,cinsiyet) VALUES (?,?,?,?)                    
                    ''', (ad,soyad,yas,cinsiyet) )
        hastaneVeritabani.commit()
        hastaneVeritabani.close()
        messagebox.showinfo("kayit islemli","hastakayit basarila gerceklesti")
        
    hastaAdi=tk.Label(hastaKayitEkrani,text="Adınız:",font=("Arial",12)).place(x=40,y=100)
    hastaAdiEntry=tk.Entry(hastaKayitEkrani)
    hastaAdiEntry.place(x=120,y=100)
    
    hastasoyad=tk.Label(hastaKayitEkrani,text="Soyadınız:",font=("Arial",12)).place(x=40,y=140)
    hastasoyadEntry=tk.Entry(hastaKayitEkrani)
    hastasoyadEntry.place(x=120,y=140)
    
    
    hastayas=tk.Label(hastaKayitEkrani,text="Yaşınız:",font=("Arial",12)).place(x=40,y=180)
    hastayasEntry=tk.Entry(hastaKayitEkrani)
    hastayasEntry.place(x=120,y=180)
    
    hastacinsiyet=tk.Label(hastaKayitEkrani,text="Cinsiyet:",font=("Arial",12)).place(x=40,y=220)
    hastacinsiyetEntry=tk.Entry(hastaKayitEkrani)
    hastacinsiyetEntry.place(x=120,y=220)
    
    kaydetButton=tk.Button(hastaKayitEkrani,text="KAYDET",command=kaydet).place(x=40,y=270)


def hastaListele():
    listelemeEkrani=tk.Toplevel()
    listelemeEkrani.geometry("500x600+200+200")
    listelemeEkrani.title("HASTALAR LİSTESİ")
    
    tk.Label(listelemeEkrani,text="HASTALAMIZ",font=("Georgia",14),fg="red").place(x=200,y=20)
    
    listem=tk.Listbox(listelemeEkrani,width=40,height=30)
    listem.place(x=30,y=60)
    
    hastaneVeritabani=sqlite3.connect("hastaneKayitVerileri.db")
    veri=hastaneVeritabani.cursor()
    veri.execute('''                 
                  SELECT * FROM hastane               
                    ''' )
    hastalar=veri.fetchall()
    hastaneVeritabani.close()
    
    print(hastalar)
    
    for hasta in hastalar:
        duzenliBilgi=f"{hasta[0]} -- {hasta[1]}   {hasta[2]}  {hasta[3]}"
        listem.insert(tk.END,duzenliBilgi)

    
    def sil():
        secilen=listem.curselection()
        
        if not secilen:
            messagebox.showwarning("Uyarı"," Lütfen bir hasta seçiniz")
        
        siraNumarasi=secilen[0]
        secilenHasta=hastalar[siraNumarasi]
        secilenKimlikNo=secilenHasta[0]
        
        hastaneVeritabani=sqlite3.connect("hastaneKayitVerileri.db")
        veri=hastaneVeritabani.cursor()
        veri.execute('''   
                        DELETE FROM hastane WHERE kimlik=?           
               ''',(secilenKimlikNo,))
        hastaneVeritabani.commit()
        hastaneVeritabani.close()
        hastaListele()
    
    def guncelle():
        guncellemeEkrani=tk.Toplevel()
        guncellemeEkrani.geometry("500x400+300+200")
        guncellemeEkrani.title("GUNCELLEME")
        
        def update():
            ad=hastaAdiEntry.get()
            soyad=hastasoyadEntry.get()
            yas=hastayasEntry.get()
            cinsiyet=hastacinsiyetEntry.get()        
  
            hastaneVeritabani=sqlite3.connect("hastaneKayitVerileri.db")
            veri=hastaneVeritabani.cursor()
            veri.execute('''                 
                    UPDATE  hastane SET ad=?,soyad=?,yas=?,cinsiyet=? WHERE  kimlik=?                 
                        ''', (ad,soyad,yas,cinsiyet,secilenHasta[0]) )
            hastaneVeritabani.commit()
            hastaneVeritabani.close

        
        secilen=listem.curselection()
        
        if not secilen:
            messagebox.showwarning("Uyarı"," Lütfen bir hasta seçiniz")
        
        siraNumarasi=secilen[0]
        secilenHasta=hastalar[siraNumarasi]
        print(secilenHasta)
        
        hastaAdi=tk.Label(guncellemeEkrani,text="Adınız:",font=("Arial",12)).place(x=40,y=100)
        hastaAdiEntry=tk.Entry(guncellemeEkrani)
        hastaAdiEntry.place(x=120,y=100)
        hastaAdiEntry.insert(0,secilenHasta[1])
        
        hastasoyad=tk.Label(guncellemeEkrani,text="Soyadınız:",font=("Arial",12)).place(x=40,y=140)
        hastasoyadEntry=tk.Entry(guncellemeEkrani)
        hastasoyadEntry.place(x=120,y=140)
        hastasoyadEntry.insert(0,secilenHasta[2])
        
        
        hastayas=tk.Label(guncellemeEkrani,text="Yaşınız:",font=("Arial",12)).place(x=40,y=180)
        hastayasEntry=tk.Entry(guncellemeEkrani)
        hastayasEntry.place(x=120,y=180)
        hastayasEntry.insert(0,secilenHasta[3])
        
        hastacinsiyet=tk.Label(guncellemeEkrani,text="Cinsiyet:",font=("Arial",12)).place(x=40,y=220)
        hastacinsiyetEntry=tk.Entry(guncellemeEkrani)
        hastacinsiyetEntry.place(x=120,y=220)
        hastacinsiyetEntry.insert(0,secilenHasta[4])
        
        guncelleButton=tk.Button(guncellemeEkrani,text="GUNCELLE",command=update).place(x=40,y=270)        
            
    
    guncelleButton=tk.Button(listelemeEkrani,text="GÜNCELLE",font=("Arial",13),width=20,command=guncelle).place(x=300,y=60)
    silButton=tk.Button(listelemeEkrani,text="SİL",font=("Arial",13),width=20,command=sil).place(x=300,y=100)
    



def doktorKayit():
    doktorKayitEkrani=tk.Toplevel()
    doktorKayitEkrani.title("DOKTOR KAYIT EKRANI")
    doktorKayitEkrani.geometry("500x400+300+200")
    #---- Kaydetme işlemi----
    def kaydet():
        ad=doktorAdiEntry.get()
        soyad=doktorsoyadEntry.get()
        yas=doktoryasEntry.get()
        cinsiyet=doktorcinsiyetEntry.get()        
  
        doktorVeritabani=sqlite3.connect("doktorKayitVerileri.db")
        veri=doktorVeritabani.cursor()
        veri.execute('''                 
                INSERT INTO doktor(ad,soyad,yas,cinsiyet) VALUES (?,?,?,?)                    
                    ''', (ad,soyad,yas,cinsiyet) )
        doktorVeritabani.commit()
        doktorVeritabani.close()
        messagebox.showinfo("kayit islemli","hastakayit basarila gerceklesti")
        
    doktorAdi=tk.Label(doktorKayitEkrani,text="Adınız:",font=("Arial",12)).place(x=40,y=100)
    doktorAdiEntry=tk.Entry(doktorKayitEkrani)
    doktorAdiEntry.place(x=120,y=100)
    
    doktorsoyad=tk.Label(doktorKayitEkrani,text="Soyadınız:",font=("Arial",12)).place(x=40,y=140)
    doktorsoyadEntry=tk.Entry(doktorKayitEkrani)
    doktorsoyadEntry.place(x=120,y=140)
    
    
    doktoryas=tk.Label(doktorKayitEkrani,text="Yaşınız:",font=("Arial",12)).place(x=40,y=180)
    doktoryasEntry=tk.Entry(doktorKayitEkrani)
    doktoryasEntry.place(x=120,y=180)
    
    doktorcinsiyet=tk.Label(doktorKayitEkrani,text="Cinsiyet:",font=("Arial",12)).place(x=40,y=220)
    doktorcinsiyetEntry=tk.Entry(doktorKayitEkrani)
    doktorcinsiyetEntry.place(x=120,y=220)
    
    kaydetButton=tk.Button(doktorKayitEkrani,text="KAYDET",command=kaydet).place(x=40,y=270)


def doktorListesi():
    ListelemeEkrani1=tk.Toplevel()
    ListelemeEkrani1.geometry("500x600+200+200")
    ListelemeEkrani1.title("DOKTOR LISTESI")

    tk.Label(ListelemeEkrani1, text="Doktor",font=("Georgia",14),fg="red").place(x=200,y=20)

    listem=tk.Listbox(ListelemeEkrani1,width=40,height=30)
    listem.place(x=30,y=60)

    doktorVeritabani=sqlite3.connect("doktorKayitVerileri.db")
    veri=doktorVeritabani.cursor()
    veri.execute('''                 
                         SELECT * from doktor        
                    ''' )
    doktorlar=veri.fetchall()
    doktorVeritabani.close()
    print(doktorlar)

    for doktor in doktorlar:
        düzenliBilgiler=f"{doktor[0]} -- {doktor[1]}    {doktor[2]}    {doktor[3]}"
        listem.insert(tk.END,düzenliBilgiler)

    def sil():
        secilen=listem.curselection()
        
        if not secilen:
            messagebox.showwarning("Uyarı"," Lütfen bir hasta seçiniz")
        
        siraNumarasi=secilen[0]
        secilenDoktor=doktorlar[siraNumarasi]
        secilenKimlikNo=secilenDoktor[0]
        
        doktorVeritabani=sqlite3.connect("doktorKayitVerileri.db")
        veri=doktorVeritabani.cursor()
        veri.execute('''   
                        DELETE FROM doktor WHERE kimlik=?           
               ''',(secilenKimlikNo,))
        doktorVeritabani.commit()
        doktorVeritabani.close()
        doktorListesi()

    def guncelle():
        guncellemeEkrani1=tk.Toplevel()
        guncellemeEkrani1.geometry("500x400+300+200")
        guncellemeEkrani1.title("GUNCELLEME")
        
        
        secilen=listem.curselection()
        
        if not secilen:
            messagebox.showwarning("Uyarı"," Lütfen bir doktor seçiniz")
        
        siraNumarasi=secilen[0]
        secilenDoktor=doktorlar[siraNumarasi]
        print(secilenDoktor)
        
        doktorAdi=tk.Label(guncellemeEkrani1,text="Adınız:",font=("Arial",12)).place(x=40,y=100)
        doktorAdiEntry=tk.Entry(guncellemeEkrani1)
        doktorAdiEntry.place(x=120,y=100)
        doktorAdiEntry.insert(0,secilenDoktor[1])
        
        doktorsoyad=tk.Label(guncellemeEkrani1,text="Soyadınız:",font=("Arial",12)).place(x=40,y=140)
        doktorsoyadEntry=tk.Entry(guncellemeEkrani1)
        doktorsoyadEntry.place(x=120,y=140)
        doktorsoyadEntry.insert(0,secilenDoktor[2])
        
        
        doktoryas=tk.Label(guncellemeEkrani1,text="Yaşınız:",font=("Arial",12)).place(x=40,y=180)
        doktoryasEntry=tk.Entry(guncellemeEkrani1)
        doktoryasEntry.place(x=120,y=180)
        doktoryasEntry.insert(0,secilenDoktor[3])
        
        doktorcinsiyet=tk.Label(guncellemeEkrani1,text="Cinsiyet:",font=("Arial",12)).place(x=40,y=220)
        doktorcinsiyetEntry=tk.Entry(guncellemeEkrani1)
        doktorcinsiyetEntry.place(x=120,y=220)
        doktorcinsiyetEntry.insert(0,secilenDoktor[4])
        
        guncelleButton=tk.Button(guncellemeEkrani1,text="GUNCELLE").place(x=40,y=270)        
            
    
    guncelleButton=tk.Button(ListelemeEkrani1,text="GÜNCELLE",font=("Arial",13),width=20,command=guncelle).place(x=300,y=60)
    silButton=tk.Button(ListelemeEkrani1,text="SİL",font=("Arial",13),width=20,command=sil).place(x=300,y=100)
    

def randevu():
    randevuEkrani=tk.Toplevel()
    randevuEkrani.geometry("1000x600+200+200")
       
    tk.Label(randevuEkrani,text="Hastalarımız",font=("Georgia",14),fg="red").place(x=30,y=20)
    
    hastalistem=tk.Listbox(randevuEkrani,width=40,height=30)
    hastalistem.place(x=30,y=60)
    
    hastaneVeritabani=sqlite3.connect("hastaneKayitVerileri.db")
    veri=hastaneVeritabani.cursor()
    veri.execute('''                 
                  SELECT * FROM hastane               
                    ''' )
    hastalar=veri.fetchall()
    hastaneVeritabani.close()
    
    print(hastalar)
    
    for hasta in hastalar:
        duzenliBilgi=f" {hasta[1]}   {hasta[2]}"
        hastalistem.insert(tk.END,duzenliBilgi)
    
    #doktor 
    tk.Label(randevuEkrani, text="Doktor",font=("Georgia",14),fg="red").place(x=350,y=20)

    doktorlistem=tk.Listbox(randevuEkrani,width=40,height=30)
    doktorlistem.place(x=350,y=60)

    doktorVeritabani=sqlite3.connect("doktorKayitVerileri.db")
    veri=doktorVeritabani.cursor()
    veri.execute('''                 
                         SELECT * from doktor        
                    ''' )
    doktorlar=veri.fetchall()
    doktorVeritabani.close()
    print(doktorlar)

    for doktor in doktorlar:
        düzenliBilgiler=f"{doktor[1]}    {doktor[2]} "
        doktorlistem.insert(tk.END,düzenliBilgiler)


    tk.Label(randevuEkrani,text="Tarih",font=("Georgi",14),fg="red").place(x=650,y=20)
    takvim=Calendar(randevuEkrani,date_pattern="dd-mm-yyyy",selectmode="day")
    takvim.place(x=650,y=60)

    def hastaSec():
        global secilenHasta
        hastaSirasi=hastalistem.curselection()[0]
        secilenHasta=hastalar[hastaSirasi]
        print(secilenHasta[1])

    
    def doktorSec():
        global secilenDoktor
        doktorSirasi=doktorlistem.curselection()[0]
        secilenDoktor=doktorlar[doktorSirasi]
        print(secilenDoktor[1])

    def tarihSec():
        global secilenTarih
        secilenTarih=takvim.get_date()
        print(secilenTarih)

    def randevuOlustur():
        if secilenHasta is None or secilenDoktor is None:
            messagebox.showwarning("Eksik", "Hasta ve doktor seçiniz")
            return
        msj = f"{secilenHasta[1]}  {secilenHasta[2]} hastamızın {secilenDoktor[1]} {secilenDoktor[2]} doktorumuz ile {secilenTarih} de randevusu oluşturulmuştur"
        messagebox.showinfo("RADEVU BİLGİSİ",msj)


    hastaSec=tk.Button(randevuEkrani,text="Hasta Sec",command=hastaSec)
    hastaSec.place(x=30,y=550)
    doktorSec=tk.Button(randevuEkrani,text="Doktor Sec",command=doktorSec)
    doktorSec.place(x=350,y=550)
    tarihSec=tk.Button(randevuEkrani,text="Tarih Sec",command=tarihSec)
    tarihSec.place(x=650,y=550)
    randevuolusturSec=tk.Button(randevuEkrani,text="Randevu Oluştur",command=randevuOlustur)
    randevuolusturSec.place(x=800,y=550)
#-------Canli destek------------------
def canliDestek():
    destekEkrani=tk.Toplevel()
    destekEkrani.geometry("300x500+1050+420")
    destekEkrani.title("CANLI DESTEK")
    
    def mesajAl():
        mesaj=soru.get()
        mesajGoster(mesaj)
        cevapVer(mesaj)
        
    
    def mesajGoster(mesaj):
        cevapAlani.insert(tk.END,mesaj+"\n")
        
    def cevapVer(mesaj):
        cevaplar={
            "merhaba":"teşekkür ederim iyiyim sen nasılsın",
            "nasılsın":"iyidir arkadaş nasılsın",
            "nasıl randevu alabilirim":"Hasta kayıt menusunden randevu alabilirsin"
        }
        
        sorumunCevabi=cevaplar.get(mesaj)
        mesajGoster(sorumunCevabi)
        
        
        
    
    
    soru=tk.Entry(destekEkrani,font=("Georgia",12),width=25)
    soru.place(x=10,y=20)
    
    cevapAlani=tk.Text(destekEkrani,width=25,height=20,font=("Georgia",12))
    cevapAlani.place(x=10,y=60)
    
    cevaplaButton=tk.Button(destekEkrani,text="CEVAPLA",font=("Georgia",12),command=mesajAl)
    cevaplaButton.place(x=30,y=450)


destekButton=tk.Button(root, text="canli destek",font=("Georgia",12), command=canliDestek)
destekButton.place(x=900, y=600)

#-------------------------------------

resim=tk.PhotoImage(file="assets\hospital.png")
resimLabel=tk.Label(root,image=resim,borderwidth=5,highlightbackground="gray",highlightthickness=10)
resimLabel.place(x=220,y=100)








# ------ MENU ------------------------
mymenu=Menu(root,tearoff=0)

# Hasta işlemleri Menüsü
hasta_menu=Menu(mymenu,tearoff=0)
hasta_menu.add_command(label="Hasta Kayıt",font=("Arial",12),command=hastaKayit)
hasta_menu.add_command(label="Hasta Listesi",font=("Arial",12),command=hastaListele)
hasta_menu.add_command(label="Hasta Radevuları",font=("Arial",12),command=randevu)

#Doktor işlemleri
doktor_menu=Menu(mymenu,tearoff=0)
doktor_menu.add_command(label="Doktor Kaydı",font=("Arial",12),command=doktorKayit)
doktor_menu.add_command(label="Doktorlar Listesi",font=("Arial",12),command=doktorListesi)
#-------------
# YArdım menusu


# iletişim Menusu

mymenu.add_cascade(label="Hasta işlemleri",menu=hasta_menu,font=("Arial",12))
mymenu.add_cascade(label="Doktor işlemleri",menu=doktor_menu,font=("Arial",12))
root.config(menu=mymenu)
#-------------------------------------
root.mainloop()