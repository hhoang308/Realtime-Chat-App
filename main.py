import flet as ft
from signin_form import *
from signup_form import *
from users_db import *
from chat_message import *
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature


def main(page: ft.Page):
    page.title = "Chat Flet Messenger"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # TODO: Generate Elliptic Curve #

    # ***************  Functions             *************
    def sign_message(private_key, message):
        signature = private_key.sign(
            message.encode(),  # Mã hóa bản tin thành bytes
            ec.ECDSA(hashes.SHA256())  # Sử dụng ECDSA với thuật toán băm SHA-256
        )
        return signature
    
    def verify_signature(public_key, message, signature):
        try:
            public_key.verify(
                signature,  # Chữ ký cần xác minh
                message.encode(),  # Bản tin cần xác minh
                ec.ECDSA(hashes.SHA256())  # Thuật toán băm SHA-256
            )
            return True
        except InvalidSignature:
            return False
    
    def dropdown_changed(e):
        new_message.value = new_message.value + emoji_list.value
        page.update()

    def close_banner(e):
        page.banner.open = False
        page.update()

    def open_dlg():
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    def close_dlg(e):
        dlg.open = False
        page.route = "/"
        page.update()

    def sign_in(user: str, password: str):
        db = UsersDB()
        if not db.read_db(user, password):
            print("User no exist ...")
            page.banner.open = True
            page.update()
        else:
            # TODO: Generate private key and public key for this user #
            private_key = ec.generate_private_key(ec.SECP256R1())
            public_key = private_key.public_key()

            if db.write_private_key(user, private_key) == False or db.write_public_key(user, public_key) == False:
                print(f'Keys for {user} saved failed.')
            else:
                print(f'Keys for {user} saved success.')

            retrieved_private_key = db.read_private_key(user)
            print("Private Key:", retrieved_private_key)

            # Đọc khóa công khai
            retrieved_public_key = db.read_public_key(user)
            print("Public Key:", retrieved_public_key)

            print("Redirecting to chat...")
            page.session.set("user", user) # TODO: Save private key for this user # 
            page.route = "/chat"
            page.pubsub.send_all(
                Message(
                    user=user,
                    text=f"{user} has joined the chat.",
                    message_type="login_message",
                    signature=""
                    # TODO: Send public key for all user message_type = "public_key message" #
                )
            )
            page.update()

    def sign_up(user: str, password: str):
        db = UsersDB()
        if db.write_db(user, password):
            print("Successfully Registered User...")
            open_dlg()

    def on_message(message: Message):
        if message.message_type == "chat_message":
            # TODO: Verify message with signature, if correct, display it and vice verse #
            db = UsersDB()
            retrieved_public_key = db.read_public_key(message.user)
            is_valid = verify_signature(retrieved_public_key, message.text, message.signature)
            if is_valid == True:
                print("Chữ ký hợp lệ")
            else:
                print("Chữ ký không hợp lệ")
            m = ChatMessage(message)
        elif message.message_type == "login_message":
            m = ft.Text(message.text, italic=True, color=ft.Colors.WHITE, size=12)
        # TODO: Receive public key of user #
        chat.controls.append(m)
        page.update()

    page.pubsub.subscribe(on_message)

    def send_message_click(e):
        db = UsersDB()
        user = page.session.get("user")
        retrieved_private_key = db.read_private_key(user)
        signature = sign_message(retrieved_private_key, new_message.value)
        print(f"Chữ ký: {signature}")
        page.pubsub.send_all(
            Message(
                user=user,
                text=new_message.value,
                message_type="chat_message",
                signature=signature,
            )
        )
        new_message.value = ""
        page.update()

    def btn_signin(e):
        page.route = "/"
        page.update()

    def btn_signup(e):
        page.route = "/signup"
        page.update()

    def btn_exit(e):
        page.session.remove("user")
        page.route = "/"
        page.update()

    # ************          Aplication UI              **********************************
    principal_content = ft.Column(
        [
            ft.Icon(ft.Icons.WECHAT, size=200, color=ft.Colors.BLUE),
            ft.Text(value="Chat Flet Messenger", size=50, color=ft.Colors.BLACK),
        ],
        height=400,
        width=600,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    emoji_list = ft.Dropdown(
        on_change=dropdown_changed,
        options=[
            ft.dropdown.Option("😃"),
            ft.dropdown.Option("😊"),
            ft.dropdown.Option("😂"),
            ft.dropdown.Option("🤔"),
            ft.dropdown.Option("😭"),
            ft.dropdown.Option("😉"),
            ft.dropdown.Option("🤩"),
            ft.dropdown.Option("🥰"),
            ft.dropdown.Option("😎"),
            ft.dropdown.Option("❤️"),
            ft.dropdown.Option("🔥"),
            ft.dropdown.Option("✅"),
            ft.dropdown.Option("✨"),
            ft.dropdown.Option("👍"),
            ft.dropdown.Option("🎉"),
            ft.dropdown.Option("👉"),
            ft.dropdown.Option("⭐"),
            ft.dropdown.Option("☀️"),
            ft.dropdown.Option("👀"),
            ft.dropdown.Option("👇"),
            ft.dropdown.Option("🚀"),
            ft.dropdown.Option("🎂"),
            ft.dropdown.Option("💕"),
            ft.dropdown.Option("🏡"),
            ft.dropdown.Option("🍎"),
            ft.dropdown.Option("🎁"),
            ft.dropdown.Option("💯"),
            ft.dropdown.Option("💤"),
        ],
        width=50,
        value="😃",
        alignment=ft.alignment.center,
        border_color=ft.Colors.AMBER,
        color=ft.Colors.AMBER,
    )

    signin_UI = SignInForm(sign_in, btn_signup)
    signup_UI = SignUpForm(sign_up, btn_signin)

    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )

    new_message = ft.TextField(
        hint_text="Write a message...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        on_submit=send_message_click,
    )

    page.overlay.append(ft.Banner(
        bgcolor=ft.Colors.BLACK45,
        leading=ft.Icon(ft.Icons.ERROR, color=ft.Colors.RED, size=40),
        content=ft.Text("Log in failed, Incorrect User Name or Password"),
        actions=[
            ft.TextButton("Ok", on_click=close_banner),
        ],
    ))

    dlg = ft.AlertDialog(
        modal=True,
        title=ft.Container(
            content=ft.Icon(
                name=ft.Icons.CHECK_CIRCLE_OUTLINED, color=ft.Colors.GREEN, size=100
            ),
            width=120,
            height=120,
        ),
        content=ft.Text(
            value="Congratulations,\n your account has been successfully created\n Please Sign In",
            text_align=ft.TextAlign.CENTER,
        ),
        actions=[
            ft.ElevatedButton(
                text="Continue", color=ft.Colors.WHITE, on_click=close_dlg
            )
        ],
        actions_alignment="center",
        on_dismiss=lambda e: print("Dialog dismissed!"),
    )

    # ****************        Routes              ******************
    def route_change(route):
        if page.route == "/":
            page.clean()
            page.add(
                ft.Row(
                    [principal_content, signin_UI],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            )

        if page.route == "/signup":
            page.clean()
            page.add(
                ft.Row(
                    [principal_content, signup_UI],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            )

        if page.route == "/chat":
            if page.session.contains_key("user"):
                page.clean()
                page.add(
                    ft.Row(
                        [
                            ft.Text(value="Chat Flet Messenger", color=ft.Colors.WHITE),
                            ft.ElevatedButton(
                                text="Log Out",
                                bgcolor=ft.Colors.RED_800,
                                on_click=btn_exit,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    )
                )
                page.add(
                    ft.Container(
                        content=chat,
                        border=ft.border.all(1, ft.Colors.OUTLINE),
                        border_radius=5,
                        padding=10,
                        expand=True,
                    )
                )
                page.add(
                    ft.Row(
                        controls=[
                            emoji_list,
                            new_message,
                            ft.IconButton(
                                icon=ft.Icons.SEND_ROUNDED,
                                tooltip="Send message",
                                on_click=send_message_click,
                            ),
                        ],
                    )
                )

            else:
                page.route = "/"
                page.update()

    page.on_route_change = route_change
    page.add(
        ft.Row([principal_content, signin_UI], alignment=ft.MainAxisAlignment.CENTER)
    )


ft.app(target=main, view=ft.WEB_BROWSER)
