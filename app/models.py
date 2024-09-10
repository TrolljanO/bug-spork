from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Tabela 'vendedores'
class Vendedor(db.Model):
    __tablename__ = 'vendedores'
    __table_args__ = {'schema': 'limpa_nome'}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('site.user.id'), nullable=False)
    afiliado_id = db.Column(db.Integer, db.ForeignKey('limpa_nome.vendedores.id'), nullable=True)  # FK para o afiliador (vendedor superior)
    id_encadeado = db.Column(db.String(255), nullable=False)  # ID hierárquico encadeado
    indicacoes = db.Column(db.Integer, default=0)
    vendas_fechadas = db.Column(db.Integer, default=0)
    vendas_concluidas = db.Column(db.Integer, default=0)
    afiliados = db.Column(db.Integer, default=0)
    comissao_acumulada = db.Column(db.Numeric(10, 2), default=0.00)
    data_ultima_venda = db.Column(db.Date)
    status = db.Column(db.String(50), default='Ativo')
    data_criacao = db.Column(db.Date, default=db.func.current_date())
    telefone = db.Column(db.String(20))
    tipo_vendedor = db.Column(db.String(50), default='Afiliado')

    # Relacionamento com o usuário
    user = db.relationship('User', backref=db.backref('vendedor', lazy=True))

# Tabela 'clientes'
class Cliente(db.Model):
    __tablename__ = 'clientes'
    __table_args__ = {'schema': 'limpa_nome'}

    id = db.Column(db.Integer, primary_key=True)
    vendedor_id = db.Column(db.Integer, db.ForeignKey('limpa_nome.vendedores.id'), nullable=False)  # FK para a tabela 'vendedores'
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

# Tabela 'vendas'
class Venda(db.Model):
    __tablename__ = 'vendas'
    __table_args__ = {'schema': 'limpa_nome'}

    id = db.Column(db.Integer, primary_key=True)
    vendedor_id = db.Column(db.Integer, db.ForeignKey('limpa_nome.vendedores.id'), nullable=False)  # FK para a tabela 'vendedores'
    cliente_id = db.Column(db.Integer, db.ForeignKey('limpa_nome.clientes.id'), nullable=False)  # FK para a tabela 'clientes'
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

# Tabela 'comissao'
class Comissao(db.Model):
    __tablename__ = 'comissao'
    __table_args__ = {'schema': 'limpa_nome'}

    id = db.Column(db.Integer, primary_key=True)
    vendedor_id = db.Column(db.Integer, db.ForeignKey('limpa_nome.vendedores.id'), nullable=False)  # FK para a tabela 'vendedores'
    afiliado_id = db.Column(db.Integer, db.ForeignKey('limpa_nome.vendedores.id'), nullable=False)  # FK para a tabela 'vendedores'
    valor_comissao = db.Column(db.Numeric(10, 2), nullable=False)
    nivel = db.Column(db.Integer, nullable=False)
    data_comissao = db.Column(db.Date, default=db.func.current_date())
    status = db.Column(db.String(50), default='Pendente')
