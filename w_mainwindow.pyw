import sys, os, re, subprocess, datetime
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import QPersistentModelIndex
from mainwindow import Ui_MainWindow
from reportlab import *
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from reportlab.platypus import Spacer, SimpleDocTemplate, Table, TableStyle, Paragraph, Image

class VentanaPrincipal(QMainWindow):
    obj_main = Ui_MainWindow()

    def __init__(self):
        QMainWindow.__init__(self)
        self.obj_main.setupUi(self)

        self.obj_main.btn_establecer_cliente.clicked.connect(self.establecer_cliente)
        self.obj_main.cbx_trabajo_realizado.currentIndexChanged.connect(self.habilitar_btn_agregar)
        self.obj_main.btn_agregar_a_lista.clicked.connect(self.cbx_seleccion_item)
        self.obj_main.tbl_lista_trabajos_realizados.clicked.connect(self.habilitar_btn_imprimir)
        self.obj_main.tbl_lista_trabajos_realizados.cellClicked.connect(self.habilitar_btn_quitar)
        self.obj_main.btn_quitar_de_lista.clicked.connect(self.eliminar_item)
        self.obj_main.btn_imprimir.clicked.connect(self.imprimir_comprobante)

    def establecer_cliente(self):
        nombre_cliente = self.obj_main.lne_ingresar_cliente.text()
        if nombre_cliente == "":
            QMessageBox.information(self, "Advertencia", "Ingrese el nombre del cliente.")
        if not re.match("^[ A-Za-zÁÄÉËÍÏÑÓÖÚÜáäéëíïñóöúü]*$", nombre_cliente):
            QMessageBox.critical(self, "Error", "Sólo se aceptan letras y espacios.")
        else:
            self.obj_main.lne_mostrar_cliente.setText(nombre_cliente.strip().upper())
            self.obj_main.lne_ingresar_cliente.setText("")

            self.obj_main.lbl_detalle_trabajos_realizados.setEnabled(True)
            self.obj_main.cbx_trabajo_realizado.setEnabled(True)
            self.obj_main.tbl_lista_trabajos_realizados.setEnabled(True)

    def habilitar_btn_agregar(self):
        index = self.obj_main.cbx_trabajo_realizado.currentIndex()
        if index == -1:
            self.obj_main.btn_agregar_a_lista.setEnabled(False)
        else:
            self.obj_main.btn_agregar_a_lista.setEnabled(True)

    def cbx_seleccion_item(self):
        trabajo = self.obj_main.cbx_trabajo_realizado.currentText()
        rowPosition = self.obj_main.tbl_lista_trabajos_realizados.rowCount()
        self.obj_main.tbl_lista_trabajos_realizados.insertRow(rowPosition)
        self.obj_main.tbl_lista_trabajos_realizados.setItem(rowPosition, 0, QTableWidgetItem(trabajo))
        self.obj_main.tbl_lista_trabajos_realizados.setItem(rowPosition, 1, QTableWidgetItem(""))
        self.obj_main.tbl_lista_trabajos_realizados.setItem(rowPosition, 2, QTableWidgetItem(""))

    def habilitar_btn_imprimir(self):
        if self.obj_main.tbl_lista_trabajos_realizados.rowCount() > 0:
            self.obj_main.btn_imprimir.setEnabled(True)
        else:
            self.obj_main.btn_imprimir.setEnabled(False)

    def habilitar_btn_quitar(self):
        self.obj_main.btn_quitar_de_lista.setEnabled(True)

    def eliminar_item(self):
        indexes = [QPersistentModelIndex(index) for index in self.obj_main.tbl_lista_trabajos_realizados.selectionModel().selectedRows()]
        for index in indexes:
            self.obj_main.tbl_lista_trabajos_realizados.removeRow(index.row())

    def limpiar(self):
        #vaciar tabla
        self.obj_main.tbl_lista_trabajos_realizados.clear()

        #limpiar resto de los campos
        self.obj_main.cbx_trabajo_realizado.setCurrentIndex(-1)

    def imprimir_comprobante(self):
        story = []

        fec_hoy = datetime.date.today()
        hoy = fec_hoy.strftime("%d/%m/%Y")
        nombre_cliente = str(self.obj_main.lne_mostrar_cliente.text())

        styleSheet = getSampleStyleSheet()
        img = Image("ccs-wing.png", 30, 30)

        story.append(Spacer(0, 50))

        estilo_total = ParagraphStyle('', fontSize=10, textColor='#000', rightIndent=0,alignment=TA_CENTER)
        texto_secundario = ParagraphStyle('', fontSize=10, textColor='#000', alignment=TA_CENTER)
        estilo_encabezado1 = ParagraphStyle('', fontSize=6, textColor='#000', alignment=TA_CENTER)
        estilo_texto = ParagraphStyle('',
                                      fontSize=8,
                                      alignment=0,
                                      spaceBefore=0,
                                      spaceAfter=0,
                                      # backColor = '#fff',
                                      textColor='#000',
                                      leftIndent=0)

        encabezado1 = [Paragraph("<b>Calle Falsa 123 - Tel.: (2920) 321654 / Cel.: (2920) 15 513322</b><br/><b> C. de Patagones - Buenos Aires - E-mail: mimail@outlook.com</b>",estilo_encabezado1)]

        encabezado2a = [Paragraph("<b>COMPROBANTE N° " + str(123456789) + "</b>", texto_secundario)]

        encabezado2b = [Paragraph("<b>Fecha:   " + str(hoy) + "</b>",texto_secundario)]

        header = [[img, encabezado2a], [encabezado1, encabezado2b]] #tabla de 2 filas y 2 columnas

        theader = Table(header, (242.5))
        theader.setStyle(TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.transparent), #setea todas las líneas interiores sin color
            ('ALIGNMENT', (0, 0), (0, 0), 'CENTER'), #centra horizontalmente la imagen
            ('TOPPADDING', (0, 0), (0, 0), 13), #padding superior de la celda
            ('BOTTOMPADDING', (0, 1), (-1, 1), 13), #padding inferior de la celda
            ('LINEBEFORE', (1, 0), (1, -1), 1, colors.black), #colorea solamente la línea del medio
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (-1, 1), colors.transparent),
            ('BACKGROUND', (1, 1), (-1, 1), colors.transparent),
            ('VALIGN', (0, 1), (-1, 1), 'TOP') #alínea el texto de la celda bien cerca del borde superior de la misma
        ]))
        story.append(theader)

        story.append(Spacer(0, -17.5))
        t_cliente = [[Paragraph('''<font size=8> <b> </b></font>''', styleSheet["BodyText"])],
                   [Paragraph('<font size=8> <b>Cliente: ' + nombre_cliente + '</b></font>',estilo_texto)]]

        tcliente = Table(t_cliente, (485))
        tcliente.setStyle(TableStyle([
            ('INNERGRID', (0, 1), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 1), (-1, -1), 0.25, colors.black),
            ('BACKGROUND', (0, 1), (-1, 1), colors.white)
        ]))
        story.append(tcliente)

        trabajos = [[Paragraph('''<font size=9> <b> </b></font>''', styleSheet["BodyText"])],
                       [Paragraph('''<font size=9> <b> </b>Trabajo realizado</font>''', estilo_texto),
                        Paragraph('''<font size=9> <b> </b>Monto</font>''', estilo_texto),
                        Paragraph('''<font size=9> <b> </b>Detalle</font>''', estilo_texto),
                        Paragraph('''<font size=9> <b> </b>SUBTOTAL</font>''', estilo_texto)]]

        tabla = self.obj_main.tbl_lista_trabajos_realizados
        cantidad_filas = tabla.rowCount()
        importe_total = 0

        for item in range(cantidad_filas):
            trabajo = tabla.item(item, 0).text()  # item es el número de fila; 0 es la columna
            precio = tabla.item(item, 1).text()
            detalle = tabla.item(item, 2).text()

            importe_total = importe_total + int(precio)

            estilotrabajo = " <font size=8>" + str(trabajo) + "</font>"
            estiloprecio = " <font size=8>" + str(precio) + "</font>"
            estilodetalle = " <font size=8>" + str(detalle) + "</font>"
            estilosubtotal = " <font size=8>" + str(precio) + "</font>"

            trabajos.append([Paragraph(estilotrabajo, estilo_texto),
                                Paragraph(estiloprecio, estilo_texto),
                                Paragraph(estilodetalle, estilo_texto),
                                Paragraph(estilosubtotal, estilo_texto)])

            t_lista_trabajos = Table(trabajos, (85, 40, 300, 60))
            t_lista_trabajos.setStyle(TableStyle([
                ('INNERGRID', (0, 1), (-1, -1), 0.25, colors.black),
                ('BOX', (0, 1), (-1, -1), 0.25, colors.white),
                ('BACKGROUND', (0, 1), (-1, 1), colors.white)
            ]))

        story.append(t_lista_trabajos)

        total = [[Paragraph('''<font size=8> <b> </b></font>''', styleSheet["BodyText"]),
                      Paragraph("", estilo_total),
                      Paragraph("", estilo_total),
                      Paragraph("<b>TOTAL: $" + str(importe_total) + " </b>", estilo_total)]]

        importe_final = Table(total, (65, 20, 300, 100)) #tabla de 4 columnas para poder customizar más cómodamente la última celda, que tiene el total

        importe_final.setStyle(TableStyle([
            ('BOX', (-1, -1), (-1, -1), 0.25, colors.lightgrey),
            ('BACKGROUND', (-1, -1), (-1, -1), colors.lightgrey)
        ]))
        story.append(importe_final)

        story.append(Spacer(0, 50))

        #Duplicado

        story.append(theader)
        story.append(Spacer(0, -17.5))
        story.append(tcliente)
        story.append(t_lista_trabajos)
        story.append(importe_final)

        #Define dónde se guardará el archivo

        file_path = os.path.dirname(os.path.abspath(__file__)) + "/pdf/" + str(datetime.date.today())

        if not os.path.exists(file_path):
            os.makedirs(file_path)

        doc = SimpleDocTemplate(
            file_path + "/comprobante_" + str(nombre_cliente) + "_" + str(datetime.date.today()) + ".pdf", pagesize=A4,
            rightMargin=14, leftMargin=14, topMargin=5, bottomMargin=18)
        doc.build(story)

        QMessageBox.information(self, "Acción realizada", "Se ha generado el comprobante.")

        if sys.platform == 'linux':
            subprocess.call(["xdg-open", file_path + "/comprobante_" + str(nombre_cliente) + "_" + str(
                datetime.date.today()) + ".pdf"])
        else:
            os.startfile(file_path + "/comprobante_" + str(nombre_cliente) + "_" + str(datetime.date.today()) + ".pdf")


app = QApplication(sys.argv)
window = VentanaPrincipal()
window.show()
app.exec_()
