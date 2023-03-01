from datetime import date, datetime
import datetime as dt
from django.shortcuts import redirect, render
from django.contrib import auth, messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum

from django.db.models import Q
from sistema.relatorios.recibo import Recibo

from django.http import HttpResponse

from sistema.funcoes import stringToFloat, datas_mes_atual, periodos_data, total_vendas_ultimos_meses, \
    vendas_status_mes

from sistema.models import CategoriaProduto, EmbalagemProducaoQueijo, ItemVenda, Estoque, Fornecedor, Producao,\
    Produto, RecebimentoLeite, Cliente, TipoProduto, Venda, PessoaFisica, PessoaJuridica

class login(View):
    template_name = 'login.html'

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('home')

        if request.method != 'POST':
            return render(request, 'login.html')

        user = request.POST.get('usuario')
        password = request.POST.get('senha')

        if not user or not password:
            messages.error(request, "Preencha todos os campos")
            return render(request, 'login.html')

        userAuth = auth.authenticate(request, username=user, password=password)

        if not userAuth:
            messages.error(request, "Usuario ou senha Incorretos")
            return render(request, 'login.html')

        else:
            auth.login(request, userAuth)
            messages.success(request, "Usuario logado com sucesso")
            return redirect('home')

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')

        if request.method != 'POST':
            return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

class home(LoginRequiredMixin, View):
    login_url = 'login/'

    def get(self, request):
        leites = RecebimentoLeite.objects.all()

        for i in leites:
            i.valor = i.quantidade * i.fornecedor.preco_leite
            i.save()

        datas = datas_mes_atual()

        hoje = date.today()

        m900 = ItemVenda.objects.filter(~Q(venda_id=277), produto__nome='IOGURTE MORANGO 900G', venda__data__month=hoje.month,
                                        venda__data__year=hoje.year)
        m450 = ItemVenda.objects.filter(~Q(venda_id=277), produto__nome='IOGURTE MORANGO 450G', venda__data__month=hoje.month,
                                        venda__data__year=hoje.year)
        n900 = ItemVenda.objects.filter(~Q(venda_id=277), produto__nome='IOGURTE NATURAL 900G', venda__data__month=hoje.month,
                                        venda__data__year=hoje.year)
        n450 = ItemVenda.objects.filter(~Q(venda_id=277), produto__nome='IOGURTE NATURAL 450G', venda__data__month=hoje.month,
                                        venda__data__year=hoje.year)
        ma900 = ItemVenda.objects.filter(~Q(venda_id=277), produto__nome='IOGURTE MARACUJÁ 900G', venda__data__month=hoje.month,
                                         venda__data__year=hoje.year)
        ma450 = ItemVenda.objects.filter(~Q(venda_id=277), produto__nome='IOGURTE MARACUJÁ 450G', venda__data__month=hoje.month,
                                         venda__data__year=hoje.year)

        tm900 = 0
        for i in m900:
            tm900 += i.quantidade

        tm450 = 0
        for i in m450:
            tm450 += i.quantidade

        tn900 = 0
        for i in n900:
            tn900 += i.quantidade

        tn450 = 0
        for i in n450:
            tn450 += i.quantidade

        tma900 = 0
        for i in ma900:
            tma900 += i.quantidade

        tma450 = 0
        for i in ma450:
            tma450 += i.quantidade



        #print(f"MORANGO 900: {tm900} --- 450: {tm450}")
        #print(f"NATURAL 900: {tn900} --- 450: {tn450}")
        #print(f"MARACUJÁ 900: {tma900} --- 450: {tma450}")


        produtos = Produto.objects.filter(categoria=1)
        #print(produtos)
        hoje = date.today()
        items = ItemVenda.objects.filter(venda__data__month=hoje.month)
        #print(items)

        p = {}
        for i in produtos:
            p[i.nome] = []

        total = 0
        for i in items:
            p[i.produto.nome].append(i.quantidade)
            total+= i.total

        for i, j in p.items():
            if sum(j) != 0:
                #print("{} = {:.2f}kg --- rótulos = {:.2f}".format(i, sum(j), int(sum(j)*4)))
                pass

        hoje = date.today()

        estoques = Estoque.objects.filter(produto__categoria__id=1).order_by('-quantidade')
        for item in estoques:
            item.quantidade = int(item.quantidade)

        fornecedores = RecebimentoLeite.objects.filter(data__year=hoje.year, data__month=hoje.month).distinct(
            'quantidade')

        fornecedores = Fornecedor.objects.all()

        recebimentos = []
        for i in fornecedores:
            try:
                recebimentos.append({
                    'fornecedor' : i.nome,
                    'quantidade': int(RecebimentoLeite.objects.filter(
                    data__year=hoje.year, data__month=hoje.month, fornecedor=i).aggregate(Sum(
                    'quantidade'))['quantidade__sum'])
                })
            except:
                pass
        try:
           v =  int(Venda.objects.filter(data__year=hoje.year, data__month=hoje.month).aggregate(Sum(
                'total'))['total__sum'])
        except:
            v=0

        context = {
                'user' : request.user,
                'vendas' : total_vendas_ultimos_meses(6),
                'vendas_atual' : vendas_status_mes(),
                'vendas_total' : v,
                'estoques' : estoques,
                'recebimentos' : recebimentos
            }

        cliente = Cliente.objects.all()

        """for i in cliente:
            dados = {
                'periodo': datas, 
                'cliente' : Cliente.objects.filter(id=i.id),
                'vendas': Venda.objects.filter(data__range=(datas[0], datas[1]), cliente=i.id, status='Em Aberto').order_by('data'),
                'total': Venda.objects.filter(data__range=(datas[0], datas[1]), cliente=i.id, status='Em Aberto').aggregate(Sum('total'))
            }
            
            if dados['total']['total__sum'] != None:
                rel.gerar_relatorio_mensal(dados, f"relatorio_{i}.pdf")"""

        #ex1 = pd.DataFrame(Venda.objects.filter(data__range=(datas[0], datas[1]), cliente=1).order_by('data').values())
        #ex2 = pd.DataFrame(Venda.objects.filter(data__range=(datas[0], datas[1]), cliente=2).order_by('data').values())
        #ex = pd.DataFrame(RecebimentoLeite.objects.filter(data__range=(datas[0], datas[1])).order_by('data').values())
        #ex.to_excel("output.xlsx", index=False)

        return render(request, 'home.html', context)

class recebimento_leite(LoginRequiredMixin, View):
    login_url = 'login/'


    def get(self, request):
        datas = datas_mes_atual()
        context = {
                'user' : request.user,
                'fornecedores': Fornecedor.objects.all(),
                'leites' : RecebimentoLeite.objects.filter(data__range=(datas[0], datas[1])),
                'filtro': "Filtro: mês atual"
            }

        return render(request, 'producao/recebimento_leite.html', context)

        
    def post(self, request):
        datas = datas_mes_atual()
        context = {
                'user' : request.user,
                'fornecedores': Fornecedor.objects.all(),
                'leites' : RecebimentoLeite.objects.filter(data__range=(datas[0], datas[1])),
                'filtro': "Filtro: mês atual"
            }
        
        if request.POST.get('filtro', False) == 'filtro':

            data_inicio = request.POST.get('data_inicio')
            data_fim = request.POST.get('data_fim')

            if request.POST.get('periodos') != '':
                data_inicio, data_fim = periodos_data(request.POST.get('periodos'))

            context['leites'] = RecebimentoLeite.objects.filter(data__range=(data_inicio, data_fim))
            print(context['leites'])
            context['filtro'] = f"Filtro: {data_inicio} à {data_fim}"
            print(context['leites'])
            return render(request, 'producao/recebimento_leite.html', context)
        
        else:
            dados = request.POST
            fornecedor = Fornecedor.objects.get(nome=dados.get('fornecedor'))
            RecebimentoLeite.objects.create(data=dados.get('data'), fornecedor=fornecedor, quantidade=dados.get('qnt'),
                                            valor=(int(dados.get('qnt'))*fornecedor.preco_leite))
            messages.success(request,
                             f"Recebimento de leite de {fornecedor.nome} {dados.get('qnt')}L adicionado com sucesso.")
        
        return render(request, 'producao/recebimento_leite.html', context)

class produção_diaria(LoginRequiredMixin, View):
    login_url = 'login/'


    def get(self, request):
        datas = datas_mes_atual()
        table = Producao.objects.filter(data__range=(datas[0], datas[1]))
        try:
            lote = Producao.objects.values_list('id').last()[0] + 1
        except:
            lote = 1

        context = {
                'user' : request.user,
                'produtos': Produto.objects.filter(tipo=TipoProduto.objects.get(nome='Queijo')),
                'lote': lote,
                'producoes': table
            }

        return render(request, 'producao/producao_diaria.html', context)
        
    def post(self, request):
        try:
            lote = Producao.objects.values_list('id').last()[0] + 1
        except:
            lote = 1
        
        context = {
                'user' : request.user,
                'produtos': Produto.objects.filter(tipo=TipoProduto.objects.get(nome='Queijo')),
                'lote': lote,
            }

        if request.POST.get('filtro', False) == 'filtro':
            context['producoes'] = Producao.objects.filter(data__range=(request.POST.get('data_inicio'), request.POST.get('data_fim')))
            context['filtro'] = f"Filtro: {request.POST.get('data_inicio')} à {request.POST.get('data_fim')}"
            return render(request, 'producao/producao_diaria.html', context)

        try:
            lote = Producao.objects.values_list('id').last()[0] + 1
        except:
            lote = 1

        dados = request.POST

        dados = {
            'lote' : dados.get('lote'),
            'data' : dados.get('data'),
            'produto' : Produto.objects.filter(nome=dados.get('produto')).first(),
            'leite' : dados.get('leite'),
            'sal' : dados.get('sal'),
            'açucar' : dados.get('açucar'),
            'peso' : dados.get('peso'),
            'rendimento' : dados.get('rendimento'),
            'observação' : dados.get('observação'),
        }

        datas = datas_mes_atual()
        context = {
                'user' : request.user,
                'produtos': Produto.objects.all(),
                'lote': lote,
                'dados': dados,
                'producoes': Producao.objects.filter(data__range=(datas[0], datas[1])),
            }

        if dados['lote'] == '' or dados['data'] == '' or dados['produto'] == '' or dados['leite'] == '' or dados['peso'] == '':
            messages.error(request, "Os campos (lote, data, produto, leite, peso) não podem estar vazios. Preencha-os corretamente.")
            return render(request, 'producao/producao_diaria.html', context)

        if dados['sal'] == '' and dados['açucar'] == '':
            messages.error(request, "Um dos campos (sal, açucar) deve ser preenchido.")
            return render(request, 'producao/producao_diaria.html', context)

        if dados['sal'] != '' and dados['açucar'] != '':
            messages.error(request, "Apenas um dos campos (sal, açucar) deve ser preenchido.")
            return render(request, 'producao/producao_diaria.html', context)

        if dados['sal'] == '':
            dados['sal'] = 0

        if dados['açucar'] == '':
            dados['açucar'] = 0

        dados['rendimento'] = stringToFloat(dados['leite']) / stringToFloat(dados['peso'])
        
        if dados['observação'] == '':
            dados['observação'] = ''

        Producao.objects.create(
            lote = dados['lote'],
            data = dados['data'],
            produto = dados['produto'],
            leite = dados['leite'],
            sal = dados['sal'],
            peso = dados['peso'],
            acucar = dados['açucar'],
            rendimento = dados['rendimento'],
            observacao = dados['observação'],
        )

        try:
            estoque = Estoque.objects.filter(produto=dados['produto']).first()
            qnt = estoque.quantidade
            peso = dados['peso']
            total = qnt+float(peso)
            estoque.quantidade = total
            estoque.save()
        except:
            if dados['produto'].tipo.nome == 'Queijo':
                uni = 'KG'
            else:
                uni = 'UNI'
            Estoque.objects.create(
                produto = dados['produto'],
                quantidade = dados['peso'],
                unidade = uni 
            )
        
        

        estoque = EmbalagemProducaoQueijo.objects.get(nome = Produto.objects.get(nome=dados['produto']))

        qntEmbalagens = int(float(dados['peso'])*estoque.quantidade)

        estoque.embalagem.quantidade = estoque.embalagem.quantidade - qntEmbalagens
        estoque.rotulo.quantidade = estoque.rotulo.quantidade - qntEmbalagens

        estoque.embalagem.save()
        estoque.rotulo.save()

        context['dados'] = {
            'leite' : '',
            'sal' : '',
            'açucar' : '',
            'peso' : '',
            'rendimento' : '',
            'observação' : '',
        }

        messages.success(request, "Produção inserida com sucesso.")
        return redirect('producao-diaria')

class clientes(LoginRequiredMixin, View):
    login_url = 'login/'

    def get(self, request):
        cliente = Cliente.objects.all()
        context = {
            'user' : request.user,
            'clientes' : cliente
            }
        return render(request, 'clientes/clientes.html', context)

    def post(self, request):
        cliente = Cliente.objects.all()
        context = {
            'user': request.user,
            'clientes': cliente
        }

        if request.POST.get('salvar', False) == 'salvar':
            cadastro = None
            if request.POST.get('tipo') == 'PJ':
                cadastro = PessoaJuridica(
                    nome = request.POST.get('nome'),
                    endereco = request.POST.get('endereco'),
                    telefone = request.POST.get('telefone'),
                    email = request.POST.get('email'),
                    razao_social = request.POST.get('razao_sobrenome'),
                    cnpj = request.POST.get('cpf_cnpj'),
                    inscricao_estadual = request.POST.get('inscricao_estadual'),
                )
            elif request.POST.get('tipo') == 'PF':
                cadastro = PessoaFisica(
                    nome=request.POST.get('nome'),
                    endereco=request.POST.get('endereco'),
                    telefone=request.POST.get('telefone'),
                    email=request.POST.get('email'),
                    sobrenome=request.POST.get('razao_sobrenome'),
                    cpf=request.POST.get('cpf_cnpj'),
                )

            try:
                cadastro.save()

                obj = Cliente(content_object=cadastro)
                obj.save()
                messages.success(request, f"Cliente '{cadastro.nome}' cadastrado com sucesso!")
            except:
                messages.error(request, f"Preencha todos os campos corretamente.")
            return render(request, 'clientes/clientes.html', context)


class clientesDetalhes(LoginRequiredMixin, View):

    def get(self, request, pk):
        cliente = Cliente.objects.get(id=pk)
        context = {
            'user': request.user,
            'id': cliente.id,
            "cliente": cliente.content_object,
        }
        if isinstance(context['cliente'], PessoaFisica):
            context['tipo'] = 'PF'
        else:
            context['tipo'] = 'PJ'

        return render(request, 'clientes/cliente-detalhes.html', context)

    def post(self, request, pk):
        if request.POST.get('editForm', False) == 'editForm':
            try:
                cliente = Cliente.objects.get(id = request.POST.get('id'))
                obj = cliente.content_object
    
                obj.nome = request.POST.get('nome')
                obj.endereco = request.POST.get('endereco')
                obj.telefone = request.POST.get('telefone')
                obj.email = request.POST.get('email')
    
                if request.POST.get('tipo') == 'Pessoa Jurídica':
                    obj.razao_social = request.POST.get('razao_sobrenome')
                    obj.cnpj = request.POST.get('cpf_cnpj')
                    obj.inscricao_estadual = request.POST.get('inscricao_estadual')
    
                elif request.POST.get('tipo') == 'Pessoa Física':
                    obj.sobrneome = request.POST.get('razao_sobrenome')
                    obj.cpf = request.POST.get('cpf_cnpj')
    
                obj.save()
    
                messages.success(request, "Alteração salva com sucesso.")
            except TypeError as r:
                print(r)
                messages.error(request, "Erro ao salvar edição, preencha os campos corretamente.")
            
        return redirect(f"/producao/cliente/{request.POST.get('id')}")


class estoque(LoginRequiredMixin, View):
    login_url = 'login/'

    def get(self, request):
        context = {
                'user' : request.user,
                'estoques': Estoque.objects.all(),
                'tipos': TipoProduto.objects.all(),
                'produtos': Produto.objects.filter(Q(categoria=CategoriaProduto.objects.get(nome='Compra Externa')) |
                                                   Q(categoria=CategoriaProduto.objects.get(nome='Produção Interna'))),
                'categorias': CategoriaProduto.objects.all(),
                'marcas': Produto.objects.values('marca').distinct()
            }
        return render(request, 'estoque/estoque.html', context)
    
    def post(self, request):
        post = request.POST

        dados = {
            'data': post.get('data'),
            'produto': post.get('produto'),
            'quantidade': post.get('quantidade')
        }

        context = {
                'user' : request.user,
                'estoques': Estoque.objects.all(),
                'tipos': TipoProduto.objects.all(),
                'categorias': CategoriaProduto.objects.all(),
                'produtos': Produto.objects.filter(Q(categoria=CategoriaProduto.objects.get(nome='Compra Externa')) |
                                                   Q(categoria=CategoriaProduto.objects.get(nome='Produção Interna'))),
                'marcas': Produto.objects.values('marca').distinct(),
                'dados': dados
            }

        if dados['data'] == '' or dados['produto'] == '' or dados['quantidade'] == '':
            messages.error(request, "Preencha os campos vazios.")
            return render(request, 'estoque/estoque.html', context)
        
        if float(dados['quantidade']) <= 0:
            messages.error(request, "Informe uma quantidade maior que 0.")
            return render(request, 'estoque/estoque.html', context)

        produto = Estoque.objects.get(produto = Produto.objects.get(nome=dados['produto']))
        produto.quantidade = produto.quantidade + float(dados['quantidade'])
        produto.save()

        if produto.produto.categoria == 'Produção Interna':
            estoque = EmbalagemProducaoQueijo.objects.get(nome=Produto.objects.get(nome=dados['produto']))
            qntEmbalagens = int(float(dados['quantidade']) * estoque.quantidade)
            estoque.embalagem.quantidade = estoque.embalagem.quantidade - qntEmbalagens
            estoque.rotulo.quantidade = estoque.rotulo.quantidade - qntEmbalagens
            estoque.embalagem.save()
            estoque.rotulo.save()

        messages.success(request, f"Adicionado {dados['quantidade']} {produto.unidade} ao estoque de {dados['produto']}. Novo estoque {produto.quantidade} {produto.unidade}.")
        return render(request, 'estoque/estoque.html', context)

class estoqueDetalhes(LoginRequiredMixin, View):
    
    def get(self, request, pk):
        objProduto = Produto.objects.get(id=pk)

        context = {
                'user' : request.user,
                'tipos': TipoProduto.objects.all(),
                'categorias': CategoriaProduto.objects.all(),
                'marcas': Produto.objects.values('marca').distinct(),
                'produto': objProduto,
                'estoque': Estoque.objects.get(produto=objProduto),
                'unidades': ['UNI', 'KG', 'PC']
            }
        return render(request, 'estoque/estoque-detalhes.html', context)
    
    def post(self, request, pk):
        post = request.POST
        objProduto = Produto.objects.get(id=pk)

        dados = {
            'tipo' : post.get('tipo'),
            'nome' : post.get('nome'),
            'categoria' : post.get('categoria'),
            'marca' : post.get('marca'),
            'codBarras' : post.get('codBarras'),
            'valCompra' : post.get('valCompra'),
            'valVenda' : post.get('valVenda'),
            'unidade': post.get('unidade')
        }

        context = {
                'user' : request.user,
                'tipos': TipoProduto.objects.all(),
                'categorias': CategoriaProduto.objects.all(),
                'marcas': Produto.objects.values('marca').distinct(),
                'produto': objProduto,
                'estoque': Estoque.objects.get(produto=objProduto),
                'unidades': ['UNI', 'KG', 'PC']
            }
        
        if dados['tipo'] == '' or dados['nome']  == '' or dados['unidade'] == '' or dados['categoria'] == '' or dados['marca'] == '' or dados['codBarras'] == '' or dados['valCompra'] == '' or dados['valVenda'] == '':
            messages.error(request, "Preencha os campos vazios.")
            return render(request, 'estoque/estoque-detalhes.html', context)
        
        objProduto.tipo = TipoProduto.objects.get(nome=dados['tipo'])
        objProduto.nome = dados['nome']
        objProduto.categoria = CategoriaProduto.objects.get(nome=dados['categoria'])
        objProduto.marca = dados['marca']
        objProduto.codBarras = dados['codBarras']
        objProduto.valorCompra = stringToFloat(dados['valCompra'])
        objProduto.valorVenda = stringToFloat(dados['valVenda'])

        estoque = Estoque.objects.get(produto=objProduto.id)
        estoque.unidade = dados['unidade']

        objProduto.save()
        estoque.save()

        messages.success(request, f"Produto atualizado com sucesso.")
        return redirect('estoque')

class cadastroProduto(estoque):

    def post(self, request):
        post = request.POST

        dados = {
            'tipo' : post.get('tipo'),
            'nome' : post.get('nome'),
            'categoria' : post.get('categoria'),
            'marca' : post.get('marca'),
            'codBarras' : post.get('codBarras'),
            'valCompra' : post.get('valCompra'),
            'valVenda' : post.get('valVenda'),
            'unidade': post.get('unidade')
        }

        context = {
                'user' : request.user,
                'estoques': Estoque.objects.all(),
                'tipos': TipoProduto.objects.all(),
                'categorias': CategoriaProduto.objects.all(),
                'marcas': Produto.objects.values('marca').distinct(),
                'dados': dados
            }


        if len(list(filter(lambda x: x.nome == dados['nome'] or x.nome == dados['nome'].title() or x.nome == dados['nome'].upper() or x.nome == dados['nome'].lower(), Produto.objects.filter(nome__contains = dados['nome'])))) != 0:
            messages.error(request, "Nome de produto já cadastrado.")
            return render(request, 'estoque/estoque.html', context)

        if dados['tipo'] == '' or dados['nome']  == '' or dados['unidade'] == '' or dados['categoria'] == '' or dados['marca'] == '' or dados['codBarras'] == '' or dados['valCompra'] == '' or dados['valVenda'] == '':
            messages.error(request, "Preencha os campos vazios.")
            return render(request, 'estoque/estoque.html', context)

        objProduto = Produto.objects.create(
            tipo = TipoProduto.objects.get(nome=dados['tipo']),
            nome = dados['nome'],
            categoria = CategoriaProduto.objects.get(nome=dados['categoria']),
            marca = dados['marca'],
            codBarras = dados['codBarras'],
            valorCompra = dados['valCompra'],
            valorVenda = dados['valVenda']
        )

        Estoque.objects.create(
            produto = objProduto,
            quantidade = 0,
            unidade = dados['unidade']
        )

        messages.success(request, "Novo produto inserido com sucesso.")
        return redirect('estoque')

class vendas(LoginRequiredMixin, View):
    login_url= 'login/'

    def get(self, request):
        request.session['listaVenda'] = {}
        request.session['contador'] = 0
        request.session['total'] = 0.00

        datas = datas_mes_atual()

        ObjVendas =  Venda.objects.filter(data__range=(datas[0], datas[1]))

        context = {
                'user' : request.user,
                'vendas': ObjVendas,
                'clientes': Cliente.objects.all(),
                'produtos': Produto.objects.filter(categoria='1'),
                'listaVenda': {},
                'clienteSelected': '',
                'data': '',
                'faturamentoSelected': '',
                'total': 0.00,
                "status": request.session['status'],
                "periodos": request.session['periodos'],
                "data_inicio": request.session['data_inicio'],
                'data_fim': request.session['data_fim'],
                "filtro": 'Filtro: mês atual',
                'hoje': datetime.now().date()
            }
        try:
            self.filtrar(request, context)
        except:
            pass
        return render(request, 'vendas/vendas.html', context)

    def post(self, request):
        if 'listaVenda' not in request.session:
            request.session['listaVenda'] = {}
        if 'contador' not in request.session:
            request.session['contador'] = 0
        if 'total' not in request.session:
            request.session['total'] = 0

        cont = request.session['contador']
        datas = datas_mes_atual()
        context = {
                'user' : request.user,
                'vendas': Venda.objects.filter(data__range=(datas[0], datas[1])),
                'clientes': Cliente.objects.all(),
                'produtos': Produto.objects.filter(categoria='1'),
                'status_venda': True,
                'clienteSelected': request.POST.get('cliente'),
                'data': request.POST.get('data'),
                'faturamentoSelected': request.POST.get('faturamento'),
                "status": request.POST.get('status'),
                "periodos": request.POST.get('periodos'),
                "data_inicio": request.POST.get('data_inicio'),
                'data_fim':request.POST.get('data_fim'),
                'hoje': datetime.now().date()
            }

        if request.POST.get('addProduto', False) == 'addProduto':
            request.session['status_venda'] = True
            if request.POST.get('produto') != '':
                produto = Estoque.objects.get(produto=Produto.objects.get(nome=request.POST.get('produto')))
                valorVenda = produto.produto.valorVenda
                if request.POST.get('valor') != '':
                    valorVenda = float(request.POST.get('valor'))
                if produto.quantidade < float(request.POST.get('quantidade')):
                    messages.error(request, "Quantidade não disponível no estoque.")
                    return render(request, 'vendas/vendas.html', context) 
                descProduto = produto.produto
                subTotal = float(request.POST.get('quantidade')) * valorVenda
                request.session['listaVenda'][cont] = {'produto': descProduto.nome, 'unidade':produto.unidade, 'valor':valorVenda, 'quantidade':request.POST.get('quantidade'), 'subtotal': "{:.2f}".format(subTotal)}
                request.session['contador']+=1
                request.session['total']+= subTotal
            else:
                messages.error(request, "Preencha os campos corretamente.")
            context['total']= "{:.2f}".format(request.session['total'])
            context['listaVenda'] = request.session['listaVenda']
            return render(request, 'vendas/vendas.html', context)

        elif request.POST.get('salvarVenda', False) == 'salvarVenda':

            if request.POST.get('cliente') != '' and request.POST.get('data') != '' and request.POST.get('faturamento') != '':
                
                context['total']= "{:.2f}".format(request.session['total'])
                context['status'] = False
                data = datetime.strptime(request.POST.get('data'), '%Y-%m-%d')
                faturamento = request.POST.get('faturamento').replace(' Dias', '')
                vencimento = data + dt.timedelta(days=int(faturamento))
                cliente = list(filter(lambda cliente: cliente.content_object.nome == request.POST.get('cliente') ,Cliente.objects.all()))
            
                venda = Venda.objects.create(
                    data = data,
                    cliente = Cliente.objects.get(id=cliente[0].id),
                    total = float(context['total']),
                    faturamento = request.POST.get('faturamento'),
                    vencimento = vencimento.strftime('%Y-%m-%d'),
                    status = 'Emitir Nota'
                )

                for item in request.session['listaVenda'].values():
                    ItemVenda.objects.create(
                        venda = venda,
                        valor = item['valor'],
                        produto = Produto.objects.get(nome = item['produto']),
                        quantidade = float(item['quantidade']),
                        total = item['subtotal']
                    )
                    produto = Estoque.objects.get(produto = Produto.objects.get(nome=item['produto']))
                    produto.quantidade = "{:.3f}".format(produto.quantidade - float(item['quantidade']))
                    produto.save()
                
                request.session['contador'] = 0
                request.session['total'] = 0
                context['clienteSelected'] = ''
                context['data'] = ''
                context['faturamentoSelected'] = ''
                context['listaVenda'] = {}
                del request.session['listaVenda']
                               
                messages.success(request, "Venda cadastrada com sucesso.")

                return render(request, 'vendas/vendas.html', context)
            else:
                context['listaVenda'] = request.session['listaVenda']
                context['total']= "{:.2f}".format(request.session['total'])
                request.session['status_venda'] = True
                messages.error(request, "Preencha os campos corretamente.")
            return redirect('vendas')

        elif request.POST.get('filtro', False) == 'filtro':
            request.session['status_venda'] = False
            request.session['status'] = request.POST.get('status')
            request.session['periodos'] = request.POST.get('periodos')
            request.session['data_inicio'] = request.POST.get('data_inicio')
            request.session['data_fim'] = request.POST.get('data_fim')

            self.filtrar(request, context)
            return render(request, 'vendas/vendas.html', context)

        return redirect('vendas')

    def filtrar(self, request, context):

        if request.session['status'] != '' and request.session['status'] != 'Vencido':
            status_post = True
        elif request.session['status']  != '' and request.session['status']  == 'Vencido':
            status_post = 'Vencido'
        else:
            status_post = False

        data_inicio = request.session['data_inicio']
        data_fim = request.session['data_fim']

        if request.session['periodos'] != '':
            data_inicio, data_fim = periodos_data(request.session['periodos'])

        if status_post is True:
            try:
                context['vendas'] = Venda.objects.filter(data__range=(data_inicio, data_fim),
                                                         status=request.session['status'])
            except:
                pass
        elif status_post == 'Vencido':
            try:
                context['vendas'] = Venda.objects.filter(data__range=(data_inicio, data_fim),
                                                         vencimento__lte=(datetime.now().date()), status='Em Aberto')
            except:
                pass
        else:
            try:
                context['vendas'] = Venda.objects.filter(data__range=(data_inicio, data_fim))
            except:
                pass

        context['filtro'] = f"Filtro: {data_inicio} à {data_fim}"
        context["status"]=request.session['status']
        context["periodos"]= request.session['periodos']
        context["data_inicio"]= request.session['data_inicio']
        context["data_fim"]= request.session['data_fim']

def nfe(request, pk):
    hoje = date.today()

    m900 = ItemVenda.objects.filter(produto__nome='IOGURTE MORANGO 900G', venda__data__month=hoje.month, venda__data__year=hoje.year)
    m450 = ItemVenda.objects.filter(produto__nome='IOGURTE MORANGO 450G', venda__data__month=hoje.month, venda__data__year=hoje.year)

    n900 = ItemVenda.objects.filter(produto__nome='IOGURTE NATURAL 900G', venda__data__month=hoje.month, venda__data__year=hoje.year)
    n450 = ItemVenda.objects.filter(produto__nome='IOGURTE NATURAL 450G', venda__data__month=hoje.month, venda__data__year=hoje.year)

    ma900 = ItemVenda.objects.filter(produto__nome='IOGURTE MARACUJÁ 900G', venda__data__month=hoje.month, venda__data__year=hoje.year)
    ma450 = ItemVenda.objects.filter(produto__nome='IOGURTE MARACUJÁ 450G', venda__data__month=hoje.month, venda__data__year=hoje.year)

    print(m900, m450)
    print(n900, n450)
    print(ma900, ma450)

    return HttpResponse()

def recibo(request, pk):

    venda = Venda.objects.get(id=pk)
    items = ItemVenda.objects.filter(venda=pk)
    hoje = datetime.today()

    response = HttpResponse()
    response['content_type'] = 'application/pdf; charset=utf-8'
    response['Content-Disposition'] = f'attachment; filename=RECIBO {venda.cliente} {venda.get_data}.pdf'

    rel = Recibo('templates/static/RECIBO.pdf', venda, items)
    rel.gerar()
    rel.salvar()

    pdf = rel.criar_pdf()
    rel.close()
    response.write(pdf)

    return response


class vendasDetalhes(LoginRequiredMixin, View):
    
    def get(self, request, pk):

        context = {
            "venda" : Venda.objects.get(id=pk),
            "itemsVenda": ItemVenda.objects.filter(venda=pk),
        }

        context['venda'].data = context['venda'].data.strftime("%Y-%m-%d")
        context['venda'].vencimento = context['venda'].vencimento.strftime("%Y-%m-%d")

        return render(request, 'vendas/vendas-detalhes.html', context)

    def post(self, request, pk):

        context = {
            "venda" : Venda.objects.get(id=pk),
            "itemsVenda": ItemVenda.objects.filter(venda=pk),
        }

        context['venda'].status = request.POST.get('status')
        context['venda'].n_nota = request.POST.get('n_nota')
        context['venda'].save()

        messages.success(request, "Alteração salva com sucesso.")

        return redirect(f"/producao/vendas/{pk}")