from flask import Flask, render_template, request, redirect, session, flash
from Entity.Produto import Produto

app = Flask(__name__)
app.secret_key = 'Aur0r4'
tm = Produto("Tulipa Marroquina", "Tulipa originária do Marrocos, ou não existe", "Flor", "2.50")
rosa = Produto("Rosa", "Rosa cor de rosa", "Flor", "1.00")
marg = Produto("Margarida", "Margarida amarela", "Flor", "1.20")
produtos = [tm, rosa, marg]

@app.route('/')
def index():
    if 'usuario' not in session or session['usuario'] == None:
        return redirect('/login')
    return render_template("Produto/index.html", produtos=produtos, titulo="Produtos", titulo_page="Floricultura AURORA")

@app.route('/produto/cadastro')
def cadastro_produto():
    if 'usuario' not in session or session['usuario'] == None:
        return redirect('/login?po=produto/cadastro')
    return render_template("Produto/Cadastro/index.html", titulo="Novo Produto", titulo_page="Cadastro de Produtos")

@app.route('/produto/create', methods=['POST',])
def create_produto():
    if 'usuario' not in session or session['usuario'] == None:
        return redirect('/login')
    nome = request.form['nome']
    descricao = request.form['descricao']
    tipo = request.form['tipo']
    custoUnidade = request.form['custoUnidade']
    produto = Produto(nome, descricao, tipo, custoUnidade)
    produtos.append(produto)
    #return render_template("index.html", produtos=produtos)
    return redirect('/')

@app.route('/login', methods=['POST', 'GET'])
def login():
    origem = request.args.get('po')
    if request.method == 'POST':
        print('POST')
        if 'admin@admin' == request.form['email'] and 'admin' == request.form['password']:
            print('ok')
            session['usuario'] = "admin"
            pag_origem = request.form['origem']
            return redirect('/' + pag_origem)
        else:
            print('erro')
            flash('E-mail ou senha incorretos')
            return render_template('Login/index.html')
    elif request.method == 'GET':
        print('GET')
        return render_template('Login/index.html', origem=origem)

@app.route('/logout', methods=['POST'])
def logout():
    session['usuario'] = None
    return redirect('/login')

app.run(debug=True)
