# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1018, 698)
        font = QtGui.QFont()
        font.setPointSize(11)
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("list.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.lne_ingresar_cliente = QtWidgets.QLineEdit(self.centralWidget)
        self.lne_ingresar_cliente.setGeometry(QtCore.QRect(70, 80, 621, 31))
        self.lne_ingresar_cliente.setToolTip("")
        self.lne_ingresar_cliente.setInputMethodHints(QtCore.Qt.ImhNone)
        self.lne_ingresar_cliente.setObjectName("lne_ingresar_cliente")
        self.lbl_ingresar_cliente = QtWidgets.QLabel(self.centralWidget)
        self.lbl_ingresar_cliente.setGeometry(QtCore.QRect(70, 40, 151, 31))
        self.lbl_ingresar_cliente.setObjectName("lbl_ingresar_cliente")
        self.cbx_trabajo_realizado = QtWidgets.QComboBox(self.centralWidget)
        self.cbx_trabajo_realizado.setEnabled(False)
        self.cbx_trabajo_realizado.setGeometry(QtCore.QRect(70, 240, 621, 31))
        self.cbx_trabajo_realizado.setCurrentText("")
        self.cbx_trabajo_realizado.setMaxVisibleItems(15)
        self.cbx_trabajo_realizado.setObjectName("cbx_trabajo_realizado")
        self.cbx_trabajo_realizado.addItem("")
        self.cbx_trabajo_realizado.addItem("")
        self.cbx_trabajo_realizado.addItem("")
        self.cbx_trabajo_realizado.addItem("")
        self.cbx_trabajo_realizado.addItem("")
        self.cbx_trabajo_realizado.addItem("")
        self.cbx_trabajo_realizado.addItem("")
        self.btn_agregar_a_lista = QtWidgets.QToolButton(self.centralWidget)
        self.btn_agregar_a_lista.setEnabled(False)
        self.btn_agregar_a_lista.setGeometry(QtCore.QRect(830, 240, 41, 31))
        self.btn_agregar_a_lista.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("add2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_agregar_a_lista.setIcon(icon1)
        self.btn_agregar_a_lista.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.btn_agregar_a_lista.setObjectName("btn_agregar_a_lista")
        self.tbl_lista_trabajos_realizados = QtWidgets.QTableWidget(self.centralWidget)
        self.tbl_lista_trabajos_realizados.setEnabled(False)
        self.tbl_lista_trabajos_realizados.setGeometry(QtCore.QRect(70, 300, 881, 241))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.tbl_lista_trabajos_realizados.setFont(font)
        self.tbl_lista_trabajos_realizados.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tbl_lista_trabajos_realizados.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tbl_lista_trabajos_realizados.setObjectName("tbl_lista_trabajos_realizados")
        self.tbl_lista_trabajos_realizados.setColumnCount(3)
        self.tbl_lista_trabajos_realizados.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_lista_trabajos_realizados.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_lista_trabajos_realizados.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_lista_trabajos_realizados.setHorizontalHeaderItem(2, item)
        self.tbl_lista_trabajos_realizados.horizontalHeader().setCascadingSectionResizes(True)
        self.tbl_lista_trabajos_realizados.horizontalHeader().setDefaultSectionSize(150)
        self.tbl_lista_trabajos_realizados.horizontalHeader().setStretchLastSection(True)
        self.lbl_detalle_trabajos_realizados = QtWidgets.QLabel(self.centralWidget)
        self.lbl_detalle_trabajos_realizados.setEnabled(False)
        self.lbl_detalle_trabajos_realizados.setGeometry(QtCore.QRect(70, 190, 281, 31))
        self.lbl_detalle_trabajos_realizados.setObjectName("lbl_detalle_trabajos_realizados")
        self.btn_imprimir = QtWidgets.QToolButton(self.centralWidget)
        self.btn_imprimir.setEnabled(False)
        self.btn_imprimir.setGeometry(QtCore.QRect(400, 570, 221, 71))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("print.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_imprimir.setIcon(icon2)
        self.btn_imprimir.setIconSize(QtCore.QSize(50, 50))
        self.btn_imprimir.setObjectName("btn_imprimir")
        self.btn_quitar_de_lista = QtWidgets.QToolButton(self.centralWidget)
        self.btn_quitar_de_lista.setEnabled(False)
        self.btn_quitar_de_lista.setGeometry(QtCore.QRect(910, 240, 41, 31))
        self.btn_quitar_de_lista.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("remove.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_quitar_de_lista.setIcon(icon3)
        self.btn_quitar_de_lista.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.btn_quitar_de_lista.setObjectName("btn_quitar_de_lista")
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        self.cbx_trabajo_realizado.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Generador de comprobantes"))
        self.lbl_ingresar_cliente.setText(_translate("MainWindow", "Ingresar cliente"))
        self.cbx_trabajo_realizado.setItemText(0, _translate("MainWindow", "Reparación"))
        self.cbx_trabajo_realizado.setItemText(1, _translate("MainWindow", "Instalación"))
        self.cbx_trabajo_realizado.setItemText(2, _translate("MainWindow", "Formateo"))
        self.cbx_trabajo_realizado.setItemText(3, _translate("MainWindow", "Configuración"))
        self.cbx_trabajo_realizado.setItemText(4, _translate("MainWindow", "Actualización"))
        self.cbx_trabajo_realizado.setItemText(5, _translate("MainWindow", "Cambio"))
        self.cbx_trabajo_realizado.setItemText(6, _translate("MainWindow", "Limpieza"))
        self.btn_agregar_a_lista.setToolTip(_translate("MainWindow", "Agregar a la lista"))
        self.btn_agregar_a_lista.setText(_translate("MainWindow", "Buscar"))
        item = self.tbl_lista_trabajos_realizados.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Trabajo"))
        item = self.tbl_lista_trabajos_realizados.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Precio"))
        item = self.tbl_lista_trabajos_realizados.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Detalle"))
        self.lbl_detalle_trabajos_realizados.setText(_translate("MainWindow", "Detalle de trabajos realizados"))
        self.btn_imprimir.setToolTip(_translate("MainWindow", "Imprimir comprobante"))
        self.btn_imprimir.setText(_translate("MainWindow", "Imprimir"))
        self.btn_quitar_de_lista.setToolTip(_translate("MainWindow", "Quitar de la lista"))
        self.btn_quitar_de_lista.setText(_translate("MainWindow", "Quitar"))

