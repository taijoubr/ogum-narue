import os
from datetime import datetime
import json

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session
from utils.auth import init_app, login_required, programador_required, generate_csrf_token, validate_csrf
from services.audit_service import ensure_tables, record_audit
from services.auth_service import (
    determine_user_level,
    is_supabase_auth_enabled,
    supabase_sign_in,
)
from models.user_level import UserLevel

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = "ogum-narue-dev"
init_app(app)

# ensure audit table exists
try:
    ensure_tables()
except Exception:
    pass


def get_giras_path():
    path = os.path.join(app.instance_path, "giras.json")
    os.makedirs(app.instance_path, exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as file:
            json.dump([], file, ensure_ascii=False, indent=2)
    return path


def load_giras():
    path = get_giras_path()
    with open(path, encoding="utf-8") as file:
        return json.load(file)


def save_giras(giras):
    path = get_giras_path()
    with open(path, "w", encoding="utf-8") as file:
        json.dump(giras, file, ensure_ascii=False, indent=2)


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
    giras = load_giras()
    return render_template(
        "agenda.html",
        title="Agenda",
        description="Confira a agenda de giras e encontros do Centro Espírita Ogum Naruê.",
        keywords="agenda, giras, encontros, espiritismo",
        giras=giras,
    )


@app.route("/admin/agendas", methods=["GET", "POST"])
def admin_agendas():
    giras = load_giras()

    if request.method == "POST":
        data = request.form.get("data", "")
        horario = request.form.get("horario", "")
        linha = request.form.get("linha", "")
        descricao = request.form.get("descricao", "")
        observacoes = request.form.get("observacoes", "")

        if data and horario and linha:
            giras.append(
                {
                    "data": data,
                    "horario": horario,
                    "linha": linha,
                    "descricao": descricao,
                    "observacoes": observacoes,
                }
            )
            save_giras(giras)
            return redirect(url_for("admin_agendas"))

    return render_template(
        "admin_agendas.html",
        title="Administração de Giras",
        description="Gerencie as giras que serão exibidas no site.",
        keywords="admin, agenda, giras, reuniões",
        giras=giras,
    )


@app.route('/admin')
@login_required
def admin_index():
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    return render_template('admin/dashboard.html', title='Dashboard')


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        token = request.form.get('csrf_token')
        if not validate_csrf(token):
            return render_template(
                'admin/login.html',
                error='CSRF inválido',
                supabase_enabled=is_supabase_auth_enabled(),
            )

        if is_supabase_auth_enabled():
            try:
                auth_data = supabase_sign_in(username, password)
                user_data = auth_data.get('user') or {}
                email = user_data.get('email', username).strip().lower()
                user_level = determine_user_level(email)
                if not user_level:
                    return render_template(
                        'admin/login.html',
                        error='Usuário autenticado, mas não autorizado ao painel administrativo.',
                        supabase_enabled=True,
                    )
                session['user'] = email
                session['user_level'] = user_level
                session['last_login'] = str(datetime.now())
                session.permanent = True
                record_audit(email, 'login', 'Login administrativo via Supabase', request.remote_addr)
                return redirect(url_for('admin_dashboard'))
            except Exception:
                return render_template(
                    'admin/login.html',
                    error='Credenciais inválidas',
                    supabase_enabled=True,
                )

        admin_user = os.environ.get('ADMIN_USER', 'admin')
        admin_pass = os.environ.get('ADMIN_PASS', 'admin')
        if username == admin_user and password == admin_pass:
            session['user'] = username
            session['user_level'] = UserLevel.PROGRAMADOR.value if username == admin_user else UserLevel.ADMINISTRADOR.value
            session['last_login'] = str(datetime.now())
            session.permanent = True
            record_audit(username, 'login', 'Login administrativo', request.remote_addr)
            return redirect(url_for('admin_dashboard'))

        return render_template(
            'admin/login.html',
            error='Credenciais inválidas',
            supabase_enabled=is_supabase_auth_enabled(),
        )

    generate_csrf_token()
    return render_template(
        'admin/login.html',
        supabase_enabled=is_supabase_auth_enabled(),
    )


@app.route('/admin/logout')
def admin_logout():
    user = session.pop('user', None)
    session.pop('user_level', None)
    session.pop('_csrf_token', None)
    record_audit(user or 'anonymous', 'logout', 'Logout administrativo', request.remote_addr)
    return redirect(url_for('admin_login'))


@app.route('/admin/usuarios')
@login_required
def admin_usuarios():
    return render_template('admin/usuarios.html', title='Usuários')


@app.route('/admin/usuarios/novo')
@login_required
def admin_usuario_novo():
    return render_template('admin/usuario_novo.html', title='Novo Usuário')


@app.route('/admin/configuracoes')
@login_required
def admin_configuracoes():
    return render_template('admin/configuracoes.html', title='Configurações')


@app.route('/admin/logs')
@programador_required
def admin_logs():
    return render_template('admin/logs.html', title='Logs')


@app.route('/admin/backup')
@programador_required
def admin_backup():
    return render_template('admin/backup.html', title='Backup')


@app.route('/admin/agenda')
@login_required
def admin_agenda():
    return render_template('admin/agenda.html', title='Agenda')


@app.route('/admin/membros')
@login_required
def admin_membros():
    return render_template('admin/membros.html', title='Membros')


@app.route('/admin/mensalidades')
@login_required
def admin_mensalidades():
    return render_template('admin/mensalidades.html', title='Mensalidades')


@app.route('/admin/financeiro')
@login_required
def admin_financeiro():
    return render_template('admin/financeiro.html', title='Financeiro')


@app.route('/admin/documentos')
@login_required
def admin_documentos():
    return render_template('admin/documentos.html', title='Documentos')


@app.route('/admin/relatorios')
@login_required
def admin_relatorios():
    return render_template('admin/relatorios.html', title='Relatórios')


@app.route('/admin/usuarios/<int:id>')
@login_required
def admin_usuario_detalhes(id):
    return render_template('admin/usuario_detalhes.html', title='Detalhes do Usuário')


@app.route('/admin/acesso-negado')
def admin_access_denied():
    return render_template('admin/acesso_negado.html'), 403


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
