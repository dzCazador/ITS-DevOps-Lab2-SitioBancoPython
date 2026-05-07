import flet as ft

from utils.data_manager import Banco

banco = Banco("data/datos.json")


def formato_moneda(valor: float) -> str:
    return f"${valor:,.2f}"


def main(page: ft.Page):
    page.title = "Banco Seguro"
    page.window_width = 1200
    page.window_height = 800
    page.theme = ft.Theme(color_scheme_seed=ft.colors.BLUE)
    page.padding = 20
    page.spacing = 20
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.scroll = "auto"

    login_error = ft.Text("", color=ft.colors.RED, size=14)

    email_field = ft.TextField(
        label="Email o Cédula",
        width=420,
        autofocus=True,
        text_size=16,
    )
    password_field = ft.TextField(
        label="Contraseña",
        password=True,
        can_reveal_password=True,
        width=420,
        text_size=16,
    )

    def mostrar_login():
        page.controls.clear()
        page.add(
            ft.Column(
                [
                    ft.Text("Banco Seguro", size=42, weight="bold"),
                    ft.Text(
                        "Ingresa para acceder a tu dashboard, consultar cuentas, tarjetas y movimientos.",
                        size=18,
                        color=ft.colors.BLUE_GREY,
                    ),
                    ft.Container(height=20),
                    ft.Column(
                        [
                            email_field,
                            password_field,
                            login_error,
                            ft.ElevatedButton("Ingresar", on_click=on_login, width=420),
                        ],
                        tight=True,
                        spacing=16,
                    ),
                    ft.Container(height=30),
                    ft.Text("Usuarios de prueba:", size=14, color=ft.colors.BLACK54),
                    ft.Text("juan.garcia@email.com / 123456", size=14),
                    ft.Text("maria.lopez@email.com / password123", size=14),
                    ft.Text("carlos.martinez@email.com / seguridadmax", size=14),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                width=800,
            )
        )
        page.update()

    def build_stats_card(titulo: str, valor: str, icono: str):
        return ft.Card(
            elevation=2,
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [ft.Icon(name=icono, color=ft.colors.BLUE, size=28), ft.Text(titulo, size=16, weight="bold")],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        ft.Text(valor, size=28, weight="bold"),
                    ],
                    tight=True,
                    spacing=8,
                ),
                padding=20,
                width=260,
            ),
        )

    def build_account_card(cuenta):
        return ft.Card(
            elevation=2,
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(cuenta.tipo_cuenta.value, size=16, weight="bold"),
                        ft.Text(cuenta.numero_cuenta, size=14, color=ft.colors.BLACK54),
                        ft.Text(formato_moneda(cuenta.saldo), size=24, weight="bold"),
                        ft.Text(f"Creada: {cuenta.fecha_creacion}", size=12, color=ft.colors.BLACK54),
                    ],
                    tight=True,
                    spacing=10,
                ),
                padding=18,
                width=300,
            ),
        )

    def build_card_card(tarjeta):
        return ft.Card(
            elevation=2,
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(tarjeta.tipo_tarjeta.value, size=16, weight="bold"),
                        ft.Text(tarjeta.numero_tarjeta, size=14),
                        ft.Text(f"Vence: {tarjeta.fecha_vencimiento}", size=12, color=ft.colors.BLACK54),
                        ft.Text(f"Estado: {tarjeta.estado.value}", size=12, color=ft.colors.BLACK54),
                        ft.Text(
                            "Límite disponible: " + formato_moneda(tarjeta.obtener_saldo_disponible()),
                            size=14,
                            weight="bold",
                        ),
                    ],
                    tight=True,
                    spacing=8,
                ),
                padding=18,
                width=300,
            ),
        )

    def build_transactions_table(transacciones):
        columnas = [
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Tipo")),
            ft.DataColumn(ft.Text("Monto")),
            ft.DataColumn(ft.Text("Cuenta origen")),
            ft.DataColumn(ft.Text("Destino")),
            ft.DataColumn(ft.Text("Fecha")),
        ]
        filas = []
        for trans in transacciones[:8]:
            filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(trans.id_transaccion)),
                        ft.DataCell(ft.Text(trans.tipo.value)),
                        ft.DataCell(ft.Text(formato_moneda(trans.monto))),
                        ft.DataCell(ft.Text(trans.cuenta_origen.numero_cuenta if trans.cuenta_origen else "N/A")),
                        ft.DataCell(ft.Text(trans.cuenta_destino.numero_cuenta if trans.cuenta_destino else "-")),
                        ft.DataCell(ft.Text(trans.fecha)),
                    ]
                )
            )
        return ft.DataTable(columns=columnas, rows=filas, border=ft.border.all(1, ft.colors.BLUE_GREY_100))

    def mostrar_dashboard(usuario):
        page.controls.clear()
        cuentas = banco.obtener_cuentas_por_usuario(usuario)
        tarjetas = banco.obtener_tarjetas_por_usuario(usuario)
        transacciones = banco.obtener_transacciones_por_usuario(usuario)

        page.add(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(f"Bienvenido, {usuario.nombre_completo}", size=32, weight="bold"),
                                    ft.Text("Este es tu panel de control bancario.", size=16, color=ft.colors.BLACK54),
                                ],
                                spacing=8,
                            ),
                            ft.ElevatedButton("Cerrar sesión", on_click=lambda _: mostrar_login()),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        [
                            build_stats_card("Cuentas", str(len(cuentas)), "account_balance_wallet"),
                            build_stats_card("Tarjetas", str(len(tarjetas)), "credit_card"),
                            build_stats_card("Saldo total", formato_moneda(usuario.obtener_saldo_total()), "savings"),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Text("Mis cuentas", size=24, weight="bold"),
                    ft.Row(
                        [build_account_card(cuenta) for cuenta in cuentas],
                        wrap=True,
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    ft.Text("Mis tarjetas", size=24, weight="bold"),
                    ft.Row(
                        [build_card_card(tarjeta) for tarjeta in tarjetas],
                        wrap=True,
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    ft.Text("Últimas transacciones", size=24, weight="bold"),
                    build_transactions_table(transacciones),
                ],
                spacing=24,
            )
        )
        page.update()

    def on_login(e):
        login_error.value = ""
        usuario = banco.autenticar(email_field.value, password_field.value)
        if usuario is None:
            login_error.value = "Credenciales inválidas. Intenta de nuevo."
            page.update()
            return
        mostrar_dashboard(usuario)

    mostrar_login()


if __name__ == "__main__":
    # Agregamos web_renderer para compatibilidad
    #ft.app(target=main, port=8085, host="0.0.0.0", view=ft.WEB_BROWSER, web_renderer=ft.WebRenderer.HTML)
    ft.app(target=main,port=8086, view=ft.AppView.WEB_BROWSER)