import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QComboBox, QListWidget, QMessageBox, QFormLayout)
from PyQt5.QtCore import Qt
from datetime import datetime

class GestionGastosApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Gastos Personales")
        self.setGeometry(100, 100, 600, 500)
        
        # Datos de la aplicación
        self.gastos = []
        self.categorias = ["Alimentación", "Transporte", "Salud", "Educación", "Otros"]
        
        # Widget central y layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout_principal = QVBoxLayout(central_widget)
        
        # Título
        titulo = QLabel("Sistema de Gestión de Gastos Personales")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout_principal.addWidget(titulo)
        
        #ingresar gastos
        layout_formulario = QFormLayout()
        
        self.input_descripcion = QLineEdit()
        self.input_descripcion.setPlaceholderText("Ej: Compra supermercado")
        layout_formulario.addRow(QLabel("Descripción:"), self.input_descripcion)
        
        self.input_monto = QLineEdit()
        self.input_monto.setPlaceholderText("Ej: 25.50")
        layout_formulario.addRow(QLabel("Monto ($):"), self.input_monto)
        
        self.combo_categoria = QComboBox()
        self.combo_categoria.addItems(self.categorias)
        layout_formulario.addRow(QLabel("Categoría:"), self.combo_categoria)
        
        layout_principal.addLayout(layout_formulario)
        
        # Botones
        layout_botones = QHBoxLayout()
        
        self.btn_agregar = QPushButton("Agregar Gasto")
        self.btn_agregar.clicked.connect(self.agregar_gasto)
        layout_botones.addWidget(self.btn_agregar)
       
        self.btn_resumen = QPushButton("Ver Resumen")
        self.btn_resumen.clicked.connect(self.mostrar_resumen)
        layout_botones.addWidget(self.btn_resumen)
        
        layout_principal.addLayout(layout_botones)
        
        # Lista de gastos
        layout_principal.addWidget(QLabel("Gastos Registrados:"))
        self.lista_gastos = QListWidget()
        layout_principal.addWidget(self.lista_gastos)
        
        # Etiqueta para el total
        self.etiqueta_total = QLabel("Total gastado: $0.00")
        self.etiqueta_total.setStyleSheet("font-weight: bold; color: red;")
        layout_principal.addWidget(self.etiqueta_total)
        
        # Mostrar ventana
        self.show()
    
    def agregar_gasto(self):
        descripcion = self.input_descripcion.text().strip()
        monto_texto = self.input_monto.text().strip()
        categoria = self.combo_categoria.currentText()
        
        # Validar campos
        if not descripcion or not monto_texto:
            QMessageBox.warning(self, "Campos incompletos", "Por favor, complete todos los campos.")
            return
        
        try:
            monto = float(monto_texto)
            if monto <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Monto inválido", "Por favor, ingrese un monto válido mayor a cero.")
            return
        
        # Crear gasto y agregar a la lista
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        gasto = {
            "descripcion": descripcion,
            "monto": monto,
            "categoria": categoria,
            "fecha": fecha
        }
        self.gastos.append(gasto)
        
        # Actualizar lista visual
        self.actualizar_lista_gastos()
        
        QMessageBox.information(self, "Éxito", "Gasto agregado correctamente.")
    
    def actualizar_lista_gastos(self):
        self.lista_gastos.clear()
        total = 0
        
        for gasto in self.gastos:
            item_texto = f"{gasto['fecha']} - {gasto['descripcion']} - ${gasto['monto']:.2f} ({gasto['categoria']})"
            self.lista_gastos.addItem(item_texto)
            total += gasto['monto']
        
        self.etiqueta_total.setText(f"Total gastado: ${total:.2f}")
    
    def mostrar_resumen(self):
        if not self.gastos:
            QMessageBox.information(self, "Resumen", "No hay gastos registrados.")
            return
        
        resumen = {}
        total = 0
        
        for gasto in self.gastos:
            categoria = gasto['categoria']
            if categoria not in resumen:
                resumen[categoria] = 0
            resumen[categoria] += gasto['monto']
            total += gasto['monto']
        
        #mensaje de resumen
        mensaje = "Resumen de Gastos por Categoría:\n\n"
        for categoria, monto in resumen.items():
            porcentaje = (monto / total) * 100 if total > 0 else 0
            mensaje += f"{categoria}: ${monto:.2f} ({porcentaje:.1f}%)\n"
        
        mensaje += f"\nTotal General: ${total:.2f}"
        
        QMessageBox.information(self, "Resumen de Gastos", mensaje)

def main():
    app = QApplication(sys.argv)
    ventana = GestionGastosApp()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()