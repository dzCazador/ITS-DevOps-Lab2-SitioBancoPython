"""
Módulo de modelo Tarjeta - Clase para gestionar tarjetas bancarias
"""
from typing import Optional
from datetime import datetime
from enum import Enum
import random
import string


class TipoTarjeta(Enum):
    """Tipos de tarjeta disponibles"""
    DEBITO = "Débito"
    CREDITO = "Crédito"
    PLATINO = "Platino"


class EstadoTarjeta(Enum):
    """Estados posibles de una tarjeta"""
    ACTIVA = "Activa"
    BLOQUEADA = "Bloqueada"
    VENCIDA = "Vencida"
    CANCELADA = "Cancelada"


class Tarjeta:
    """Clase que representa una tarjeta bancaria"""
    
    _contador = 0
    
    def __init__(self, usuario, tipo_tarjeta: TipoTarjeta, cuenta_asociada,
                 limite_credito: float = 0, fecha_emision: Optional[str] = None):
        """
        Inicializa una tarjeta bancaria
        
        Args:
            usuario: Objeto Usuario propietario de la tarjeta
            tipo_tarjeta: Tipo de tarjeta (Débito, Crédito, Platino)
            cuenta_asociada: Cuenta bancaria asociada
            limite_credito: Límite de crédito (solo para tarjetas de crédito)
            fecha_emision: Fecha de emisión (auto-generada si no se proporciona)
        """
        Tarjeta._contador += 1
        self.id_tarjeta = f"CARD-{Tarjeta._contador}"
        self.numero_tarjeta = self._generar_numero()
        self.usuario = usuario
        self.tipo_tarjeta = tipo_tarjeta
        self.cuenta_asociada = cuenta_asociada
        self.estado = EstadoTarjeta.ACTIVA
        self.limite_credito = limite_credito
        self.deuda_actual = 0
        self.fecha_emision = fecha_emision or datetime.now().strftime("%Y-%m-%d")
        self.fecha_vencimiento = self._calcular_vencimiento()
        self.cvv = self._generar_cvv()
        
    @staticmethod
    def _generar_numero() -> str:
        """Genera un número de tarjeta válido (16 dígitos)"""
        return ''.join(random.choices(string.digits, k=16))
    
    @staticmethod
    def _generar_cvv() -> str:
        """Genera un CVV válido (3 dígitos)"""
        return ''.join(random.choices(string.digits, k=3))
    
    @staticmethod
    def _calcular_vencimiento() -> str:
        """Calcula la fecha de vencimiento (5 años)"""
        from datetime import timedelta
        fecha_vencimiento = datetime.now() + timedelta(days=365*5)
        return fecha_vencimiento.strftime("%m/%y")
    
    def realizar_compra(self, monto: float, comercio: str) -> bool:
        """
        Realiza una compra con la tarjeta
        
        Args:
            monto: Monto de la compra
            comercio: Nombre del comercio
            
        Returns:
            True si fue exitosa, False en caso contrario
        """
        if self.estado != EstadoTarjeta.ACTIVA:
            return False
        
        if self.tipo_tarjeta == TipoTarjeta.DEBITO:
            return self.cuenta_asociada.retirar(monto, f"Compra en {comercio}")
        else:  # Crédito o Platino
            if self.deuda_actual + monto > self.limite_credito:
                return False
            self.deuda_actual += monto
            return True
    
    def pagar_deuda(self, monto: float) -> bool:
        """
        Realiza un pago de deuda
        
        Args:
            monto: Monto a pagar
            
        Returns:
            True si fue exitoso, False en caso contrario
        """
        if monto <= 0 or monto > self.deuda_actual:
            return False
        
        if self.cuenta_asociada.retirar(monto, "Pago de tarjeta de crédito"):
            self.deuda_actual -= monto
            return True
        return False
    
    def bloquear(self) -> None:
        """Bloquea la tarjeta"""
        self.estado = EstadoTarjeta.BLOQUEADA
    
    def desbloquear(self) -> None:
        """Desbloquea la tarjeta"""
        self.estado = EstadoTarjeta.ACTIVA
    
    def obtener_saldo_disponible(self) -> float:
        """Retorna el saldo disponible (para tarjetas de crédito)"""
        if self.tipo_tarjeta in [TipoTarjeta.CREDITO, TipoTarjeta.PLATINO]:
            return self.limite_credito - self.deuda_actual
        return self.cuenta_asociada.obtener_saldo()
    
    def obtener_info(self) -> dict:
        """Retorna información de la tarjeta"""
        return {
            'id_tarjeta': self.id_tarjeta,
            'numero_tarjeta': f"**** **** **** {self.numero_tarjeta[-4:]}",
            'tipo_tarjeta': self.tipo_tarjeta.value,
            'estado': self.estado.value,
            'fecha_emision': self.fecha_emision,
            'fecha_vencimiento': self.fecha_vencimiento,
            'limite_credito': self.limite_credito,
            'deuda_actual': self.deuda_actual,
            'saldo_disponible': self.obtener_saldo_disponible()
        }
    
    def __str__(self) -> str:
        return f"Tarjeta {self.tipo_tarjeta.value} - Vencimiento: {self.fecha_vencimiento}"
    
    def __repr__(self) -> str:
        return f"Tarjeta(tipo='{self.tipo_tarjeta.value}', estado='{self.estado.value}')"
