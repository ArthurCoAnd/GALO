# "A LICENÇA AÇAÍWARE" (Revisão +55):
# arthurcoand@gmail.com escreveu este arquivo em 2023.
# Enquanto você manter este comentário, você poderá fazer o que quiser com este arquivo.
# Caso nos encontremos algum dia e você ache que este arquivo vale, você poderá me comprar uma açaí em retribuição.
# Arthur Cordeiro Andrade.

#  ██████╗  █████╗ ██╗      ██████╗ 
# ██╔════╝ ██╔══██╗██║     ██╔═══██╗
# ██║  ███╗███████║██║     ██║   ██║
# ██║   ██║██╔══██║██║     ██║   ██║
# ╚██████╔╝██║  ██║███████╗╚██████╔╝
#  ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝ 
# Gerador de Análises Livre e Open-source

import os, sys
parent = os.path.abspath(".")
sys.path.insert(1, parent)

# Bibliotecas
from dateutil.relativedelta import relativedelta
from tqdm import tqdm
import datetime as DT
import json
import pandas as PD

import smtplib, ssl
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders

# Ferramentas
from Ferramentas.Mês import Mês
from Ferramentas.Título import Título

# Link Para Permitir Envio de Email
# Permitir aplicativos menos seguros o envio de emails. Depois do uso desative para segurança.
# https://myaccount.google.com/lesssecureapps

def ITATIAIA():
	Título("ITATIAIA")
	
	ATLETICANOS = PD.read_csv("BDD/ATLETICANOS.csv",sep=";")
	ATLETICANOS = PD.read_csv("BDD/ATLETICANOS-TESTE.csv",sep=";")

	BID_CBF = PD.read_csv("BDD/BID_CBF.csv",sep=";")
	dt_BDD = BID_CBF["dt_ANEEL"][0]

	BID_CBF = PD.read_csv("BDD/BID_CBF.csv",sep=";")
	dt_BDD = BID_CBF["dt_ANEEL"][0]
	ult_Data = DT.datetime.strptime(dt_BDD, "%Y-%m-%d")
	if(int(dt_BDD[8:]) <= 10):
		Data_lim = ult_Data - DT.timedelta(days=ult_Data.day) - relativedelta(months=+1)
	else:
		Data_lim = ult_Data - DT.timedelta(days=ult_Data.day)
	mês = Data_lim.month
	mês_txt = Mês(mês)
	ano = Data_lim.year

	with open("BDD/CFG.json") as f:
		CFG = json.load(f)

	eGALO = CFG["email"]
	eGALO_senha = CFG["senha"]
	eGALO_assunto = f"Relatório GALO - {mês_txt} de {ano}"

	eGALO_port = 465
	eGALO_smtp_server = "smtp.gmail.com"

	context = ssl.create_default_context()
	with smtplib.SMTP_SSL(eGALO_smtp_server, eGALO_port, context=context) as server:
		server.login(eGALO, eGALO_senha)

		for i in (ibar := tqdm(ATLETICANOS.index, leave=False, position=0)):
			ATL_nome = ATLETICANOS["Nome"][i]
			ATL_email = ATLETICANOS["Endereço de e-mail"][i]
			ibar.set_description(f"{ATL_nome}")

			eGALO_msg = MIMEMultipart("alternative")
			eGALO_msg["Subject"] = eGALO_assunto
			eGALO_msg["From"] = eGALO
			eGALO_msg["To"] = ATL_email

			html = str(open("Complementos/GALO.html", "r", encoding="utf-8").read())
			html = html.replace("*nome*",ATL_nome)
			html = html.replace("*mês*",mês_txt)
			html = html.replace("*ano*",str(ano))
			htmlMT = MIMEText(html, "html", "utf-8")
			eGALO_msg.attach(htmlMT)

			pPDF = f"BDD/RELATÓRIOS/GALO - {ATL_nome} - {ano} - {mês}.pdf"
			PDF = MIMEBase("application", "octate-stream", Name=pPDF)
			PDF.set_payload((open(pPDF, "rb")).read())
			encoders.encode_base64(PDF)
			PDF.add_header("Content-Decomposition", "attachment", filename=pPDF.replace("BDD/RELATÓRIOS/","").replace(".pdf",""))
			eGALO_msg.attach(PDF)

			server.send_message(eGALO_msg, from_addr=eGALO, to_addrs=ATL_email)

if __name__ == "__main__":
	os.system("cls" if os.name == "nt" else "clear")
	print(" ██████╗  █████╗ ██╗      ██████╗ ")
	print("██╔════╝ ██╔══██╗██║     ██╔═══██╗")
	print("██║  ███╗███████║██║     ██║   ██║")
	print("██║   ██║██╔══██║██║     ██║   ██║")
	print("╚██████╔╝██║  ██║███████╗╚██████╔╝")
	print(" ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝ ")
	print("Gerador de Análises Livre e Open-source")
	ITATIAIA()