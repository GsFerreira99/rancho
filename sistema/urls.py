from django.urls import path, include
from . import views
from site_publico import urls as site_publico


urlpatterns = [
    path('login/', views.login.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('home/', views.home.as_view(), name='home'),
    path('producao/vendas/<int:pk>/recibo', views.recibo, name='recibo'),
    path('producao/vendas/<int:pk>/nfe', views.nfe, name='nfe'),
    path('producao/recebimento-leite', views.recebimento_leite.as_view(), name='recebimento-leite'),
    path('producao/producao-diaria', views.produção_diaria.as_view(), name='producao-diaria'),
    path('producao/estoque', views.estoque.as_view(), name='estoque'),
    path('producao/estoque/<int:pk>/', views.estoqueDetalhes.as_view(), name='estoque-detalhes'),
    path('producao/clientes', views.clientes.as_view(), name='clientes'),
    path('producao/cliente/<int:pk>/', views.clientesDetalhes.as_view(), name='cliente-detalhes'),
    path('producao/vendas', views.vendas.as_view(), name='vendas'),
    path('producao/vendas/<int:pk>/', views.vendasDetalhes.as_view(), name='vendas-detalhes'),
    path('producao/cadastro-produto', views.cadastroProduto.as_view(), name='cadastro-produto'),
] + site_publico.urlpatterns
