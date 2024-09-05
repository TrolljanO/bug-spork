from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Vendedor(db.Model):
    __tablename__ = 'vendedores'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    indicacoes = db.Column(db.Integer, default=0)
    vendas_fechadas = db.Column(db.Integer, default=0)
    vendas_concluidas = db.Column(db.Integer, default=0)
    afiliados = db.Column(db.Integer, default=0)
    afiliados_ids = db.Column(db.Text)
    comissao_acumulada = db.Column(db.Numeric(10, 2), default=0.00)
    data_ultima_venda = db.Column(db.Date)
    status = db.Column(db.String(50), default='Ativo')
    data_criacao = db.Column(db.Date, default=db.func.current_date())
    telefone = db.Column(db.String(20))
    tipo_vendedor = db.Column(db.String(50), default='Afiliado')

    # Relacionamento com o usuário
    user = db.relationship('User', backref=db.backref('vendedor', lazy=True))


class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    vendedor_id = db.Column(db.Integer, db.ForeignKey('vendedores.id'))
    nome = db.Column(db.String(255), nullable=False)
    valor_divida = db.Column(db.Numeric(10, 2))
    status_pagamento = db.Column(db.String(50), default='Aguardando pagamento')
    status_contrato = db.Column(db.String(50), default='Aberto')
    afiliado_potencial = db.Column(db.Boolean, default=False)
    afiliado_id = db.Column(db.String(255))
    forma_pagamento = db.Column(db.String(50), default='Não Informado')
    data_pagamento = db.Column(db.Date)
    email = db.Column(db.String(255))
    telefone = db.Column(db.String(20))
    data_contrato = db.Column(db.Date)
    origem_lead = db.Column(db.String(100), default='Afiliado')
    documentos_recebidos = db.Column(db.Boolean, default=False)


class Venda(db.Model):
    __tablename__ = 'vendas'
    id = db.Column(db.Integer, primary_key=True)
    vendedor_id = db.Column(db.Integer, db.ForeignKey('vendedores.id'))
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    valor_venda = db.Column(db.Numeric(10, 2), default=1500.00)
    status = db.Column(db.String(50), default='Aguardando Fechamento')
    data_venda = db.Column(db.Date)
    data_conclusao = db.Column(db.Date)
    forma_pagamento = db.Column(db.String(50), default='Não Informado')
    data_pagamento = db.Column(db.Date)
    numero_parcelas = db.Column(db.Integer, default=1)
    valor_pago = db.Column(db.Numeric(10, 2))
    data_cancelamento = db.Column(db.Date)
    motivo_cancelamento = db.Column(db.String(255))
    status_pagamento = db.Column(db.String(50), default='Pendente')
    tipo_venda = db.Column(db.String(50), default='Limpa Nome')
