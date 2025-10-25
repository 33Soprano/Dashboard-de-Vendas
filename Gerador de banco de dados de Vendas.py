import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

# Configurar Faker para português
fake = Faker('pt_BR')

class GeradorDadosLojas:
    def __init__(self):
        self.fake = fake
        self.categorias = ['Eletrônicos', 'Roupas', 'Casa', 'Esportes', 'Beleza']
        self.metodos_pagamento = ['Cartão Crédito', 'Cartão Débito', 'PIX', 'Boleto']
        self.generos = ['M', 'F', 'Outro']
        
    def gerar_customers(self, quantidade=50):
        """Gera tabela de clientes"""
        customers = []
        for i in range(quantidade):
            customers.append({
                'customer_id': i + 1,
                'nome': self.fake.name(),
                'cidade': self.fake.city(),
                'genero': random.choice(self.generos),
                'idade': random.randint(18, 70)
            })
        return pd.DataFrame(customers)
    
    def gerar_products(self, quantidade=30):
        """Gera tabela de produtos"""
        products = []
        for i in range(quantidade):
            categoria = random.choice(self.categorias)
            # Preços variam por categoria
            if categoria == 'Eletrônicos':
                preco = round(random.uniform(500, 5000), 2)
            elif categoria == 'Roupas':
                preco = round(random.uniform(50, 300), 2)
            else:
                preco = round(random.uniform(30, 800), 2)
                
            products.append({
                'product_id': i + 1,
                'categoria': categoria,
                'preco': preco,
                'estoque': random.randint(0, 100)
            })
        return pd.DataFrame(products)
    
    def gerar_orders(self, customers_df, products_df, quantidade=200):
        """Gera tabela de pedidos (relaciona clientes e produtos)"""
        orders = []
        for i in range(quantidade):
            customer_id = random.choice(customers_df['customer_id'].tolist())
            product_id = random.choice(products_df['product_id'].tolist())
            
            # Buscar preço do produto
            preco_produto = products_df[products_df['product_id'] == product_id]['preco'].values[0]
            quantidade_pedido = random.randint(1, 5)
            valor_total = round(preco_produto * quantidade_pedido, 2)
            
            # Data aleatória nos últimos 6 meses
            data_pedido = self.fake.date_between(start_date='-6m', end_date='today')
            
            orders.append({
                'order_id': i + 1,
                'customer_id': customer_id,
                'product_id': product_id,
                'data': data_pedido,
                'quantidade': quantidade_pedido,
                'valor_total': valor_total,
                'metodo_pagamento': random.choice(self.metodos_pagamento)
            })
        return pd.DataFrame(orders)
    
    def gerar_sales_targets(self, meses=12):
        """Gera tabela de metas de vendas por categoria"""
        sales_targets = []
        ano_atual = datetime.now().year
        
        for mes in range(1, meses + 1):
            for categoria in self.categorias:
                # Meta base varia por categoria
                if categoria == 'Eletrônicos':
                    meta_base = random.randint(50000, 100000)
                elif categoria == 'Roupas':
                    meta_base = random.randint(30000, 80000)
                else:
                    meta_base = random.randint(20000, 60000)
                
                # Ajuste sazonal
                if mes in [11, 12]:  # Nov/Dez - Natal
                    meta_base = int(meta_base * 1.3)
                elif mes in [6, 7]:  # Jun/Jul - Férias
                    meta_base = int(meta_base * 1.2)
                
                sales_targets.append({
                    'target_id': len(sales_targets) + 1,
                    'categoria': categoria,
                    'mes': mes,
                    'ano': ano_atual,
                    'meta_mensal': meta_base
                })
        return pd.DataFrame(sales_targets)

    def exportar_para_excel(self):
        """Gera todas as tabelas e exporta para Excel"""
        
        print("Gerando dados...")
        
        # Gerar dados
        customers_df = self.gerar_customers(50)
        products_df = self.gerar_products(30)
        orders_df = self.gerar_orders(customers_df, products_df, 200)
        sales_targets_df = self.gerar_sales_targets(12)
        
        # Criar arquivo Excel com múltiplas abas
        with pd.ExcelWriter('loja_dados_completos.xlsx', engine='openpyxl') as writer:
            customers_df.to_excel(writer, sheet_name='customers', index=False)
            products_df.to_excel(writer, sheet_name='products', index=False)
            orders_df.to_excel(writer, sheet_name='orders', index=False)
            sales_targets_df.to_excel(writer, sheet_name='sales_targets', index=False)
        
        print("✅ Arquivo 'loja_dados_completos.xlsx' criado com sucesso!")
        print(f"📊 Resumo:")
        print(f"   - Customers: {len(customers_df)} registros")
        print(f"   - Products: {len(products_df)} registros")
        print(f"   - Orders: {len(orders_df)} registros")
        print(f"   - Sales Targets: {len(sales_targets_df)} registros")
        
        return customers_df, products_df, orders_df, sales_targets_df

    def mostrar_relacionamentos(self, customers_df, products_df, orders_df):
        """Demonstra como as tabelas se relacionam"""
        print("\n🔗 EXEMPLOS DE RELACIONAMENTOS:")
        
        # Pegar alguns exemplos
        exemplos_orders = orders_df.head(3)
        
        for _, order in exemplos_orders.iterrows():
            customer = customers_df[customers_df['customer_id'] == order['customer_id']].iloc[0]
            product = products_df[products_df['product_id'] == order['product_id']].iloc[0]
            
            print(f"Pedido {order['order_id']}:")
            print(f"  Cliente: {customer['nome']} ({customer['cidade']})")
            print(f"  Produto: {product['categoria']} - R$ {product['preco']}")
            print(f"  Valor Total: R$ {order['valor_total']}")
            print(f"  Data: {order['data']}")
            print("  ---")

# Executar
if __name__ == "__main__":
    gerador = GeradorDadosLojas()
    
    # Gerar e exportar dados
    customers, products, orders, targets = gerador.exportar_para_excel()
    
    # Mostrar exemplos de relacionamentos
    gerador.mostrar_relacionamentos(customers, products, orders)
    
    # Mostrar primeiros registros de cada tabela
    print("\n📋 PRIMEIROS REGISTROS DE CADA TABELA:")
    print("\nCUSTOMERS:")
    print(customers.head(3))
    
    print("\nPRODUCTS:")
    print(products.head(3))
    
    print("\nORDERS:")
    print(orders.head(3))
    
    print("\nSALES_TARGETS:")
    print(targets.head(10))  # Mostra mais para ver diferentes categorias