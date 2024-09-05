from flask import Blueprint, jsonify, request, abort
from app.models import db, Vendedor, Cliente, Venda

main = Blueprint('main', __name__)


# Exemplo de uma função auxiliar para gerar respostas padronizadas
def json_response(data=None, message="Success", status=200):
    response = {
        "message": message,
        "data": data
    }
    return jsonify(response), status


# --------------------- ROTAS DOS VENDEDORES -----------------------

@main.route('/vendedores', methods=['GET'])
def get_vendedores():
    vendedores = Vendedor.query.all()
    resultado = [
        {
            "id": v.id,
            "nome": v.user.nome,  # Assumindo que há uma relação com o modelo User
            "indicacoes": v.indicacoes,
            "vendas_fechadas": v.vendas_fechadas,
            "vendas_concluidas": v.vendas_concluidas,
            "afiliados": v.afiliados,
            "comissao_acumulada": str(v.comissao_acumulada)
        } for v in vendedores
    ]
    return json_response(data=resultado)


@main.route('/vendedores/<int:id>', methods=['GET'])
def get_vendedor(id):
    vendedor = Vendedor.query.get(id)
    if not vendedor:
        return json_response(message="Vendedor não encontrado", status=404)

    vendedor_data = {
        "id": vendedor.id,
        "nome": vendedor.user.nome,  # Supondo relacionamento com tabela de usuários
        "indicacoes": vendedor.indicacoes,
        "vendas_fechadas": vendedor.vendas_fechadas,
        "vendas_concluidas": vendedor.vendas_concluidas,
        "afiliados": vendedor.afiliados,
        "comissao_acumulada": str(vendedor.comissao_acumulada)
    }
    return json_response(data=vendedor_data)


@main.route('/vendedores', methods=['POST'])
def create_vendedor():
    data = request.json
    if not data.get('user_id'):
        return json_response(message="ID de usuário é obrigatório", status=400)

    novo_vendedor = Vendedor(
        user_id=data['user_id'],
        indicacoes=0,
        vendas_fechadas=0,
        vendas_concluidas=0,
        afiliados=0,
        comissao_acumulada=0.00
    )
    db.session.add(novo_vendedor)
    db.session.commit()
    return json_response(data={"id": novo_vendedor.id}, message="Vendedor criado com sucesso", status=201)


# --------------------- ROTAS DOS CLIENTES -----------------------

@main.route('/clientes', methods=['GET'])
def get_clientes():
    clientes = Cliente.query.all()
    resultado = [
        {
            "id": c.id,
            "nome": c.nome,
            "vendedor_id": c.vendedor_id,
            "valor_divida": str(c.valor_divida),
            "status_pagamento": c.status_pagamento,
            "status_contrato": c.status_contrato
        } for c in clientes
    ]
    return json_response(data=resultado)


@main.route('/clientes/<int:id>', methods=['GET'])
def get_cliente(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return json_response(message="Cliente não encontrado", status=404)

    cliente_data = {
        "id": cliente.id,
        "nome": cliente.nome,
        "vendedor_id": cliente.vendedor_id,
        "valor_divida": str(cliente.valor_divida),
        "status_pagamento": cliente.status_pagamento,
        "status_contrato": cliente.status_contrato
    }
    return json_response(data=cliente_data)


@main.route('/clientes', methods=['POST'])
def create_cliente():
    data = request.json
    if not data.get('nome') or not data.get('vendedor_id'):
        return json_response(message="Nome e ID do vendedor são obrigatórios", status=400)

    novo_cliente = Cliente(
        nome=data['nome'],
        vendedor_id=data['vendedor_id'],
        valor_divida=data.get('valor_divida', 0.00),
        status_pagamento="Aguardando pagamento",
        status_contrato="Aberto"
    )
    db.session.add(novo_cliente)
    db.session.commit()
    return json_response(data={"id": novo_cliente.id}, message="Cliente criado com sucesso", status=201)


# --------------------- ROTAS DAS VENDAS -----------------------

@main.route('/vendas', methods=['GET'])
def get_vendas():
    vendas = Venda.query.all()
    resultado = [
        {
            "id": v.id,
            "vendedor_id": v.vendedor_id,
            "cliente_id": v.cliente_id,
            "valor_venda": str(v.valor_venda),
            "status": v.status,
            "data_venda": v.data_venda.strftime("%Y-%m-%d") if v.data_venda else None,
            "data_conclusao": v.data_conclusao.strftime("%Y-%m-%d") if v.data_conclusao else None
        } for v in vendas
    ]
    return json_response(data=resultado)


@main.route('/vendas/<int:id>', methods=['GET'])
def get_venda(id):
    venda = Venda.query.get(id)
    if not venda:
        return json_response(message="Venda não encontrada", status=404)

    venda_data = {
        "id": venda.id,
        "vendedor_id": venda.vendedor_id,
        "cliente_id": venda.cliente_id,
        "valor_venda": str(venda.valor_venda),
        "status": venda.status,
        "data_venda": venda.data_venda.strftime("%Y-%m-%d") if venda.data_venda else None,
        "data_conclusao": venda.data_conclusao.strftime("%Y-%m-%d") if venda.data_conclusao else None
    }
    return json_response(data=venda_data)


@main.route('/vendas', methods=['POST'])
def create_venda():
    data = request.json
    if not data.get('vendedor_id') or not data.get('cliente_id'):
        return json_response(message="ID do vendedor e cliente são obrigatórios", status=400)

    nova_venda = Venda(
        vendedor_id=data['vendedor_id'],
        cliente_id=data['cliente_id'],
        valor_venda=data.get('valor_venda', 1500.00),
        status="Aguardando Fechamento"
    )
    db.session.add(nova_venda)
    db.session.commit()
    return json_response(data={"id": nova_venda.id}, message="Venda criada com sucesso", status=201)
