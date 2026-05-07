"""
Módulo de modelo CuentaBancaria - Clase para gestionar cuentas bancarias
"""
from typing import List, Optional
from datetime import datetime
from enum import Enum


class TipoCuenta(Enum):
    """Tipos de cuenta disponibles"""
    AHORROS = "Ahorros"
    CORRIENTE = "Corriente"
    DEPOSITO_PLAZO = "Depósito a Plazo"


class CuentaBancaria:
    """Clase que representa una cuenta bancaria"""
    
    _contador_numero = 1000000
    
    def __init__(self, usuario, tipo_cuenta: TipoCuenta, saldo_inicial: float = 0,
                 fecha_creacion: Optional[str] = None):
        """
        Inicializa una cuenta bancaria
        
        Args:
            usuario: Objeto Usuario propietario de la cuenta
            tipo_cuenta: Tipo de cuenta (Ahorros, Corriente, etc)
            saldo_inicial: Saldo inicial de la cuenta
            fecha_creacion: Fecha de creación (auto-generada si no se proporciona)
        """
        CuentaBancaria._contador_numero += 1
        self.numero_cuenta = f"ACC-{CuentaBancaria._contador_numero}"
        self.usuario = usuario
        self.tipo_cuenta = tipo_cuenta
        self.saldo = saldo_inicial
        self.fecha_creacion = fecha_creacion or datetime.now().strftime("%Y-%m-%d")
        self.activa = True
        self.transacciones: List = []
        
    def depositar(self, monto: float, descripcion: str = "Depósito") -> bool:
        """
        Realiza un depósito a la cuenta
        
        Args:
            monto: Monto a depositar
            descripcion: Descripción del depósito
            
        Returns:
            True si fue exitoso, False en caso contrario
        """
        if monto <= 0:
            return False
        
        self.saldo += monto
        return True
    
    def retirar(self, monto: float, descripcion: str = "Retiro") -> bool:
        """
        Realiza un retiro de la cuenta
        
        Args:
            monto: Monto a retirar
            descripcion: Descripción del retiro
            
        Returns:
            True si fue exitoso, False si hay fondos insuficientes
        """
        if monto <= 0 or monto > self.saldo:
            return False
        
        self.saldo -= monto
        return True
    
    def transferir(self, cuenta_destino, monto: float) -> bool:
        """
        Realiza una transferencia a otra cuenta
        
        Args:
            cuenta_destino: Cuenta receptora
            monto: Monto a transferir
            
        Returns:
            True si fue exitoso, False en caso contrario
        """
        if self.retirar(monto, f"Transferencia a {cuenta_destino.numero_cuenta}"):
            cuenta_destino.depositar(monto, f"Transferencia desde {self.numero_cuenta}")
            return True
        return False
    
    def obtener_saldo(self) -> float:
        """Retorna el saldo actual de la cuenta"""
        return self.saldo
    
    def obtener_info(self) -> dict:
        """Retorna información de la cuenta"""
        return {
            'numero_cuenta': self.numero_cuenta,
            'tipo_cuenta': self.tipo_cuenta.value,
            'saldo': self.saldo,
            'fecha_creacion': self.fecha_creacion,
            'activa': self.activa,
            'total_transacciones': len(self.transacciones)
        }
    
    def __str__(self) -> str:
        return f"Cuenta {self.numero_cuenta} ({self.tipo_cuenta.value}) - Saldo: ${self.saldo:,.2f}"
    
    def __repr__(self) -> str:
        return f"CuentaBancaria(numero='{self.numero_cuenta}', tipo='{self.tipo_cuenta.value}')"
