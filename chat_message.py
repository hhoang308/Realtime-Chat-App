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
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment="start"
        self.controls=[
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
                    tooltip="Pause record",
                ),
            ]

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



