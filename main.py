from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.label import MDLabel
from functools import partial
from screens import *
from kivymd.uix.button import MDIconButton
from kivymd.uix.button import MDButton, MDButtonText
from kivy.uix.widget import Widget
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogSupportingText, MDDialogButtonContainer


class MainApp(MDApp):
    def build(self):
        screen = Builder.load_file("main.kv")

        return screen

    def on_start(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Darkcyan"

        self.ScreenManager = self.root
        self.ScreenManager.add_widget(Login(name="loginpage"))
        self.ScreenManager.add_widget(CadastroEmail(name="cadastroemail"))
        self.ScreenManager.add_widget(CodigoConfirmacao(name="codigoconfirmacao"))
        self.ScreenManager.add_widget(CadastroSenha(name="cadastrosenha"))
        self.ScreenManager.add_widget(HomePage(name="homepage"))
        self.dialogo = ""
        self.codigo_rec_conf = 123123

        self.palavras = [
            ("Das Mädchen", "A menina"),
            ("Die Frau", "A mulher"),
            ("Der Mann", "O homem"),
            ("Der Junge", "O menino"),
            ("Das Baby", "O bebê"),
            ("Das Haus", "A casa"),
            ("Die Schwester", "A irmã"),
            ("Der Bruder", "O irmão"),
        ]

        homepage = self.root.ids["homepage"]
        lista_palavas = homepage.ids["lista_palavras"]

        for palavra, traducao in self.palavras:
            label_palavra = MDLabel(
                    text=f"{palavra}",
                    halign="center",
                    theme_text_color = "Custom",
                    md_bg_color = [.119, .136, .153, 1],
                    radius= [15]
                )

            sobre_palavra = MDIconButton(
                icon="dots-vertical",
                style="outlined",
                theme_font_size="Custom",
                font_size="25sp",
                pos_hint={"center_x": .85, "center_y": .85},
                on_release=partial(self.sobre_palavra, palavra)
            )

            lista_palavas.add_widget(label_palavra)
            lista_palavas.add_widget(sobre_palavra)


    def sobre_palavra(self, palavra, *args):
        print(f"Exibindo informações sobre a palavra: {palavra}")
        self.mudar_tela("loginpage", "left")


    def mudar_tela(self, id_tela, direcao_transicao):
        self.ScreenManager.transition = SlideTransition(direction=direcao_transicao)
        self.ScreenManager.current = id_tela


    def enviar_email_recuperacao(self, email, *args):
        print(f"Enviando e-mail de recuperação para {email}")
        self.dialogo.dismiss()
        self.mudar_tela("codigorecuperacao", "left")

    def enviar_email_confirmacao(self, email, *args):
        print(f"enviando e-mail de confirmação para {email}")


    def verificar_codigo_recuperacao(self, codigo_digitado):
        print(f"Codigo digitado: {codigo_digitado}")

    def verificar_codigo_confirmacao(self, codigo_digitado):
        if int(codigo_digitado) == self.codigo_rec_conf:
            self.mudar_tela("cadastrosenha", "left")
        else:
            print("Código incorreto")


    # Usado para que o usuário consiga digitar apenas números da página do código de recuperação
    def apenas_digito(self, campo_texto, texto):
        if len(texto) > 6:
            campo_texto.text = texto[:len(texto) - 1]
            return 0

        for caracter in texto:
            if caracter.isdigit()==False:
                campo_texto.text = texto[:len(texto) - 1]
                break


    # Verifica se o usuário está ou não preenchendo um e-mail válido
    def verificar_email(self, campo_email):
        if campo_email.is_email_valid(campo_email.text) == True:
            campo_email.error = True
            return False
        else:
            campo_email.error = False
            return True

    def verificar_senha(self, campo_senha):
        print(campo_senha.text)

    def cadastrar_email(self, campo_email):
        # Se o usuário digitou o e-mail corretamente (e se ele digitou um e-mail)
        if self.verificar_email(campo_email):
            # Verificar se o e-mail já existe
            # Se o e-mail não existir
            print("Pode fazer cadastro do e-mail")
            self.mudar_tela("codigoconfirmacao", "left")


        # Caso o e-mail não seja válido
        else:
            print("Não pode fazer cadastro do e-mail")

    def cadastrar_senha(self, campo_senha):
        print("Senha cadastrada com sucesso")
        self.mudar_tela("homepage", "left")

    def fazer_login(self, campo_email, campo_senha):
        usuarios = [("pedrovbittencourt@gmail.com", "ppvb26102004ooet"), ("pedrovbittencourt@hotmail.com", "pa1234")]
        email = campo_email.text
        senha = campo_senha.text

        email_encontrado = 0

        for usuario in usuarios:
            if usuario[0] == email:
                email_encontrado = 1

                if usuario[1] == senha:
                    self.mudar_tela("homepage", "left")
                    break

                else:
                    campo_senha.text = ""
                    campo_senha.error = True
                    self.dialogo = MDDialog(
                        MDDialogHeadlineText(
                            text="Senha Incorreta"
                        ),
                        MDDialogSupportingText(
                            text=f"Enviar e-mail de recuperação de senha?",
                            halign="justify"
                        ),
                        MDDialogButtonContainer(
                            MDButton(
                                MDButtonText(text="Não"),
                                style="filled",
                                theme_bg_color= "Custom",
                                md_bg_color=[1, 0.6, 0.6, 1],
                                on_release = lambda x: self.dialogo.dismiss(),
                            ),
                            MDButton(
                                MDButtonText(text="Sim"),
                                style="filled",
                                theme_bg_color="Custom",
                                md_bg_color=[0.6, 1, 0.6, 1],
                                on_release = partial(self.enviar_email_recuperacao, campo_email.text)

                            )
                        ),
                        size_hint=[.3, .3],
                        style="filled"
                    )
                    break




        if email_encontrado==0:
            print("E-mail não cadastrado")
            campo_email.error = True
            self.dialogo = MDDialog(
                MDDialogHeadlineText(
                    text="E-mail não cadastrado"
                ),
                MDDialogButtonContainer(
                    Widget(),
                    MDButton(
                        MDButtonText(text="Fechar"),
                        style="filled",
                        on_release=lambda x: self.dialogo.dismiss(),
                        pos_hint={"center_x": 0.5}
                    ),
                    Widget(),
                ),
                size_hint=[.3, .3],
                style="filled"
            )

        if self.dialogo:
            self.dialogo.open()


MainApp().run()