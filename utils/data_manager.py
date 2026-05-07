import json
from pathlib import Path
from typing import Optional

from models.usuario import Usuario
from models.cuenta import CuentaBancaria, TipoCuenta
from models.tarjeta import Tarjeta, TipoTarjeta
from models.transaccion import Transaccion, TipoTransaccion


class Banco:
    """Gestor de datos bancarios cargados desde JSON."""

    def __init__(self, datos_path: str):
        self.datos_path = Path(datos_path)
        self.usuarios = []
        self.cuentas = []
        self.tarjetas = []
        self.transacciones = []
        self._cargar_datos()

    def _cargar_datos(self) -> None:
        if not self.datos_path.exists():
            raise FileNotFoundError(f"No se encontró el archivo: {self.datos_path}")

        with open(self.datos_path, encoding="utf-8") as archivo:
            datos = json.load(archivo)

        usuarios_por_cedula = {}
        cuentas_por_numero = {}

        for usuario_dto in datos.get("usuarios", []):
            usuario = Usuario(
                cedula=usuario_dto["cedula"],
                nombre=usuario_dto["nombre"],
                apellido=usuario_dto["apellido"],
                email=usuario_dto["email"],
                telefono=usuario_dto["telefono"],
                contrasena=usuario_dto["contrasena"],
                fecha_registro=usuario_dto.get("fecha_registro"),
            )
            self.usuarios.append(usuario)
            usuarios_por_cedula[usuario.cedula] = usuario

        max_acc = 0
        for cuenta_dto in datos.get("cuentas", []):
            usuario = usuarios_por_cedula[cuenta_dto["cedula_usuario"]]
            tipo = TipoCuenta(cuenta_dto["tipo_cuenta"])
            cuenta = CuentaBancaria(
                usuario=usuario,
                tipo_cuenta=tipo,
                saldo_inicial=cuenta_dto.get("saldo", 0.0),
                fecha_creacion=cuenta_dto.get("fecha_creacion"),
            )
            cuenta.numero_cuenta = cuenta_dto["numero_cuenta"]
            self.cuentas.append(cuenta)
            usuario.agregar_cuenta(cuenta)
            cuentas_por_numero[cuenta.numero_cuenta] = cuenta

            try:
                numero = int(cuenta.numero_cuenta.split("-")[-1])
                max_acc = max(max_acc, numero)
            except ValueError:
                continue

        if max_acc > CuentaBancaria._contador_numero:
            CuentaBancaria._contador_numero = max_acc

        for tarjeta_dto in datos.get("tarjetas", []):
            usuario = usuarios_por_cedula[tarjeta_dto["cedula_usuario"]]
            cuenta_asociada = cuentas_por_numero[tarjeta_dto["numero_cuenta"]]
            tipo_tarjeta = TipoTarjeta(tarjeta_dto["tipo_tarjeta"])
            tarjeta = Tarjeta(
                usuario=usuario,
                tipo_tarjeta=tipo_tarjeta,
                cuenta_asociada=cuenta_asociada,
                limite_credito=tarjeta_dto.get("limite_credito", 0.0),
                fecha_emision=tarjeta_dto.get("fecha_emision"),
            )
            tarjeta.numero_tarjeta = tarjeta_dto["numero_tarjeta"]
            tarjeta.fecha_vencimiento = tarjeta_dto.get("vencimiento", tarjeta.fecha_vencimiento)
            tarjeta.deuda_actual = tarjeta_dto.get("deuda_actual", tarjeta.deuda_actual)
            tarjeta.estado = tarjeta.estado
            self.tarjetas.append(tarjeta)
            usuario.agregar_tarjeta(tarjeta)

        max_trans = 0
        for transaccion_dto in datos.get("transacciones", []):
            tipo = TipoTransaccion(transaccion_dto["tipo"])
            cuenta_origen = None
            cuenta_destino = None

            if tipo == TipoTransaccion.TRANSFERENCIA:
                cuenta_origen = cuentas_por_numero.get(transaccion_dto.get("cuenta_origen"))
                cuenta_destino = cuentas_por_numero.get(transaccion_dto.get("cuenta_destino"))
            else:
                cuenta_origen = cuentas_por_numero.get(transaccion_dto.get("cuenta") or transaccion_dto.get("cuenta_origen"))

            transaccion = Transaccion(
                tipo_transaccion=tipo,
                monto=transaccion_dto.get("monto", 0.0),
                cuenta_origen=cuenta_origen,
                cuenta_destino=cuenta_destino,
                descripcion=transaccion_dto.get("descripcion", transaccion_dto.get("comercio", "")),
                fecha=transaccion_dto.get("fecha"),
            )
            transaccion.id_transaccion = transaccion_dto["id_transaccion"]
            self.transacciones.append(transaccion)

            if cuenta_origen:
                cuenta_origen.transacciones.append(transaccion)
            if cuenta_destino and cuenta_destino is not cuenta_origen:
                cuenta_destino.transacciones.append(transaccion)

            try:
                numero = int(transaccion.id_transaccion.split("-")[-1])
                max_trans = max(max_trans, numero)
            except ValueError:
                continue

        if max_trans > Transaccion._contador_id:
            Transaccion._contador_id = max_trans

    def autenticar(self, identificador: str, contrasena: str) -> Optional[Usuario]:
        identificador = identificador.strip().lower()
        for usuario in self.usuarios:
            if (usuario.email.lower() == identificador or usuario.cedula == identificador) and usuario.contrasena == contrasena:
                return usuario
        return None

    def obtener_cuentas_por_usuario(self, usuario: Usuario):
        return usuario.cuentas

    def obtener_tarjetas_por_usuario(self, usuario: Usuario):
        return usuario.tarjetas

    def obtener_transacciones_por_usuario(self, usuario: Usuario):
        cuentas = self.obtener_cuentas_por_usuario(usuario)
        transacciones = []
        for cuenta in cuentas:
            transacciones.extend(cuenta.transacciones)
        return sorted(transacciones, key=lambda t: t.fecha, reverse=True)

    def buscar_usuario(self, identificador: str) -> Optional[Usuario]:
        identificador = identificador.strip().lower()
        for usuario in self.usuarios:
            if usuario.email.lower() == identificador or usuario.cedula == identificador:
                return usuario
        return None
