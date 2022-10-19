from django.shortcuts import render
from django.views import View
from .models import Produto
from .models import Linha as LinhaModel


class Index(View):

    def get(self, request):
        dados = {
            'linhas': LinhaModel.objects.all()
        }
        return render(request, 'index.html', dados)


class Produtos(View):

    def get(self, request):
        dados = {
            'titulo': 'Produtos',
            'produtos': Produto.objects.all()
        }
        return render(request, 'produtos.html', context=dados)


class Linha(View):

    def get(self, request, linha):
        produtos = Produto.objects.filter(linha__nome=linha)
        dados = {
            'titulo': linha,
            'produtos': produtos,
        }
        return render(request, 'produtos.html', context=dados)


class SobreNos(View):

    def get(self, request):
        dados = {
        }
        return render(request, 'sobre-nos.html', context=dados)


class Contato(View):

    def get(self, request):
        dados = {
        }
        return render(request, 'contato.html', context=dados)

    def post(self, request):
        dados = {
        }
        return render(request, 'contato.html', context=dados)


class ProdutoDetalhes(View):

    def get(self, request, pk, linha):
        dados = {
            'linha' : linha,
            'produto': Produto.objects.get(id=pk)
        }

        return render(request, 'produto-detalhes.html', dados)
