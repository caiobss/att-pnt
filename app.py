# -*- coding: utf-8 -*-

from flask import (
    redirect, render_template, request, session, url_for, Flask
)

from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

SECRET_KEY = 'ETEPD - DEV - PNT1'


app = Flask(__name__)
app.secret_key = SECRET_KEY


#indicação do banco de dados
engine = create_engine("sqlite:///efn.db")
Session = sessionmaker(bind=engine)
Base = automap_base()
Base.prepare(engine, reflect=True)

# Tabelas existentes no SQLite
Pessoa = Base.classes.estudantes


#Tela inicial do sistema
@app.route('/')
def inicio():
    return render_template('index.html')

#tela com a lista de estudantes cadastrados
@app.route('/listar')
def listar_pessoas():
    sessionSQL = Session()
    # Listando todas pessoas
    pessoas = sessionSQL.query(Pessoa).all()
    sessionSQL.close()
    return render_template('listar.html', title='Listar', pessoas=pessoas)



@app.route('/editar', methods=['GET', 'POST'])
def editar():
    sessionSQL = Session()
    if request.method == 'GET':
        # pegar o id da pessoa via GET (parâmetro id na URL)
        pessoaId = str(request.args.get('id'))

        pessoa = sessionSQL.query(Pessoa).filter(Pessoa.id == pessoaId).first()

        if pessoa is None:
            return redirect(url_for('listar_pessoas'))
        
        # adicionando id da pessoa na sessão do usuário
        session['pessoaId'] = pessoaId
        return render_template('editar.html', title='Editar pessoa', pessoa=pessoa)
    else:
        # obtendo ids que estavam na sessão
        pessoaId = session['pessoaId']
        # limpando a sessão
        session.pop('pessoaId', None)
       
        # obtendo o novo valor que estava no campo 'nome' do formulário da página editar.html
        nome = request.form['nome']
        idade = request.form['idade']
        cpf = request.form['cpf']
        email = request.form['email']
        fone = request.form['fone']
        cidade = request.form['cidade']
        uf = request.form['uf']
        curso = request.form['curso']
        turma = request.form['turma']

        # buscando pela pessoa
        pessoa = sessionSQL.query(Pessoa).filter(Pessoa.id == pessoaId).first()

        # atualizando o nome da pessoa
        pessoa.nome = nome
        pessoa.idade = idade
        pessoa.cpf = cpf
        pessoa.email = email
        pessoa.fone = fone
        pessoa.cidade = cidade
        pessoa.uf = uf
        pessoa.curso = curso
        pessoa.turma = turma
        
        # persistindo os dados
        sessionSQL.commit()
        sessionSQL.close()
        #retornando para a página com a listagem
        return redirect(url_for('listar_pessoas'))


@app.route('/excluir', methods=['GET', 'POST'])
def excluir():
    sessionSQL = Session()
    if request.method == 'GET':
        # pegar o id da pessoa via GET (parâmetro id na URL)
        pessoaId = str(request.args.get('id'))
        pessoa = sessionSQL.query(Pessoa).filter(Pessoa.id == pessoaId).first()

        if pessoa is None:
            return redirect(url_for('listar_pessoas'))

        # adicionando id da pessoa na sessão do usuário
        session['pessoaId'] = pessoaId
        return render_template('excluir.html', title='Excluir pessoa', pessoa=pessoa)
    else:
        # obtendo ids que estavam na sessão
        pessoaId = session['pessoaId']
        # limpando a sessão
        session.pop('pessoaId', None)
        # buscando pela pessoa
        pessoa = sessionSQL.query(Pessoa).filter(Pessoa.id == pessoaId).first()
        
        # excluindo a pessoa
        sessionSQL.delete(pessoa)

        #persistindo os dados no banco
        sessionSQL.commit()
        sessionSQL.close()
        #redirecionando para a listagem
        return redirect(url_for('listar_pessoas'))


@app.route('/inserir', methods=['GET', 'POST'])
def inserir():
    if request.method == 'GET':
        return render_template('inserir.html', title='Adicionar pessoa')
    else:
        sessionSQL = Session()

        # obtendo o novo valor que estava no campo 'nome' do formulário da página editar.html
        nome = request.form['nome']
        idade = request.form['idade']
        cpf = request.form['cpf']
        email = request.form['email']
        fone = request.form['fone']
        cidade = request.form['cidade']
        uf = request.form['uf']
        curso = request.form['curso']
        turma = request.form['turma']

        pessoa = Pessoa()
        pessoa.nome = nome
        pessoa.idade = idade
        pessoa.cpf = cpf
        pessoa.email = email
        pessoa.fone = fone
        pessoa.cidade = cidade
        pessoa.uf = uf
        pessoa.curso = curso
        pessoa.turma = turma

        #persistindo os dados no banco
        sessionSQL.add(pessoa)
        sessionSQL.commit()
        sessionSQL.close()

        #redirecionando para a página de listagem
        return redirect(url_for('listar_pessoas'))


@app.route('/detalhar', methods=['GET', 'POST'])
def detalhar():
    sessionSQL = Session()
    if request.method == 'GET':
        # pegar o id da pessoa via GET (parâmetro id na URL)
        pessoaId = str(request.args.get('id'))

        #fazendo consulta ao banco de dados e guardando o resultado na variável pessoa.
        pessoa = sessionSQL.query(Pessoa).filter(Pessoa.id == pessoaId).first()

        if pessoa is None:
            return redirect(url_for('listar_pessoas'))

        
        # adicionando id da pessoa na sessão do usuário
        session['pessoaId'] = pessoaId

        #retorna par
       
        return render_template('detalhar.html', title='Editar pessoa', pessoa=pessoa)
    else:
        # obtendo ids que estavam na sessão
        pessoaId = session['pessoaId']
        # limpando a sessão
        session.pop('pessoaId', None)
       
        # obtendo o novo valor que estava no campo 'nome' do formulário da página editar.html
        nome = request.form['nome']
        idade = request.form['idade']
        cpf = request.form['cpf']
        email = request.form['email']
        fone = request.form['fone']
        cidade = request.form['cidade']
        uf = request.form['uf']
        curso = request.form['curso']
        turma = request.form['turma']

        # buscando pela pessoa
        pessoa = sessionSQL.query(Pessoa).filter(Pessoa.id == pessoaId).first()

        # atualizando o nome da pessoa
        pessoa.nome = nome
        pessoa.idade = idade
        pessoa.cpf = cpf
        pessoa.email = email
        pessoa.fone = fone
        pessoa.cidade = cidade
        pessoa.uf = uf
        pessoa.curso = curso
        pessoa.turma = turma
        

        # persistindo os dados
        sessionSQL.commit()
        sessionSQL.close()
        return redirect(url_for('listar_pessoas'))




if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)