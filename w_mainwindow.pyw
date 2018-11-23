import sys
import os
import re
import subprocess
import datetime
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import QPersistentModelIndex
from mainwindow import Ui_MainWindow
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import Spacer, SimpleDocTemplate, Table, TableStyle, Paragraph, Image


class VentanaPrincipal(QMainWindow):
    obj_main = Ui_MainWindow()
    columna_trabajo = 0
    columna_precio = 1
    columna_descripcion = 2

    def __init__(self):
        QMainWindow.__init__(self)
        self.obj_main.setupUi(self)

        self.obj_main.lne_ingresar_cliente.textChanged.connect(self.verificar_cliente)
        self.obj_main.lne_ingresar_cliente.textChanged.connect(self.habilitar_btn_agregar)
        self.obj_main.cbx_trabajo_realizado.currentIndexChanged.connect(self.habilitar_btn_agregar)
        self.obj_main.btn_agregar_a_lista.clicked.connect(self.cbx_seleccion_item)
        self.obj_main.tbl_lista_trabajos_realizados.itemSelectionChanged.connect(self.habilitar_btn_imprimir)
        self.obj_main.lne_ingresar_cliente.textChanged.connect(self.habilitar_btn_imprimir)
        self.obj_main.tbl_lista_trabajos_realizados.itemSelectionChanged.connect(self.habilitar_btn_quitar)
        self.obj_main.tbl_lista_trabajos_realizados.clicked.connect(self.comprobar_columna_precio)
        self.obj_main.btn_quitar_de_lista.clicked.connect(self.eliminar_item)
        self.obj_main.btn_imprimir.clicked.connect(self.imprimir_comprobante)

    def verificar_cliente(self):
        nombre_cliente = self.obj_main.lne_ingresar_cliente.text()
        if not re.match("^[ A-Za-zÁÄÉËÍÏÑÓÖÚÜáäéëíïñóöúü]*$", nombre_cliente):
            QMessageBox.critical(self, "Error", "Sólo se aceptan letras y espacios.")
        else:
            if len(nombre_cliente.strip()) < 5:
                self.obj_main.cbx_trabajo_realizado.setCurrentIndex(-1)
                self.obj_main.cbx_trabajo_realizado.setEnabled(False)
                self.obj_main.lbl_detalle_trabajos_realizados.setEnabled(False)
                self.obj_main.tbl_lista_trabajos_realizados.setEnabled(False)
                self.obj_main.btn_imprimir.setEnabled(False)
                self.obj_main.btn_agregar_a_lista.setEnabled(False)
                self.obj_main.btn_quitar_de_lista.setEnabled(False)
            else:
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
        row_position = self.obj_main.tbl_lista_trabajos_realizados.rowCount()
        self.obj_main.tbl_lista_trabajos_realizados.insertRow(row_position)
        self.obj_main.tbl_lista_trabajos_realizados.setItem(row_position, self.columna_trabajo, QTableWidgetItem(trabajo))
        self.obj_main.tbl_lista_trabajos_realizados.setItem(row_position, self.columna_precio, QTableWidgetItem(""))
        self.obj_main.tbl_lista_trabajos_realizados.setItem(row_position, self.columna_descripcion, QTableWidgetItem(""))

    def habilitar_btn_imprimir(self):
        if self.obj_main.lne_ingresar_cliente.text() != "":
            contador = 0
            tabla = self.obj_main.tbl_lista_trabajos_realizados
            cantidad_filas = tabla.rowCount()
            if cantidad_filas == 0:
                self.obj_main.cbx_trabajo_realizado.setCurrentIndex(-1)
                self.obj_main.btn_imprimir.setEnabled(False)
            else:
                for item in range(cantidad_filas):
                    if tabla.item(item, self.columna_precio).text() == "":
                        self.obj_main.btn_imprimir.setEnabled(False)
                    else:
                        contador = contador + 1
                        self.obj_main.btn_imprimir.setEnabled(True)
                if contador == cantidad_filas:
                    self.obj_main.btn_imprimir.setEnabled(True)
                else:
                    self.obj_main.btn_imprimir.setEnabled(False)

    def habilitar_btn_quitar(self):
        if self.obj_main.tbl_lista_trabajos_realizados.selectedItems():
            self.obj_main.btn_quitar_de_lista.setEnabled(True)
        else:
            self.obj_main.btn_quitar_de_lista.setEnabled(False)

    def eliminar_item(self):
        indexes = [QPersistentModelIndex(index) for index in self.obj_main.tbl_lista_trabajos_realizados.selectionModel().selectedRows()]
        for index in indexes:
            self.obj_main.tbl_lista_trabajos_realizados.removeRow(index.row())
        self.habilitar_btn_imprimir()

    def comprobar_columna_precio(self):
        comprobar = True
        tabla = self.obj_main.tbl_lista_trabajos_realizados
        cantidad_filas = tabla.rowCount()
        for item in range(cantidad_filas):
            if not re.match("^[0-9]*$", tabla.item(item, self.columna_precio).text()):
                QMessageBox.critical(self, "Error", "Por favor, ingrese precio en cada fila de la tabla."
                                                    "Solo se aceptan números en columna precio.")
                comprobar = False
            else:
                continue
        return comprobar

    def imprimir_comprobante(self):
        if self.obj_main.lne_ingresar_cliente.text() == "":
            QMessageBox.information(self, "Advertencia", "Ingrese el nombre del cliente.")
        else:
            if self.comprobar_columna_precio() == True:
                documento_pdf = []

                fec_hoy = datetime.date.today()
                hoy = fec_hoy.strftime("%d/%m/%Y")
                nombre_cliente = str(self.obj_main.lne_ingresar_cliente.text())

                style_sheet = getSampleStyleSheet()
                img = Image("python_logo.png", 30, 30)

                documento_pdf.append(Spacer(0, 50))

                estilo_monto_total = ParagraphStyle('', fontSize=10, textColor='#000', rightIndent=0, alignment=TA_CENTER)
                estilo_encabezado_2 = ParagraphStyle('', fontSize=10, textColor='#000', alignment=TA_CENTER)
                estilo_encabezado_1 = ParagraphStyle('', fontSize=6, textColor='#000', alignment=TA_CENTER)
                estilo_texto = ParagraphStyle('', fontSize=8, alignment=0, spaceBefore=0, spaceAfter=0, textColor='#000',
                                              leftIndent=0)

                encabezado1 = [Paragraph("<b>Calle Falsa 123 - Tel.: (2920) 321654 / Cel.: (2920) 15 513322</b><br/><b> "
                                         + "C. de Patagones - Buenos Aires - E-mail: mimail@outlook.com</b>",
                                         estilo_encabezado_1)]

                encabezado2a = [Paragraph("<b>COMPROBANTE N° " + str(123456789) + "</b>", estilo_encabezado_2)]

                encabezado2b = [Paragraph("<b>Fecha:   " + str(hoy) + "</b>", estilo_encabezado_2)]

                t_encabezado = [[img, encabezado2a], [encabezado1, encabezado2b]]  # Tabla de 2 filas y 2 columnas

                tabla_encabezado = Table(t_encabezado, 242.5)
                tabla_encabezado.setStyle(TableStyle([
                    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.transparent),  # Setea todas las líneas interiores sin color
                    ('ALIGNMENT', (0, 0), (0, 0), 'CENTER'),  # Centra horizontalmente la imagen
                    ('TOPPADDING', (0, 0), (0, 0), 13),  # Padding superior de la celda
                    ('BOTTOMPADDING', (0, 1), (-1, 1), 13),  # Padding inferior de la celda
                    ('LINEBEFORE', (1, 0), (1, -1), 1, colors.black),  # Colorea solamente la línea del medio
                    ('BOX', (0, 0), (-1, -1), 1, colors.black),
                    ('BACKGROUND', (0, 0), (-1, 1), colors.transparent),
                    ('BACKGROUND', (1, 1), (-1, 1), colors.transparent),
                    ('VALIGN', (0, 1), (-1, 1), 'TOP')  # Alínea el texto de la celda bien cerca del borde superior de la misma
                ]))
                documento_pdf.append(tabla_encabezado)

                documento_pdf.append(Spacer(0, -17.5))
                t_cliente = [[Paragraph('''<font size=8> <b> </b></font>''', style_sheet["BodyText"])],
                             [Paragraph('<font size=8> <b>Cliente: ' + nombre_cliente + '</b></font>', estilo_texto)]]

                tabla_cliente = Table(t_cliente, 485)
                tabla_cliente.setStyle(TableStyle([
                    ('INNERGRID', (0, 1), (-1, -1), 0.25, colors.black),
                    ('BOX', (0, 1), (-1, -1), 0.25, colors.black),
                    ('BACKGROUND', (0, 1), (-1, 1), colors.white)
                ]))
                documento_pdf.append(tabla_cliente)

                trabajos = [[Paragraph('''<font size=9> <b> </b></font>''', style_sheet["BodyText"])],
                            [Paragraph('''<font size=9> <b> </b>Trabajo realizado</font>''', estilo_texto),
                             Paragraph('''<font size=9> <b> </b>Monto</font>''', estilo_texto),
                             Paragraph('''<font size=9> <b> </b>Detalle</font>''', estilo_texto),
                             Paragraph('''<font size=9> <b> </b>SUBTOTAL</font>''', estilo_texto)]]

                tabla = self.obj_main.tbl_lista_trabajos_realizados
                cantidad_filas = tabla.rowCount()
                importe_total = 0
                tabla_lista_trabajos = []

                for item in range(cantidad_filas):
                    # Item es el número de fila; self.columna_trabajo es la columna
                    trabajo = tabla.item(item, self.columna_trabajo).text()
                    precio = tabla.item(item, self.columna_precio).text()
                    detalle = tabla.item(item, self.columna_descripcion).text()

                    importe_total = importe_total + int(precio)

                    estilotrabajo = " <font size=8>" + str(trabajo) + "</font>"
                    estiloprecio = " <font size=8>" + str(precio) + "</font>"
                    estilodetalle = " <font size=8>" + str(detalle) + "</font>"
                    estilosubtotal = " <font size=8>" + str(precio) + "</font>"

                    trabajos.append([Paragraph(estilotrabajo, estilo_texto),
                                     Paragraph(estiloprecio, estilo_texto),
                                     Paragraph(estilodetalle, estilo_texto),
                                     Paragraph(estilosubtotal, estilo_texto)])

                    tabla_lista_trabajos = Table(trabajos, (85, 40, 300, 60))
                    tabla_lista_trabajos.setStyle(TableStyle([
                        ('INNERGRID', (0, 1), (-1, -1), 0.25, colors.black),
                        ('BOX', (0, 1), (-1, -1), 0.25, colors.white),
                        ('BACKGROUND', (0, 1), (-1, 1), colors.white)
                    ]))

                documento_pdf.append(tabla_lista_trabajos)

                monto_total = [[Paragraph('''<font size=8> <b> </b></font>''', style_sheet["BodyText"]),
                          Paragraph("", estilo_monto_total),
                          Paragraph("", estilo_monto_total),
                          Paragraph("<b>TOTAL: $" + str(importe_total) + " </b>", estilo_monto_total)]]

                importe_final = Table(monto_total, (65, 20, 300, 100))  # Tabla de 4 columnas para poder personalizar
                                                                        # cómodamente la última celda, que tiene el total

                importe_final.setStyle(TableStyle([
                    ('BOX', (-1, -1), (-1, -1), 0.25, colors.lightgrey),
                    ('BACKGROUND', (-1, -1), (-1, -1), colors.lightgrey)
                ]))
                documento_pdf.append(importe_final)

                documento_pdf.append(Spacer(0, 50))

                # Duplicado

                documento_pdf.append(tabla_encabezado)
                documento_pdf.append(Spacer(0, -17.5))
                documento_pdf.append(tabla_cliente)
                documento_pdf.append(tabla_lista_trabajos)
                documento_pdf.append(importe_final)

                # Define dónde se guardará el archivo

                fecha_de_hoy = str(datetime.date.today().day) + "-" + str(datetime.date.today().month) + "-"\
                               + str(datetime.date.today().year)

                file_path = os.path.dirname(os.path.abspath(__file__)) + "/pdf/" + fecha_de_hoy

                if not os.path.exists(file_path):
                    os.makedirs(file_path)

                doc = SimpleDocTemplate(file_path + "/comprobante " + str(nombre_cliente) + " "
                    + fecha_de_hoy
                    + ".pdf", pagesize=A4, rightMargin=14, leftMargin=14, topMargin=5, bottomMargin=18)
                doc.build(documento_pdf)

                QMessageBox.information(self, "Acción realizada", "Se ha generado el comprobante.")

                if sys.platform == 'linux':
                    subprocess.call(["xdg-open", file_path + "/comprobante " + str(nombre_cliente) + " " + fecha_de_hoy + ".pdf"])
                else:
                    os.startfile(file_path + "/comprobante " + str(nombre_cliente) + " " + fecha_de_hoy + ".pdf")


app = QApplication(sys.argv)
window = VentanaPrincipal()
window.show()
app.exec_()
