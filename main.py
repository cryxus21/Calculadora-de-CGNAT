from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QApplication, QMainWindow, QMessageBox)
from ui_main import Ui_MainWindow
import sys

class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Calulo Nat")
        self.pushButton.clicked.connect(self.geradorcgnat)
        self.pushButton.setEnabled(False)
        self.radioButton_4.clicked.connect(lambda: self.calculate_result(4))
        self.radioButton_8.clicked.connect(lambda: self.calculate_result(8))
        self.radioButton_16.clicked.connect(lambda: self.calculate_result(16))
        self.radioButton_32.clicked.connect(lambda: self.calculate_result(32))
        self.radioButton_64.clicked.connect(lambda: self.calculate_result(64))
        self.inicio_1024.toggled.connect(self.verificar_radio_button)
        self.inicio_0.toggled.connect(self.verificar_radio_button)
        self.quantidade_portas = 0
        self.portainicial = ''
        self.spinBox.setMaximum(999)
        self.label_7.setStyleSheet("background-color: green; color: white;")
        self.label_6.setStyleSheet("background-color: red; color: white;")
        for button in self.buttonGroup.buttons():
            button.setEnabled(False)

    def verificar_radio_button(self):
        for button in self.buttonGroup.buttons():
                button.setEnabled(True)
        if self.inicio_1024.isChecked():
            self.desmarcar_opcoes()
            self.portainicial = '1024'
            self.quantidade_portas = 64510
            
            
        elif self.inicio_0.isChecked():
            self.desmarcar_opcoes()
            self.portainicial = '0'
            self.quantidade_portas = 65535

    def desmarcar_opcoes(self):
        self.pushButton.setEnabled(False)
        for button in self.buttonGroup.buttons():
            button.setChecked(False)
                       



    def calculate_result(self, divisor):
                self.pushButton.setEnabled(True)
                resultado_quant_ip = int(self.quantidade_portas / divisor)
                self.resultado_ip = resultado_quant_ip
                self.clientes_ip = divisor
                  
    
    def geradorcgnat(self, resultado_quant_ip):
        def calcular_quantidade_ips(cidr):
            bits_host = 32 - int(cidr)
            quantidade_ips = 2 ** bits_host
            return quantidade_ips
        
        ip_mascara_privado = self.Rede_priv.text().strip()
         # Verifique se o campo ip_mascara está no formato esperado
        if not ip_mascara_privado or '/' not in ip_mascara_privado:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Erro")
            msg_box.setText("Endereço IP e máscara inválidos.")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()
            return
        
        # verifica se foi digitado no formato correto
        ip_privado, mascara_privado = ip_mascara_privado.split('/')
        if not ip_privado or not mascara_privado:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Erro")
            msg_box.setText("Endereço IP e máscara inválidos.")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()
            return
        # verifica se foi digitado no formato correto
        ip_mascara_publico = self.Rede_pub.text().strip()
        ip_publico, mascara_publico = ip_mascara_publico.split('/')
        if not ip_publico or not mascara_publico:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Erro")
            msg_box.setText("Endereço IP e máscara inválidos.")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()
            return
        
        def validar_endereco_ip(ip):
            octetos = ip.split('.')
            if len(octetos) != 4:
                return False
            for octeto in octetos:
                if not octeto.isdigit():
                    return False
                valor = int(octeto)
                if valor < 0 or valor > 255:
                    return False
            return True
        
        def validar_mascara(mascara):
            if not mascara.isdigit():
                return False
            mascara_int = int(mascara)
            if mascara_int < 0 or mascara_int > 32:
                return False
            return True
         # Verifique se a ip privado está no formato correto
        if not validar_endereco_ip(ip_privado):
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Erro")
            msg_box.setText("Endereço IP Privado inválido.")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()
            return
        # Verifique se a ip publico está no formato correto# Verifique se a ip privado está no formato correto
        if not validar_endereco_ip(ip_publico):
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Erro")
            msg_box.setText("Endereço IP Público inválido.")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()
            return

        # Verifique se a máscara privado está no formato correto
        if not validar_mascara(mascara_privado):
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Erro")
            msg_box.setText("Máscara inválida (Rede Privada).")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()
            return
         # Verifique se a máscara privado está no formato correto
        if not validar_mascara(mascara_publico):
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Erro")
            msg_box.setText("Máscara inválida (Rede Pública).")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()
            return
        # Verifique se existe interface
        int_up_link = self.int_up_link.text().strip()
        if not int_up_link:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Erro")
            msg_box.setText("Defina uma Interface.")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()
            return
        

        
        privado_octetos = ip_privado.split('.')
        privado_octeto1, privado_octeto2, privado_octeto3, privado_octeto4 = privado_octetos

        publico_octetos = ip_publico.split('.')
        publico_octeto1, publico_octeto2, publico_octeto3, publico_octeto4 = publico_octetos
        quantidade_ips_privado = calcular_quantidade_ips(mascara_privado)
        quantidade_ips_publico = calcular_quantidade_ips(mascara_publico)
        total_de_ip = quantidade_ips_publico * self.clientes_ip

        print("total de ip = " + str(total_de_ip) + " ip privados = " + str(quantidade_ips_privado))
        chain = self.spinBox.value()
        protocolo1 = 'tcp'
        protocolo2 = 'udp'
        #ippublico = '45.172.114'
        #publicoocteto4 = '240'
        portainicial = self.portainicial
        intervaloporta = self.resultado_ip  # Quantidade de portas por IP
        portainicial2 = str(int(portainicial) + intervaloporta)
        contador = 0
        resultado_nat = ''
        resultado_jumping = ''
        interface_up_link = self.int_up_link.text()
        if not  publico_octetos:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Erro")
            msg_box.setText("Campos obrigatórios não preenchidos.")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()
            return
        if total_de_ip == quantidade_ips_privado:
            while (
                contador < quantidade_ips_privado
            ):
                contador += 1
                ipprivadoFull = f"{privado_octeto1}.{privado_octeto2}.{privado_octeto3}.{privado_octeto4}"
                ip_publico_full = f"{publico_octeto1}.{publico_octeto2}.{publico_octeto3}"

                resultado_nat += (
                    f"ip firewall nat add chain=CGNAT_{chain} src-address={ipprivadoFull} protocol={protocolo1} out-interface={interface_up_link} action=src-nat to-addresses={ip_publico_full}.{publico_octeto4} to-ports={portainicial}-{portainicial2} disable=yes\n"
                )
                resultado_nat += (
                    f"ip firewall nat add chain=CGNAT_{chain} src-address={ipprivadoFull} protocol={protocolo2} out-interface={interface_up_link} action=src-nat to-addresses={ip_publico_full}.{publico_octeto4} to-ports={portainicial}-{portainicial2} disable=yes\n\n"
                )
                if int(portainicial) == 1024:
                        if int(intervaloporta) == 1007:
                            resultado_jumping +=(
                                f"ip firewall nat add chain=srcnat src-address={ipprivadoFull}/26 action=jump jump-target=CGNAT_{chain} out-interface={interface_up_link}\n"
                            )
                        if int(intervaloporta) == 2015:
                            resultado_jumping +=(
                                f"ip firewall nat add chain=srcnat src-address={ipprivadoFull}/27 action=jump jump-target=CGNAT_{chain} out-interface={interface_up_link}\n"
                            )
                        if int(intervaloporta) == 4031:
                            resultado_jumping +=(
                                f"ip firewall nat add chain=srcnat src-address={ipprivadoFull}/28 action=jump jump-target=CGNAT_{chain} out-interface={interface_up_link}\n"
                            )
                        if int(intervaloporta) == 8063:
                            resultado_jumping +=(
                                f"ip firewall nat add chain=srcnat src-address={ipprivadoFull}/29 action=jump jump-target=CGNAT_{chain} out-interface={interface_up_link}\n"
                            )
                        if int(intervaloporta) == 16127:
                            resultado_jumping +=(
                                f"ip firewall nat add chain=srcnat src-address={ipprivadoFull}/30 action=jump jump-target=CGNAT_{chain} out-interface={interface_up_link}\n"
                            )
                        
                if int(portainicial) == 0:
                    if int(intervaloporta) == 1023:
                            resultado_jumping +=(
                                f"ip firewall nat add chain=srcnat src-address={ipprivadoFull}/26 action=jump jump-target=CGNAT_{chain} out-interface={interface_up_link}\n"
                            )
                    if int(intervaloporta) == 2047:
                            resultado_jumping +=(
                                f"ip firewall nat add chain=srcnat src-address={ipprivadoFull}/27 action=jump jump-target=CGNAT_{chain} out-interface={interface_up_link}\n"
                            )
                    if int(intervaloporta) == 4095:
                            resultado_jumping +=(
                                f"ip firewall nat add chain=srcnat src-address={ipprivadoFull}/28 action=jump jump-target=CGNAT_{chain} out-interface={interface_up_link}\n"
                            )
                    if int(intervaloporta) == 8191:
                            resultado_jumping +=(
                                f"ip firewall nat add chain=srcnat src-address={ipprivadoFull}/29 action=jump jump-target=CGNAT_{chain} out-interface={interface_up_link}\n"
                            )
                    if int(intervaloporta) == 16383:
                            resultado_jumping +=(
                                f"ip firewall nat add chain=srcnat src-address={ipprivadoFull}/30 action=jump jump-target=CGNAT_{chain} out-interface={interface_up_link}\n"
                            )


                privado_octeto4 = str(int(privado_octeto4) + 1)
                portainicial = str(int(portainicial) + intervaloporta + 1)
                portainicial2 = str(int(portainicial2) + intervaloporta + 1 )

                if int(portainicial2) > 65536:
                    portainicial = self.portainicial  
                    portainicial2 = str(int(portainicial) + intervaloporta)  
                    publico_octeto4 = str(int(publico_octeto4) + 1)
                    chain = str(int(chain) + 1)

                if int(privado_octeto4) > 255:
                    privado_octeto4 = '0'
                    privado_octeto3 = str(int(privado_octeto3) + 1)

                if int(publico_octeto4) > 255:
                    publico_octeto4 = '0'
                    publico_octeto3 = str(int(publico_octeto3) + 1)


            self.Regras_nat.setText(resultado_nat)
            self.Regras_jumping.setText(resultado_jumping)
            self.statusBar.showMessage("Quantidade de IPs Privado: " + str(quantidade_ips_privado) + " | Intervalo de portas: " + str(intervaloporta) + " | Quantidade de IPs Publicos: " + str(quantidade_ips_publico))
        else:
            if total_de_ip < quantidade_ips_privado:
                self.Regras_jumping.clear()
                self.Regras_nat.clear()
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setWindowTitle("Erro")
                msg_box.setText("Quantidade de IPs Privado Excede a quantidade de Clientes por IP Público.")
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.exec_()    
            if total_de_ip > quantidade_ips_privado:
                self.Regras_jumping.clear()
                self.Regras_nat.clear()
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setWindowTitle("Erro")
                msg_box.setText("Quantidade de IPs Público Excede a quantidade de Clientes por IP Privado.")
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.exec_()     




if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

