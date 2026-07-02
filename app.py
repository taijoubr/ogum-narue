from datetime import datetime

from flask import Flask, render_template

app = Flask(__name__)
app.config["SECRET_KEY"] = "ogum-narue-dev"


@app.context_processor
def inject_year():
    return {"current_year": datetime.now().year}


@app.route("/")
def home():
    return render_template(
        "index.html",
        title="Centro Espírita Ogum Naruê",
        description="Site institucional do Centro Espírita Ogum Naruê, com história, agenda, nossa casa, perguntas frequentes e contato.",
        keywords="ogum narue, centro espirita, espiritismo, historia, agenda, nossa casa",
    )


@app.route("/historia")
def historia():
    return render_template(
        "historia.html",
        title="Nossa História",
        description="Conheça a trajetória e os valores do Centro Espírita Ogum Naruê.",
        keywords="historia, nosso passado, valores, missao, visao",
    )


@app.route("/agenda")
def agenda():
    giras = []
    return render_template(
        "agenda.html",
        title="Agenda",
        description="Confira a agenda de giras e encontros do Centro Espírita Ogum Naruê.",
        keywords="agenda, giras, encontros, espiritismo",
        giras=giras,
    )


@app.route("/nossa-casa")
def nossa_casa():
    return render_template(
        "nossa-casa.html",
        title="Nossa Casa",
        description="Conheça a estrutura, os atendimentos e as atividades do Centro Espírita Ogum Naruê.",
        keywords="nossa casa, atendimento, trabalhos espirituais, horarios",
    )


@app.route("/faq")
def faq():
    return render_template(
        "faq.html",
        title="Perguntas Frequentes",
        description="Respostas rápidas sobre participação, agendamento, vestimenta e acesso.",
        keywords="faq, perguntas frequentes, participar, agendamento",
    )


@app.route("/contato")
def contato():
    return render_template(
        "contato.html",
        title="Contato",
        description="Entre em contato com o Centro Espírita Ogum Naruê por telefone ou WhatsApp.",
        keywords="contato, endereco, telefone, whatsapp",
    )


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html", title="Página não encontrada"), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html", title="Erro interno"), 500


if __name__ == "__main__":
    app.run(debug=True)
