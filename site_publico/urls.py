from django.urls import path
from site_publico import views


urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('contato/', views.Contato.as_view(), name='contato'),
    path('sobre-nos/', views.SobreNos.as_view(), name='sobre-nos'),
    path('produtos/', views.Produtos.as_view(), name='produtos'),
    path('produtos/<linha>', views.Linha.as_view(), name='linha'),
    path('produtos/<linha>/<pk>', views.ProdutoDetalhes.as_view(), name='produto-detalhes'),
]