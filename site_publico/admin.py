from django.contrib import admin
from .models import Linha, Tabela, Produto


class LinhaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome',)
    list_filter = ['nome']
    search_fields = (
        "nome",
    )


class TabelaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome',)
    list_filter = ['nome']
    search_fields = (
        "nome",
    )


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'linha', 'tabela', 'ativo',)
    list_filter = ['nome', 'linha', 'tabela', 'ativo']
    search_fields = ('nome', 'linha', 'tabela', 'ativo',)
    list_editable = ('ativo',)


admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Linha, LinhaAdmin)
admin.site.register(Tabela, TabelaAdmin)