from django.shortcuts import render
from django.views import View
from .models import Produto


class Index(View):

    def get(self, request):
        return render(request, 'index.html')


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


class ProdutoDetalhes(View):
    def get(self, request, pk, linha):
        dados = {
            'linha' : linha,
            'produto': Produto.objects.get(id=pk)
        }

        return render(request, 'produto-detalhes.html', dados)
