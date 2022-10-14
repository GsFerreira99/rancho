from django.urls import path
from site_publico import views


urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('produtos/', views.Produtos.as_view(), name='produtos'),
    path('produtos/<pk>', views.ProdutoDetalhes.as_view(), name='produto-detalhes'),
]