# _*_ coding: cp1252 _*_

###############################################################
# Autor:   #  Carsten Pfeffer                                 #
#          #                                                  #
# Modul:   #  Bitmap24                                        #
#          #                                                  #
# Datum:   #  September 08                                    #
###############################################################

# -------------------------------------------------------------
# Importe
# -------------------------------------------------------------
import os.path      # F�r Dateioperationen

# -------------------------------------------------------------
# Funktionen
# -------------------------------------------------------------
# Diese Funktionen geh�ren nicht unmittelbar zur Bitmapklasse und sind daher
# nicht als Methoden implementiert

def streamToInt(value):
    '''
    streamToInt rechnet einen Stream aus Bytes in eine Integerzahl um
    @param value: (string) Bytes, deren Wertigkeit konvertiert werden soll
    '''
    # Typ�berpr�fung
    if type(value) != str:
        raise ValueError("Value has to be a string")

    ergebnis = 0
    for i in range(len(value)-1, -1, -1):
        # Einzelne Bytes mit der entsprechenden Wertigkeit aufaddieren
        ergebnis += ord(value[i]) *(256** i)
    return ergebnis


def intToStream(value, length):
    '''
    intToStream rechnet eine Integerzahl in einen Stream aus Bytes um
    @param value: (int)
    @param length: (int) l�nge desgew�nschten streams
    '''
    # Typ�berpr�fung
    if type(value) != int:
        raise ValueError("Value has to be an integer")
    if type(length) != int:
        raise ValueError("length has to be an integer")


    ergebnis = ""

    while value > 0:
        tmp = chr(value % 256)
        value /= 256
        ergebnis += tmp

    if len(ergebnis) > length:
        raise ValueError("Value is too big for length "+str(length))

    while len(ergebnis) < length:
        ergebnis += chr(0)

    return ergebnis

# -------------------------


def negativeStream(value):
    '''
    Rechnet einen Wert, gr��er als 2,2 Mrd. in die entsprechende negative 32 Bit Integerzahl um.
    @param value: (int) Die Zahl, die umgerechnet werden soll
          (Integerobjekte in Python haben mehr als 32 Bit, daher ist dieser Typ hier m�glich)
    '''
    return value-4294967296




# -------------------------------------------------------------
# Klassen
# -------------------------------------------------------------

class Bitmap24(object):
    '''
    Diese Klasse stellt eine 24-Bit Bitmap dar. Zur Instanziierung wird der Dateiname �bergeben.
    '''

    __digits = [["0110", "1011", "1011", "1101", "1101", "0110"], # 0
                ["0010", "0110", "1010", "0010", "0010", "0010"], # 1
                ["0110", "1001", "0001", "0010", "0100", "1111"], # 2
                ["0110", "1001", "0010", "0001", "1001", "0110"], # 3
                ["0100", "0100", "1000", "1010", "1111", "0010"], # 4
                ["1111", "1000", "1110", "0001", "0001", "1110"], # 5
                ["0110", "1000", "1110", "1001", "1001", "0110"], # 6
                ["1111", "0001", "0010", "0010", "0100", "0100"], # 7
                ["0110", "1001", "0110", "1001", "1001", "0110"], # 8
                ["0110", "1001", "1001", "0111", "0001", "0110"], # 9
                ["0000", "0000", "0110", "0000", "0000", "0000"]] # 10

    def __init__(self, filename="", width=0, height=0):
        '''
        Der Konstruktor legt die Attribute an und l�dt das Bild.
        @param filename: (string) Dateiname des Bildes, inklusive absolutem oder relativem Pfad
        '''
        # -- Attribute anlegen
        self.__filename = ""        # Dateiname
        self.__width = 0            # Bildbreite
        self.__height = 0           # Bildh�he

        self.__file_header = ""     # Dateiheader
        self.__bitmap_header = ""   # Bitmapheader
        self.__image_data = []      # Bilddaten

        self.__top_down = False     # Wert zeigt,
                                    # ob das Bild von oben nach unten aufgebaut ist oder nicht

        if filename != "":
            self.setFile(filename)      # Datei �ffnen und Daten einlesen
        else:
            self.__createBitmap(width, height)


    ###########################################################
    # Systemmethoden
    ###########################################################

    def __str__(self):
        '''
        __str__ repr�sentiert das Objekt als String
        '''
        return "Bitmap - 24Bit ["+self.__filename+"], "+str(self.__width)+"x"+str(self.__height)


    ###########################################################
    # Initialisierung
    ###########################################################

    def __createBitmap(self, width, height):
        '''
        initialisiert ein eigenes Bild
        @param width: Breite des Bildes > 0
        @param: height: H�he des Bildes > 0
        '''
        if width <= 0 or height <= 0:
            raise ValueError("width und height m�ssen gr��er als 0 sein")

        self.__width = width
        self.__height = height

        # Anzahl der Bytes, die f�r die Bilddaten gebraucht werden
        w = width*3
        while w % 4 != 0:   # auf ein vielfaches von 4 Bytes bringen
            w += 1
        count = w*height

        # Daten schreiben

        self.__file_header = "BM"                # Dateiheader anlegen
        self.__file_header += intToStream(count+54, 4)  # 4 Byte => Gr��e der Datei            2
        self.__file_header += intToStream(0, 4)  # 4 Byte => 0                                 6
        self.__file_header += intToStream(54, 4) # 4 Byte => Offset der Bilddaten             10
                                                 #     in Byte vom Beginn der Datei an

        self.__bitmap_header = ""
        self.__bitmap_header += intToStream(40, 4)     # 4Byte => 40 BITMAP-HEADER-L�NGE      14
        self.__bitmap_header += intToStream(width, 4)  # 4Byte => BREITE in px                18
        self.__bitmap_header += intToStream(height, 4) # 4Byte => h�he in px (positiv)        22
        self.__bitmap_header += intToStream(1, 2)      # 2Byte => 1 Farbebenen                26
        self.__bitmap_header += intToStream(24, 2)     # 2Byte => 24 Bittiefe                 28
        self.__bitmap_header += intToStream(0, 4)      # 4Byte => 0  Komprimierung            30
        self.__bitmap_header += intToStream(count, 4)  # 4Byte => Gr��e der Bilddaten in Byte 34
        self.__bitmap_header += intToStream(0, 4)      # 4Byte => 0 hor. Aufl�sung            38
        self.__bitmap_header += intToStream(0, 4)      # 4Byte => 0 vert. Aufl�sung           42
        self.__bitmap_header += intToStream(0, 4)      # 4Byte => 0 Gr��e der Farbtabelle     46
        self.__bitmap_header += intToStream(0, 4)      # 4Byte => 0 Anzahl der Farben         50

        bild = []

        while count > 0:
            bild.append(chr(255))
            count -= 1

        self.__image_data = bild

    ###########################################################
    ###########################################################

    def convertCoords(self, x, y):
        '''
        konvertiert x und y Koordinaten in einen Listenindex
        '''
        if x >= self.__width or y >= self.__height:
            raise ValueError("Pixel ist nicht im Bild vorhanden!")

        y = self.__height-y-1

        value = self.__width*3

        while value % 4 != 0:
            value += 1

        return value*y+(x*3)+2


    ###########################################################
    ###########################################################

    def drawDigit(self, digit, x, y, color = (0,0,0)):
        '''
        drawDigit malt eine Zahl der Gr��e 4*6 auf das Bild
        @param digit: Zahl zwischen 0 und 9
        @param x: Horizontale Position
        @param y: Vertikale Position
        '''
        x = int(x)
        y = int(y)
        if digit not in range(11):
            raise ValueError("digit muss eine Zahl zwischen 0 und 9 sein!")

        digit = self.__digits[digit]

        tx = x
        ty = y

        for iy in digit:
            for ix in iy:
                if ix != "0":
                    pos = self.convertCoords(tx,ty)

                    # hier k�nnte es einen Indexfehler geben
                    # wenn die Position au�erhalb des Bildes liegt
                    # es wird im Fehlerfall einfach ignoriert
                    try:
                        self.__image_data[pos] = chr(color[0])
                        self.__image_data[pos-1] = chr(color[1])
                        self.__image_data[pos-2] = chr(color[2])
                    except:
                        pass
                tx += 1
            ty += 1
            tx = x

    ###########################################################
    ###########################################################

    def drawNumber(self, number, x, y):
        '''
        drawNumber malt eine Zahlen auf das Bild
        @param digit: die zu malende Zahl
        @param x: Horizontale Position
        @param y: Vertikale Position
        '''
        x = int(x)
        y = int(y)
        num = str(number)
        for i in num:
            try:
                self.drawDigit(int(i),x,y)
            except:
                # negatives Vorzeichen
                if i == "-":
                    self.drawDigit(10,x,y)
            x += 5

    ###########################################################
    ###########################################################

    def drawPixel(self, x, y, color=(0,0,0)):
        '''
        drawPixel malt einen Pixel an die gegebene Position
        @param x: Horizontale Position
        @param y: Vertikale Position
        '''
        x = int(x)
        y = int(y)
        if x >= self.__width or y >= self.__height:
            return #raise ValueError("die Angegebene Position ist au�erhalb des Bildes")
        pos = self.convertCoords(x,y)

        # hier k�nnte es einen Indexfehler geben
        # wenn die Position au�erhalb des Bildes liegt
        try:
            self.__image_data[pos] = chr(color[0])
            self.__image_data[pos-1] = chr(color[1])
            self.__image_data[pos-2] = chr(color[2])
        except:
            pass #raise ValueError("die Angegebene Position ist au�erhalb des Bildes")

    ###########################################################
    ###########################################################

    def drawLine(self, x1, y1, x2, y2, color=(0,0,0)):
        '''
        drawLine malt eine Linie zwischen zwei Punkten
        @param x1: Horizontale Position1
        @param y1: Vertikale Position1
        @param x2: Horizontale Position2
        @param y2: Vertikale Position2
        '''
        self.drawPixel(x1,y1,color)
        self.drawPixel(x2,y2,color)

        if abs(x1-x2) <= 1 and abs(y1-y2) <= 1:
            return

        xa = (x1+x2)/2
        ya = (y1+y2)/2

        self.drawLine(x1, y1, xa, ya, color)
        self.drawLine(x2, y2, xa, ya, color)




    ###########################################################
    ###########################################################

    def setFile(self, filename):
        '''
        setFile l�dt das Bild.
        @param filename: (string) Dateiname des Bildes, inklusive absolutem oder relativem Pfad
        '''
        # ---- Parameterpr�fung ----
        if type(filename) != str:
            raise ValueError("filename muss ein String sein!")

        # ist die Datei �berhaupt vorhanden?
        if not os.path.isfile(filename):
            raise IOError("Die Datei \""+filename+"\" wurde nicht gefunden!")

        # ist die Datei lesbar?
        try:
            ref = file(filename, "rb")
        except:
            raise IOError("Die Datei \""+filename+"\" konnte nicht ge�ffnet werden")


        # Bei Erfolg neuen Dateinamen setzten
        self.__filename = filename

        # die Referenz auf die Datei den Methoden �bergeben, die den Header und die Bilddaten auslesen
        self.__readHeader(ref)
        self.__readImageData(ref)

        # nachdem alle Daten gelesen wurden, wird die Datei geschlossen
        ref.close()

    ###########################################################
    ###########################################################

    def __readHeader(self, ref):
        '''
        __readHeader liest den Header aus.
        @param ref: (file) Referenz auf eine Datei (�ber file("bild.bmp", "rb") ge�ffnet)
        '''
        # == Fileheader ===========================
        # =========================================

        # Dateityp pr�fen
        filetype = ref.read(2)
        if filetype != "BM":        # in den ersten zwei Bytes der Datei muss BM stehen, sonst
            ref.close()             # handelt es sich nicht um eine Bitmap
            raise TypeError("Die Datei \""+self.__filename+"\" ist keine g�ltige Bitmap-Datei!")

        # die n�chsten 12 Bytes sind nicht f�r unsere Zwecke relevant, sie werden nur gelesen,
        # nicht verarbeitet, sie werden dennoch im Attribut file_header gespeichert,
        # um sie beim Speichern einer Datei wieder schreiben zu k�nnen
        self.__file_header = filetype + ref.read(12)


        # == Bitmap-Header ========================
        # =========================================

        tmp = ref.read(4)           # Die L�nge des Bitmap-Headers auslesen
        hlen = streamToInt(tmp)     # und aus 4 Bytes eine Zahl machen

        self.__bitmap_header = tmp  # die gelesenen Bytes an das Attribut bitmap_header anh�ngen
        self.__bitmap_header += ref.read(hlen-4) # die restlichen Headerbytes im Attribut speichern

        # Abmessungen speichern
        self.__width = streamToInt(self.__bitmap_header[4:8])     # die Bildbreite in Pixeln wird ausgelesen
        self.__height = streamToInt(self.__bitmap_header[8:12])   # die H�he ebenfalls

        # wenn die H�he negativ im 2er Komplement angegeben wurde,
        # wird das Bild von oben nach unten aufgebaut (Top-Down-Bitmap)
        if self.__height > 2147483647:
            self.__top_down = True
            self.__height = negativeStream(self.__height)

        # Farbtiefe pr�fen
        depth = ord(self.__bitmap_header[14])
        # Es k�nnen nur Bitmap-Dateien mit 24 Bit Farbtiefe, also 3 Bytes pro Pixel gelesen werden
        if depth != 24:
            ref.close()
            raise TypeError("Die Datei \""+self.__filename+"\" ist keine g�ltige 24-Bit Bitmap!")


    ###########################################################
    ###########################################################

    def __readImageData(self, ref):
        '''
        __readImageData liest das eigentliche Bild aus.
        @param ref: (file) Referenz auf eine Datei (�ber file("bild.bmp", "rb") ge�ffnet)
        '''
        # == Bilddaten ==============================
        bild = []

        daten = ref.read(1) # erstes Zeichen lesen

        # solange Zeichen vorhanden sind
        while daten:
            # Zeichen wird angeh�ngt
            bild.append(daten)
            daten = ref.read(1) # ein Zeichen lesen

        # im Attribut speichern
        self.__image_data = bild



    ############################################################
    ############################################################


    def writeBitmap(self, filename):
        '''
        writeBitmap speichert die Bilddaten in einer Bitmap-Datei.
        @param filename: (string) Dateiname der neuen Bilddatei, inklusive absolutem oder relativem Pfad
        '''
        # Parameter�berpr�fung
        if type(filename) != str:
            raise ValueError("filename muss ein String sein!")

        # Daten zusammensuchen
        output = self.__file_header     # Dateiheader enth�lt Informationen zur Datei
        output += self.__bitmap_header  # Bitmapheader enth�lt Bildinformationen
                                        # (Breite H�he, Farbtiefe, Kompression, ect...)

        for i in self.__image_data:     # Die Bilddaten werden wieder zusammengesetzt
            output += i

        # Datei schreiben
        try:
            ref = file(filename, "wb")
            ref.write(output)
        except:
            raise IOError("In die Datei \""+self.__filename+"\" konnte nicht geschrieben werden!")

        ref.close() #Datei schlie�en

    ###########################################################
    ###########################################################

    def getWidth(self):
        '''
        getWidth gibt die Breite des Bildes in Pixeln zur�ck.
        '''
        return self.__width

    ###########################################################
    ###########################################################

    def getHeight(self):
        '''
        getHeight gibt die H�he des Bildes in Pixeln zur�ck.
        '''
        return self.__height

    ###########################################################
    ###########################################################

    def getSize(self):
        '''
        getSize gibt die Gr��e des Bildes in Pixeln zur�ck.
        '''
        return self.__width, self.__height

    ###########################################################
    ###########################################################

    def getFileName(self):
        '''
        getFileName gibt den Originaldateinamen des Bildes zur�ck.
        '''
        return self.__filename

    ###########################################################
    ###########################################################

    def isBottomUp(self):
        '''
        liefert True, wenn das Bid von unten nach oben aufgebaut wird
        '''
        return not self.__top_down

    ###########################################################
    ###########################################################

    def isTopDown(self):
        '''
        liefert True, wenn das Bid von oben nach unten aufgebaut wird
        '''
        return self.__top_down


    ###########################################################
    ###########################################################

    def flipVertically(self):
        '''
        spiegelt das Bild vertikal
        '''
        image_data = []
        for i in range(self.__height, -1, -1):
            von = (self.__width*3*i)-(self.__width*3)
            bis = (self.__width*3*i)
            image_data += self.__image_data[von:bis]
        self.__image_data = image_data

    ###########################################################
    ###########################################################

    def getImageData(self):
        '''
        getImageData gibt die Bilddaten zur�ck.
        '''
        data = ""

        for y in range(self.__height):
            for x in range(self.__width):
                i = self.convertCoords(x,y)
                data += self.__image_data[i]
                data += self.__image_data[i-1]
                data += self.__image_data[i-2]
        return data

    ###########################################################
    ###########################################################

    def setImageData(self, data):
        '''
        setImageData setzt die Bilddaten
        @param data: (string) Die L�nge der Daten muss der H�he*Breite*3 entsprechen
        '''
        if len(data) != self.__width*self.__height*3:
            raise ValueError("Die angegebenen Bilddaten passen nicht in das Bild!")

#        # daten umkehren, wenn das Bild von unten aufgebaut wird
#        if not self.__top_down:
#            data2 = ""
#            for i in range(self.__height, -1, -1):
#                von = (self.__width*3*i)-(self.__width*3)
#                bis = (self.__width*3*i)
#                data2 += data[von:bis]
#            data = data2



        offset = []
        while (self.__width*3+len(offset)) %4 != 0:
            offset.append(chr(0))

        image_data = []
        x = 0
        for i in data:
            x += 1
            image_data.append(i)
            if x == self.__width*3:
                image_data += offset

        self.__image_data = image_data

#        for y in range(self.__height):
#            for x in range(self.__width):
#                i = self.convertCoords(x,y)
#                data += self.__image_data[i]
#                data += self.__image_data[i-1]
#                data += self.__image_data[i-2]
#        return data


# ------------------------------------------------------------------------------------------------

def saveSpielbrett(filename, name, autor, feld_weiss, feld_schwarz, stein_weiss, stein_schwarz, dame_weiss, dame_schwarz, background=(0,128,128)):
    '''
    '''
    if type(filename) != str:
        raise TypeError("Der Parameter 'filename' muss vom Typ String sein!")
    if type(name) != str:
        raise TypeError("Der Parameter 'name' muss vom Typ String sein!")
    if type(autor) != str:
        raise TypeError("Der Parameter 'autor' muss vom Typ String sein!")
    if type(feld_weiss) != Bitmap24:
        raise TypeError("Der Parameter 'feld_weiss' muss vom Typ Bitmap24 sein!")
    if type(feld_schwarz) != Bitmap24:
        raise TypeError("Der Parameter 'feld_schwarz' muss vom Typ Bitmap24 sein!")
    if type(stein_weiss) != Bitmap24:
        raise TypeError("Der Parameter 'stein_weiss' muss vom Typ Bitmap24 sein!")
    if type(stein_schwarz) != Bitmap24:
        raise TypeError("Der Parameter 'stein_schwarz' muss vom Typ Bitmap24 sein!")
    if type(dame_weiss) != Bitmap24:
        raise TypeError("Der Parameter 'dame_weiss' muss vom Typ Bitmap24 sein!")
    if type(dame_schwarz) != Bitmap24:
        raise TypeError("Der Parameter 'dame_schwarz' muss vom Typ Bitmap24 sein!")

    if type(background) != Bitmap24:
        if type(background) != tuple or len(background) != 3:
            raise TypeError("Der Parameter 'background' muss ein Bitmap24-Objekt oder dreielementiges Farbtupel sein!")

    if len(name) > 255 or len(autor) > 255:
        raise ValueError("'name' und 'autor' d�rfen nicht l�nger als 255 Zeichen sein!")

    if feld_weiss.getSize() != (70,70) or feld_schwarz.getSize() != (70,70):
        raise ValueError("Die Spielfelder m�ssen 70x70 Pixel gro� sein!")

    if stein_weiss.getSize() != (44,44) or stein_schwarz.getSize() != (44,44) or dame_weiss.getSize() != (44,44) or dame_schwarz.getSize() != (44,44):
        raise ValueError("Alle Sielsteine m�ssen 44x44 Pixel gro� sein!")

    stream = ""

    stream += chr(0)+"dame"+chr(0)      # x0damex0 als Dateitypsignatur
    stream += chr(len(name))            # l�nge des Spielbrett
    stream += name                      # Spielbrettname
    stream += chr(len(autor))           # L�nge des Namens des Autors
    stream += autor                     # Name des Autors

    stream += feld_weiss.getImageData()         # Bilddaten der einzelen
    stream += feld_schwarz.getImageData()       # Steine / Felder haben eine
    stream += stein_weiss.getImageData()        # feste L�nge und werden daher
    stream += stein_schwarz.getImageData()      # einfach in den Stream eingef�gt
    stream += dame_weiss.getImageData()
    stream += dame_schwarz.getImageData()

    # ist ein Hintergrundbild gesetzt, wird das Flag i der Datei auf einen
    # Wert ungleich 0 gesetzt
    if type(background) == Bitmap24:
        stream += chr(255)

        w,h = background.getSize()  # H�he und Breite des Hintergrundbildes ermitteln
        stream += intToStream(w,4)  # in dem Stream speichern
        stream += intToStream(h,4)
        stream += background.getImageData()

    # soll nur eine Farbe gesetzt werden, ist das Flag 0
    else:
        stream += chr(0)
        stream += chr(background[0])
        stream += chr(background[1])
        stream += chr(background[2])

    try:
        f = file(filename, "wb")
        f.write(stream)
        f.close()
    except:
        raise IOError("Die Datei konnte nicht geschrieben werden!")

# ------------------------------------------------------------------------------------------------

def openSpielbrett(filename):
    '''
    '''

    try:
        f = file(filename, "rb")
    except:
        raise IOError("Die Datei konnte nicht gelesen werden!")

    if f.read(6) != chr(0)+"dame"+chr(0):
        raise TypeError("Die Datei ist keine Dame-Spielbrett-Datei")

    count = f.read(1)
    name = f.read(ord(count))
    count = f.read(1)
    autor = f.read(ord(count))

    feld_weiss = f.read(14700)
    feld_schwarz = f.read(14700)
    stein_weiss = f.read(5808)
    stein_schwarz = f.read(5808)
    dame_weiss = f.read(5808)
    dame_schwarz = f.read(5808)

    flag = ord(f.read(1))

    # wenn ein Hintergrundbild geladen werden muss...
    if flag:
        w = streamToInt(f.read(4))
        h = streamToInt(f.read(4))
        count = 3*w*h
        background = f.read(count)

        f.close()
        return name, autor, feld_weiss, feld_schwarz, stein_weiss, stein_schwarz, dame_weiss, dame_schwarz, (w, h, background)

    # wenn es nur eine Farbe ist...
    else:
        r = ord(f.read(1))
        g = ord(f.read(1))
        b = ord(f.read(1))

        f.close()
        return name, autor, feld_weiss, feld_schwarz, stein_weiss, stein_schwarz, dame_weiss, dame_schwarz, (r, g, b)

# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------

# ein kleiner Testrahmen, der nur ausgef�hrt wird, wenn die Datei direkt ausgef�hrt wird
if __name__ == "__main__":

    feld_weiss = Bitmap24("feld_weiss.bmp")
    feld_schwarz = Bitmap24("feld_schwarz.bmp")
    stein_weiss = Bitmap24("stein_weiss.bmp")
    stein_schwarz = Bitmap24("stein_schwarz.bmp")
    dame_weiss = Bitmap24("dame_weiss.bmp")
    dame_schwarz = Bitmap24("dame_schwarz.bmp")

    name="Standard Spielbrett"
    autor="Carsten Pfeffer"

    #saveSpielbrett("standard.brett", name, autor, feld_weiss, feld_schwarz, stein_weiss, stein_schwarz, dame_weiss, dame_schwarz)
    background = Bitmap24("textur.bmp")
    saveSpielbrett("standard.brett", name, autor, feld_weiss, feld_schwarz, stein_weiss, stein_schwarz, dame_weiss, dame_schwarz,background)
    name, autor, feld_weiss, feld_schwarz, stein_weiss, stein_schwarz, dame_weiss, dame_schwarz, background = openSpielbrett("standard.brett")

    print name, "#", autor, "#",

    if type(background[2]) == str:
        print "hat ein Hintergrundbild"
        print "Groesse: %dx%d" % (background[0],background[1])
    else:
        print "hat kein Hintergrundbild"
        print "Farbe: %d,%d,%d" % background

