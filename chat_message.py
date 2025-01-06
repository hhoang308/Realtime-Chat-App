import flet as ft
from cryptography.hazmat.primitives.asymmetric import ec

class Message():
    def __init__(self,user:str,text:str,message_type:str,signature):
        self.user=user
        self.text=text
        self.message_type=message_type
        self.signature=signature
        # TODO: Add property: public key for each user #

        
class ChatMessage(ft.Row):
    def __init__(self, message: Message, page: ft.Page):
        super().__init__()
        self.vertical_alignment = "start"
        self.page = page

        # Define the alert dialog
        self.message_information_dialog = ft.AlertDialog(
            title=ft.Text("Message Information"),
            content=ft.Column(
                [
                    ft.Text("Plain Text: " + message.text, selectable=True),
                    ft.Text("Signature: " + message.signature.hex())
                ],
                tight=True,  # Optional: giảm khoảng cách giữa các phần tử
            ),
            actions=[
                ft.TextButton("Close", on_click=lambda e: self.close_dlg())
            ],
        )

        # Add controls for the ChatMessage
        self.controls = [
            ft.CircleAvatar(
                content=ft.Text(self.get_initials(message.user)),
                color=ft.colors.WHITE,
                bgcolor=self.get_avatar_color(message.user),
            ),
            ft.Column(
                [
                    ft.Text(message.user, weight="bold"),
                    ft.Text(message.text, selectable=True),
                ],
                tight=True,
                spacing=5,
                expand=True,
            ),
            ft.IconButton(
                icon=ft.Icons.MORE_VERT,
                icon_color="blue400",
                icon_size=20,
                tooltip="Show details",
                on_click=lambda e: self.open_dlg(),
            ),
        ]

    def open_dlg(self):
        self.page.dialog = self.message_information_dialog
        self.message_information_dialog.open = True
        self.page.update()

    def close_dlg(self):
        self.message_information_dialog.open = False
        self.page.update()
    
    def get_initials(self, user: str):
        return user[:1].capitalize()

    def get_avatar_color(self, user: str):
        colors_lookup = [
            ft.colors.AMBER,
            ft.colors.BLUE,
            ft.colors.BROWN,
            ft.colors.CYAN,
            ft.colors.GREEN,
            ft.colors.INDIGO,
            ft.colors.LIME,
            ft.colors.ORANGE,
            ft.colors.PINK,
            ft.colors.PURPLE,
            ft.colors.RED,
            ft.colors.TEAL,
            ft.colors.YELLOW,
        ]
        return colors_lookup[hash(user) % len(colors_lookup)]



