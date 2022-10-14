from django.urls import path
from site_publico import views


urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('produtos/', views.Produtos.as_view(), name='produtos'),
    path('produtos/<linha>', views.Linha.as_view(), name='linha'),
    path('produtos/<linha>/<pk>', views.ProdutoDetalhes.as_view(), name='produto-detalhes'),
]