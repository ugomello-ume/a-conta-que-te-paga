from flask import Flask, render_template_string, request, redirect
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# GOOGLE SHEETS
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json",
    scope
)

client = gspread.authorize(creds)

sheet = client.open("Leads A Conta que te Paga").sheet1

HTML = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>A Conta que te Paga</title>

    <style>
        *{
            margin:0;
            padding:0;
            box-sizing:border-box;
            font-family: Arial, sans-serif;
        }

        body{
            background:#0f172a;
            color:white;
            display:flex;
            justify-content:center;
            align-items:center;
            min-height:100vh;
            padding:20px;
        }

        .container{
            width:100%;
            max-width:500px;
            background:#111827;
            padding:40px;
            border-radius:20px;
            box-shadow:0 0 30px rgba(0,0,0,0.4);
        }

        h1{
            font-size:32px;
            margin-bottom:20px;
            line-height:1.2;
        }

        p{
            color:#cbd5e1;
            margin-bottom:25px;
            line-height:1.6;
        }

        .question{
            margin-bottom:25px;
        }

        label{
            display:block;
            margin-bottom:10px;
            font-weight:bold;
        }

        select,input{
            width:100%;
            padding:14px;
            border:none;
            border-radius:10px;
            background:#1e293b;
            color:white;
            font-size:16px;
        }

        button{
            width:100%;
            padding:16px;
            border:none;
            border-radius:12px;
            background:#22c55e;
            color:white;
            font-size:18px;
            font-weight:bold;
            cursor:pointer;
        }

        button:hover{
            opacity:0.9;
        }
    </style>
</head>
<body>

<div class="container">

    <h1>A Conta que te Paga</h1>

    <p>
        Transformei uma despesa mensal em oportunidade.
        <br><br>
        Existe uma conta que pode trabalhar a seu favor.
    </p>

    <form method="POST">

        <div class="question">
            <label>O que mais despertou sua curiosidade?</label>

            <select name="interesse" required>
                <option value="">Selecione</option>
                <option>Mudança de mentalidade</option>
                <option>Novas oportunidades</option>
                <option>Curiosidade</option>
            </select>
        </div>

        <div class="question">
            <label>Hoje você busca:</label>

            <select name="objetivo" required>
                <option value="">Selecione</option>
                <option>Apenas conhecimento</option>
                <option>Uma nova oportunidade</option>
                <option>Renda extra</option>
                <option>Liberdade financeira</option>
            </select>
        </div>

        <div class="question">
            <label>Seu nome</label>
            <input type="text" name="nome" required>
        </div>

        <div class="question">
            <label>WhatsApp</label>
            <input type="text" name="whatsapp" required>
        </div>

        <div class="question">
            <label>Email</label>
            <input type="email" name="email" required>
        </div>

        <button type="submit">
            Liberar meu acesso
        </button>

    </form>

</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        nome = request.form.get("nome")
        whatsapp = request.form.get("whatsapp")
        email = request.form.get("email")
        interesse = request.form.get("interesse")
        objetivo = request.form.get("objetivo")

        # SALVAR NO GOOGLE SHEETS
        sheet.append_row([
            nome,
            whatsapp,
            email,
            interesse,
            objetivo
        ])

        # REDIRECIONAR PARA O EBOOK
        return redirect("https://drive.google.com/file/d/1cCcsDxgwfe8kPq0Si1_yJnxBVA87Khbq/view?usp=sharing")

    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(host="0.0.0.0")