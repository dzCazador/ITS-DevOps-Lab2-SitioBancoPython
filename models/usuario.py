"""
Módulo de modelo Usuario - Clase base para gestionar usuarios del banco
"""
from typing import Optional
from datetime import datetime


class Usuario:
    """Clase que representa un usuario del banco"""
    
    _contador_id = 1000
    
    def __init__(self, cedula: str, nombre: str, apellido: str, email: str, 
                 telefono: str, contrasena: str, fecha_registro: Optional[str] = None):
        """
        Inicializa un usuario del banco
        
        Args:
            cedula: Número de cédula único del usuario
            nombre: Nombre del usuario
            apellido: Apellido del usuario
            email: Email del usuario
            telefono: Teléfono de contacto
            contrasena: Contraseña de acceso
            fecha_registro: Fecha de registro (auto-generada si no se proporciona)
        """
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = telefono
        self.contrasena = contrasena
        self.fecha_registro = fecha_registro or datetime.now().strftime("%Y-%m-%d")
        self.cuentas = []
        self.tarjetas = []
        
    @property
    def nombre_completo(self) -> str:
        """Retorna el nombre completo del usuario"""
        return f"{self.nombre} {self.apellido}"
    
    def agregar_cuenta(self, cuenta) -> None:
        """Agrega una cuenta bancaria al usuario"""
        if cuenta not in self.cuentas:
            self.cuentas.append(cuenta)
    
    def agregar_tarjeta(self, tarjeta) -> None:
        """Agrega una tarjeta al usuario"""
        if tarjeta not in self.tarjetas:
            self.tarjetas.append(tarjeta)
    
    def obtener_saldo_total(self) -> float:
        """Calcula el saldo total en todas las cuentas"""
        return sum(cuenta.saldo for cuenta in self.cuentas)
    
    def obtener_info(self) -> dict:
        """Retorna información del usuario"""
        return {
            'cedula': self.cedula,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'nombre_completo': self.nombre_completo,
            'email': self.email,
            'telefono': self.telefono,
            'fecha_registro': self.fecha_registro,
            'total_cuentas': len(self.cuentas),
            'total_tarjetas': len(self.tarjetas),
            'saldo_total': self.obtener_saldo_total()
        }
    
    def __str__(self) -> str:
        return f"Usuario: {self.nombre_completo} ({self.cedula})"
    
    def __repr__(self) -> str:
        return f"Usuario(cedula='{self.cedula}', nombre='{self.nombre}', apellido='{self.apellido}')"
