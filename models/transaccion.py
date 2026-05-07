"""
Módulo de modelo Transacción - Clase para registrar transacciones bancarias
"""
from typing import Optional
from datetime import datetime
from enum import Enum


class TipoTransaccion(Enum):
    """Tipos de transacciones disponibles"""
    DEPOSITO = "Depósito"
    RETIRO = "Retiro"
    TRANSFERENCIA = "Transferencia"
    PAGO_TARJETA = "Pago de Tarjeta"
    COMPRA = "Compra"
    INTERES = "Interés"


class Transaccion:
    """Clase que representa una transacción bancaria"""
    
    _contador_id = 1000
    
    def __init__(self, tipo_transaccion: TipoTransaccion, monto: float,
                 cuenta_origen, cuenta_destino: Optional = None,
                 descripcion: str = "", fecha: Optional[str] = None):
        """
        Inicializa una transacción
        
        Args:
            tipo_transaccion: Tipo de transacción realizada
            monto: Monto de la transacción
            cuenta_origen: Cuenta de origen
            cuenta_destino: Cuenta de destino (opcional)
            descripcion: Descripción de la transacción
            fecha: Fecha de la transacción (auto-generada si no se proporciona)
        """
        Transaccion._contador_id += 1
        self.id_transaccion = f"TRX-{Transaccion._contador_id}"
        self.tipo = tipo_transaccion
        self.monto = monto
        self.cuenta_origen = cuenta_origen
        self.cuenta_destino = cuenta_destino
        self.descripcion = descripcion
        self.fecha = fecha or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def obtener_info(self) -> dict:
        """Retorna información de la transacción"""
        info = {
            'id_transaccion': self.id_transaccion,
            'tipo': self.tipo.value,
            'monto': self.monto,
            'cuenta_origen': self.cuenta_origen.numero_cuenta if self.cuenta_origen else "N/A",
            'descripcion': self.descripcion,
            'fecha': self.fecha
        }
        
        if self.cuenta_destino:
            info['cuenta_destino'] = self.cuenta_destino.numero_cuenta
        
        return info
    
    def __str__(self) -> str:
        return f"{self.tipo.value}: ${self.monto:,.2f} - {self.fecha}"
    
    def __repr__(self) -> str:
        return f"Transaccion(id='{self.id_transaccion}', tipo='{self.tipo.value}', monto={self.monto})"
