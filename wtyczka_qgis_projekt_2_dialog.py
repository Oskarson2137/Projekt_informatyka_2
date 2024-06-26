# -*- coding: utf-8 -*-

import os
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtCore import QVariant
from qgis.PyQt.QtCore import Qt
from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from qgis.utils import iface
from qgis.core import *

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'wtyczka_qgis_projekt_2_dialog_base.ui'))


class WtyczkaQgisProjekt2Dialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(WtyczkaQgisProjekt2Dialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        self.button_box.accepted.connect(self.resetowanie_a)
        self.button_box.rejected.connect(self.resetowanie_r)

        self.pushButton_wybierz.clicked.connect(self.wybierz_punkty)
        self.pushButton_clear.clicked.connect(self.clear)
        self.pushButton_wybierz.clicked.connect(self.minimalizuj)
        
        self.pushButton_oblicz.clicked.connect(self.oblicz)
        self.mMapLayerComboBox_wybor_warstwy.setAllowEmptyLayer(True, 'Wybierz warstwę')
        self.mMapLayerComboBox_wybor_warstwy.setCurrentIndex(0)
        self.mMapLayerComboBox_wybor_warstwy.currentIndexChanged.connect(self.zmiana_warstwy)

        self.checkBox_pl2000.clicked.connect(self.odznaczanie_pl)
        self.checkBox_pl1992.clicked.connect(self.odznaczanie_pl)

        self.checkBox_s5.clicked.connect(self.odznaczanie_stref)
        self.checkBox_s6.clicked.connect(self.odznaczanie_stref)
        self.checkBox_s7.clicked.connect(self.odznaczanie_stref)
        self.checkBox_s8.clicked.connect(self.odznaczanie_stref)

        self.label_strefa.setVisible(False)
        self.checkBox_s5.setVisible(False)
        self.checkBox_s6.setVisible(False)
        self.checkBox_s7.setVisible(False)
        self.checkBox_s8.setVisible(False)
        self.checkBox_pl2000.stateChanged.connect(self.zmiana_widocznosci)

        self.checkBox_a.setVisible(False)
        self.checkBox_m2.setVisible(False)
        self.checkBox_ha.setVisible(False)

        self.checkBox_a.clicked.connect(self.odznaczanie_pola)
        self.checkBox_m2.clicked.connect(self.odznaczanie_pola)
        self.checkBox_ha.clicked.connect(self.odznaczanie_pola)

        self.radioButton_pole.clicked.connect(self.zmiana_widocznosci_pola)
        self.radioButton_dH.clicked.connect(self.zmiana_widocznosci_pola)

        self.checkBox_m2.setChecked(True)
        self.mFieldComboBox_wybor_atrybutu.setVisible(False)
        self.checkBox_poligon.setVisible(False)

        self.mQgsFileWidget_plik.setFilter('Text files (*.txt *.csv)')
        self.mQgsFileWidget_plik.setDialogTitle('Wybierz plik tekstowy')
        self.mQgsFileWidget_plik.fileChanged.connect(self.open_file)
        self.lineEdit_nazwa_warstwy.setPlaceholderText('Wprowadz nazwe warstwy')
        self.pushButton_wczytaj.clicked.connect(self.dodaj_warstwe)

        self.pushButton_odznacz.clicked.connect(self.czyszczenie_wyboru_punktow)

    def resetowanie_a(self):
        self.listWidget.clear()
        self.plainTextEdit_wyniki.clear()
        checkboxes = [self.checkBox_pl2000, self.checkBox_pl1992, self.checkBox_s5, self.checkBox_s6, self.checkBox_s7, self.checkBox_s8, self.checkBox_a, self.checkBox_ha]
        for checkbox in checkboxes:
            checkbox.setChecked(False)
        self.checkBox_m2.setChecked(True)
        self.lineEdit_nazwa_warstwy.clear()
        self.tableWidget_zawartosc.clear()
        self.mQgsFileWidget_plik.setFilePath(None)
        self.accept()

    def resetowanie_r(self):
        self.listWidget.clear()
        self.plainTextEdit_wyniki.clear()
        checkboxes = [self.checkBox_pl2000, self.checkBox_pl1992, self.checkBox_s5, self.checkBox_s6, self.checkBox_s7, self.checkBox_s8, self.checkBox_a, self.checkBox_ha]
        for checkbox in checkboxes:
            checkbox.setChecked(False)
        self.checkBox_m2.setChecked(True)
        self.lineEdit_nazwa_warstwy.clear()
        self.tableWidget_zawartosc.clear()
        self.mQgsFileWidget_plik.setFilePath(None)
        self.reject()

    def czyszczenie_wyboru_punktow(self):
        warstwa = iface.activeLayer()
        self.listWidget.clear()
        features = warstwa.getFeatures()
        for feature in features:
            warstwa.deselect(feature.id())
            item = QListWidgetItem(f"ID: {feature.id()}")
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.listWidget.addItem(item)

    # wybiera narzędzie do zaznaczania obiektów
    def wybierz_punkty(self):
        layer = iface.activeLayer()
        iface.setActiveLayer(layer)
        iface.actionSelect().trigger()
        
    # czyści okienko tekstowe
    def clear(self):
        self.plainTextEdit_wyniki.clear()

     # minimalizuje okno wtyczki
    def minimalizuj(self):
        self.showMinimized()

    # sprawia że może być wybrane jedno albo drugie(robi to też radioButton, ale działa to tak że tylko jeden może być zaznaczony na całą wtyczke i odznacza pozostałe)
    def odznaczanie_pl(self):
        zaznaczony = self.sender()
        checkboxes = [self.checkBox_pl2000, self.checkBox_pl1992]
        for checkbox in checkboxes:
            if checkbox is not zaznaczony:
                checkbox.setChecked(False)

    # sprawia że tylko jedna strefa będzie wybrana
    def odznaczanie_stref(self):
        zaznaczony = self.sender()
        checkboxes = [self.checkBox_s5, self.checkBox_s6, self.checkBox_s7, self.checkBox_s8]
        for checkbox in checkboxes:
            if checkbox is not zaznaczony:
                checkbox.setChecked(False)

    # sprawia że tylko jedno pole może być zaznaczone
    def odznaczanie_pola(self):
        zaznaczony = self.sender()
        checkboxes = [self.checkBox_a, self.checkBox_m2, self.checkBox_ha]
        for checkbox in checkboxes:
            if checkbox is not zaznaczony:
                checkbox.setChecked(False)

    # ustawia widoczność wyboru opcji rysowania poligonu i wyboru jednostek
    def zmiana_widocznosci_pola(self):
        if self.radioButton_pole.isChecked():
            self.checkBox_a.setVisible(True)
            self.checkBox_m2.setVisible(True)
            self.checkBox_ha.setVisible(True)
            self.checkBox_poligon.setVisible(True)
            self.mFieldComboBox_wybor_atrybutu.setVisible(False)
        else:
            self.checkBox_a.setVisible(False)
            self.checkBox_m2.setVisible(False)
            self.checkBox_ha.setVisible(False)
            self.checkBox_poligon.setVisible(False)
            self.mFieldComboBox_wybor_atrybutu.setVisible(True)

    # pokazuje i ukrywa wybór stref
    def zmiana_widocznosci(self, state):
        if state == 2:
            self.checkBox_s5.setVisible(True)
            self.checkBox_s6.setVisible(True)
            self.checkBox_s7.setVisible(True)
            self.checkBox_s8.setVisible(True)
            self.label_strefa.setVisible(True)
        else:
            self.checkBox_s5.setVisible(False)
            self.checkBox_s6.setVisible(False)
            self.checkBox_s7.setVisible(False)
            self.checkBox_s8.setVisible(False)
            self.label_strefa.setVisible(False)

    # zmienia aktywną warstwę zależnie od wyboru w MapLayer, i ustawia warstwe z której wyświetlane będą atrybuty         
    def zmiana_warstwy(self):
        wybrana_warstwa = self.mMapLayerComboBox_wybor_warstwy.currentLayer()
        self.mMapLayerComboBox_wybor_warstwy.setLayer(wybrana_warstwa)
        self.mFieldComboBox_wybor_atrybutu.setLayer(wybrana_warstwa)
        self.mFieldComboBox_wybor_atrybutu.currentField()
        iface.setActiveLayer(wybrana_warstwa)
        if wybrana_warstwa == None:
            self.listWidget.clear()
        else:
            self.czyszczenie_wyboru_punktow()

        # otwiera plik
    def open_file(self, file_path):
        if file_path:
            try:
                with open(file_path, 'r') as plik:
                    zawartosc = plik.readlines()
                    self.wgraj_do_tabeli(zawartosc)
            except Exception as e:
                print(f'Blad podczas otwierania pliku: {str(e)}')

    # dodaje warstwe i ustawia EPSG zależnie od wyboru
    def dodaj_warstwe(self):
        zawartosc = []
        for wiersze in range(self.tableWidget_zawartosc.rowCount()):
            wartosci = []
            for kolumny in range(self.tableWidget_zawartosc.columnCount()):
                item = self.tableWidget_zawartosc.item(wiersze, kolumny)
                if item:
                    wartosci.append(item.text())
                else:
                    wartosci.append('')
            zawartosc.append(','.join(wartosci))
        nazwa_warstwy = self.lineEdit_nazwa_warstwy.text()
        
        if self.checkBox_pl1992.isChecked() == True:
            epsg = 2180
        elif self.checkBox_pl2000.isChecked() == True:
            if self.checkBox_s5.isChecked() == True:
                epsg = 2176
            elif self.checkBox_s6.isChecked() == True:
                epsg = 2177
            elif self.checkBox_s7.isChecked() == True:
                epsg = 2178
            elif self.checkBox_s8.isChecked() == True:
                epsg = 2179
            else:
                QgsMessageLog.logMessage("Nie wybrano strefy")
                epsg = None
        else:
            QgsMessageLog.logMessage("Nie wybrano strefy")
            epsg = None

        fields = QgsFields()
        fields.append(QgsField('NR', QVariant.Int))
        fields.append(QgsField('X', QVariant.Double))
        fields.append(QgsField('Y', QVariant.Double))
        fields.append(QgsField('H', QVariant.Double))

        crs = QgsCoordinateReferenceSystem('EPSG:'+str(epsg))

        warstwa = QgsVectorLayer('Point?crs='+crs.toWkt(), f'{nazwa_warstwy}', 'memory')
        warstwa.dataProvider().addAttributes(fields.toList())
        warstwa.updateFields()
        
        features = []
        for i, line in enumerate(zawartosc):
            wartosci = line.strip().split(',')
            nr = float(wartosci[0])
            x = float(wartosci[1])
            y = float(wartosci[2])
            h = float(wartosci[3])
            feature = QgsFeature(fields)
            feature.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(y, x)))
            feature.setAttributes([nr, y, x, h])
            features.append(feature)

        warstwa.dataProvider().addFeatures(features)

        QgsProject.instance().addMapLayer(warstwa)

    # wgrywa dane z pliku do tabeli która pokazuje dane
    def wgraj_do_tabeli(self, zawartosc):
        self.tableWidget_zawartosc.clear()

        wiersze = len(zawartosc)
        if wiersze > 0:
            kolumny = len(zawartosc[0].split(' '))
        else:
            kolumny = 0

        self.tableWidget_zawartosc.setRowCount(wiersze)
        self.tableWidget_zawartosc.setColumnCount(kolumny)
        
        l = 0
        for i, line in enumerate(zawartosc):
            wartosci = line.strip().split(' ')
            for j, wartosc in enumerate(wartosci):
                item = QtWidgets.QTableWidgetItem(wartosc)
                self.tableWidget_zawartosc.setItem(i, j, item)

    # część obliczeniowa
    def oblicz(self):
        layer = iface.activeLayer()
        selected_features = layer.selectedFeatures()

        selected_ids = []
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            if item.checkState() == Qt.Checked:
                selected_ids.append(int(item.text().split(":")[1].strip()))

        for feature in layer.getFeatures():
            if feature.id() in selected_ids:
                selected_features.append(feature)

        if self.radioButton_dH.isChecked() == True:
            if len(selected_features) != 2:
                QgsMessageLog.logMessage("Prosze wybrac 2 punkty.")
                return

            feature1 = selected_features[0]
            feature2 = selected_features[1]

            atrybut = self.mFieldComboBox_wybor_atrybutu.currentField()

            wysokosc1 = feature1.attribute(atrybut)
            wysokosc2 = feature2.attribute(atrybut)
            id1 = feature1.id()
            id2 = feature2.id()
            if wysokosc1 is None or wysokosc2 is None:
                QgsMessageLog.logMessage("Wybrane punkty nie maja okreslonej wysokosci.")
                return
            elif type(wysokosc1) in (int,float) == False or type(wysokosc2) in (int,float) == False:
                QgsMessageLog.logMessage("Wybrane atrybuty nie mają wartości liczbowej.")
                return
            elif type(wysokosc1) == str or type(wysokosc2) == str:
                QgsMessageLog.logMessage("Wybrane atrybuty nie mają wartości liczbowej.")
                return

            dH = round(wysokosc2 - wysokosc1,5)

            wiadomosc = f'Różnica wysokosci miedzy punktami o ID: {id1} o H = {wysokosc1} [m] oraz {id2} o H = {wysokosc2} [m] wynosi: {dH} [m], natomiast między punktami o ID: {id2} o H = {wysokosc2} [m] oraz {id1} o H = {wysokosc1} [m] wynosi: {-dH} [m]'
            self.plainTextEdit_wyniki.appendPlainText(wiadomosc)
            iface.messageBar().pushMessage(wiadomosc)
            
        elif self.radioButton_pole.isChecked() == True:
            #layer = iface.activeLayer()
            #selected_features = layer.selectedFeatures()
            if len(selected_features) < 3:
                QgsMessageLog.logMessage("Prosze wybrac minimum 3 punkty.")
                return
            
            wsp2 = []
            for feature in selected_features:
                geom = feature.geometry()
                geomSingleType = QgsWkbTypes.isSingleType(geom.wkbType())
                if geom.type() == QgsWkbTypes.PointGeometry:
                    if geomSingleType:
                        x = geom.asPoint().x()
                        y = geom.asPoint().y()
                        wsp2.append((x,y))
                else:
                    QgsMessageLog.logMessage("Niepoprawna geometria")
            
            wsp = sorted(wsp2, key=lambda p: p[1])

            pole = 0.0
            n = len(wsp) 
            for i in range(n):
                j = (i + 1) % n
                pole += wsp[i][0] * wsp[j][1]
                pole -= wsp[j][0] * wsp[i][1]

            pole = abs(pole/2)


            if self.checkBox_ha.isChecked() == True:
                pole = pole/10000
                jednostka = 'ha'
            elif self.checkBox_m2.isChecked() == True:
                jednostka = 'm2'
            elif self.checkBox_a.isChecked() == True:
                pole = pole/100
                
                jednostka = 'a'
            else:
                QgsMessageLog.logMessage("Niewybrano jednostki, domyślna to metry")
                jednostka = 'm2'

            pole_gauss = pole
            id = ''
            for i in selected_features:
                id = id + str(i.id()) + ', '
                
                
            if n > 4:
                wiadomosc = f'Pole powierzchni figury o liczbie wierzchołków większej niż 4 może prowadzić do błędnych wyników.'
            else:
                wiadomosc = f'Pole powierzchni figury o wierzchołkach w punktach o ID:{id} wynosi: {round(pole,3)} {jednostka}'
            self.plainTextEdit_wyniki.appendPlainText(wiadomosc)
            iface.messageBar().pushMessage(wiadomosc)

            if self.checkBox_poligon.isChecked() == True:
                poligon_punkty = [QgsPointXY(x, y) for x, y in wsp2]
                #poligon = QgsGeometry.fromPolygonXY([polygon])
                poligon = QgsGeometry.fromMultiPointXY(poligon_punkty).convexHull()
                projekt = QgsProject.instance()
                crs = layer.crs()
                epsg = crs.authid()

                warstwa_poligon_nazwa = 'poligon'
                warstwa_poligon = QgsVectorLayer('Polygon?crs='+str(epsg), warstwa_poligon_nazwa, 'memory')
                provider = warstwa_poligon.dataProvider()
                fields = QgsFields()
                fields.append(QgsField('Pole_Poligon', QVariant.Double))
                fields.append(QgsField('Pole_Gauss', QVariant.Double))
                provider.addAttributes(fields)
                warstwa_poligon.updateFields()

                feature = QgsFeature(fields)
                feature.setGeometry(poligon)
                feature.setAttributes([poligon.area(), pole])
                
                provider.addFeature(feature)
                warstwa_poligon.updateExtents()

                QgsProject.instance().addMapLayer(warstwa_poligon)

                pole = poligon.area()

                if self.checkBox_ha.isChecked() == True:
                    pole = pole/10000
                    jednostka = 'ha'
                elif self.checkBox_m2.isChecked() == True:
                    jednostka = 'm2'
                elif self.checkBox_a.isChecked() == True:
                    pole = pole/100
                    jednostka = 'a'
                else:
                    QgsMessageLog.logMessage("Niewybrano jednostki, domyślna to metry")
                    jednostka = 'm2'
                   

                wiadomosc2 = f'Pole powierzchni(geometry().area()) figury o wierzchołkach w punktach o ID:{id} wynosi: {round(pole,3)} {jednostka}.  '
                self.plainTextEdit_wyniki.appendPlainText(wiadomosc2)
                iface.messageBar().pushMessage(wiadomosc2)
                if abs(pole_gauss- pole) >= 0.0000001:
                    wiadomosc3 = f'Pole powierzchni(geometry().area()) figury o wierzchołkach w punktach o ID:{id} oraz pole obliczone metodą Gaussa są różne. Nastąpił błąd opisany dokładniej w readme'
                    self.plainTextEdit_wyniki.appendPlainText(wiadomosc3)
                    iface.messageBar().pushMessage(wiadomosc3)



                iface.setActiveLayer(layer)
