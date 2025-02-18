import mercadopago
from flask import Flask, render_template

# Função para gerar o link de pagamento com Pix
def gerar_link_pagamento():
    sdk = mercadopago.SDK("APP_USR-6233181748431095-021716-58226306382f39282d514b002acfa258-1688260848")  # Substitua pelo seu Access Token do Mercado Pago

    # Dados do pagamento
    payment_data = {
        "items": [
            {"id": "1", "title": "Acesso ao Conteúdo Secreto", "quantity": 1, "currency_id": "BRL", "unit_price": 9.90}
        ],
        "back_urls": {
            "success": "http://127.0.0.1:5000/compracerta",
            "failure": "http://127.0.0.1:5000/compraerrada",
            "pending": "http://127.0.0.1:5000/compraerrada",
        },
        "auto_return": "approved",
        "payer": {
            "email": "acesso@secreto.com",  # Coloque seu e-mail aqui
        },
        "payment_methods": {
            "excluded_payment_types": [{"id": "credit_card"}, {"id": "debit_card"}, {"id": "ticket"}],  # Exclui outras formas de pagamento
            "default_payment_method": {"id": "pix"}  # Força o pagamento por Pix
        }
    }

    result = sdk.preference().create(payment_data)
    payment = result["response"]
    link_iniciar_pagamento = payment["init_point"]  # URL do Mercado Pago para iniciar o pagamento
    return link_iniciar_pagamento

# Flask app
app = Flask(__name__)

@app.route("/")
def homepage():
    link_iniciar_pagamento = gerar_link_pagamento()  # Gera o link de pagamento
    return render_template("pagar.html", link_pagamento=link_iniciar_pagamento)

@app.route("/compracerta")
def compra_certa():
    return render_template("compracerta.html")

@app.route("/compraerrada")
def compra_errada():
    return render_template("compraerrada.html")

if __name__ == "__main__":
    app.run(debug=True)