from django.shortcuts import render
from django.views import View


# Create your views here.
class Index(View):

    def get(self, request):
        return render(request, 'index.html')


class Produtos(View):

    def get(self, request):
        return render(request, 'produtos.html')


class ProdutoDetalhes(View):

    def get(self, request, pk):
        return render(request, 'produto-detalhes.html')