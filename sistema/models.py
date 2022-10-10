from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.formats import localize



class User(AbstractUser):
    cpf = models.IntegerField(default=00000000000)

    def get_group(self):
        return self.groups.name

class TipoLeite(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Fornecedor(models.Model):
    nome = models.CharField(max_length=30)
    leite = models.ForeignKey(TipoLeite, on_delete=models.DO_NOTHING, default=1, blank=True)
    preco_leite = models.FloatField(default=0)

    def __str__(self):
        return self.nome
    @property
    def preco(self):
        return self.preco_leite

class RecebimentoLeite(models.Model):
    data = models.DateField()
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.DO_NOTHING)
    quantidade = models.FloatField(default=0)
    valor = models.FloatField(default=0)

    def get_data(self):
        return self.data.strftime('%d/%m/%Y')

class TipoProduto(models.Model):
    nome = models.CharField(max_length=40)

    def __str__(self) -> str:
        return self.nome

class CategoriaProduto(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.nome

class Produto(models.Model):
    tipo = models.ForeignKey(TipoProduto, on_delete=models.DO_NOTHING)
    nome = models.CharField(max_length=40, unique=True)
    categoria = models.ForeignKey(CategoriaProduto, on_delete=models.DO_NOTHING, default=1)
    marca = models.CharField(max_length=25, default=0)
    codBarras = models.CharField(max_length=13, default='0000000000000')
    valorCompra = models.FloatField(default=0)
    valorVenda = models.FloatField(default=0)
    class Meta:
        default_related_name = 'produto'

    def __str__(self) -> str:
        return self.nome

class Producao(models.Model):
    data = models.DateField(blank=False)
    produto = models.ForeignKey(Produto, on_delete=models.DO_NOTHING)
    leite = models.IntegerField(blank=False)
    sal = models.FloatField(default=0, blank=True)
    peso = models.FloatField(default=0, blank=True)
    rendimento = models.FloatField(default=0, blank=True)
    acucar = models.FloatField(default=0, blank=True)
    lote = models.IntegerField(blank=False)
    observacao = models.TextField(blank=True)

    class Meta:
        default_related_name = 'producao'

    def __str__(self) -> str:
        return str(self.lote)

class Estoque(models.Model):
    produto = models.OneToOneField(Produto, on_delete=models.DO_NOTHING)
    quantidade = models.FloatField(default=0)
    unidade = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.produto.nome
        
class Pessoa(models.Model):
    nome = models.CharField(max_length=30)
    endereco = models.CharField(max_length=200, blank=True)
    telefone = models.CharField(max_length=11)
    email = models.EmailField(unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.nome

    @property
    def contato(self):
        if len(self.telefone) == 11:
            return f"({self.telefone[:2]}) {self.telefone[2:7]}-{self.telefone[7:]}"
        elif len(self.telefone) == 10:
            return f"({self.telefone[:2]}) {self.telefone[2:6]}-{self.telefone[6:]}"
        else:
            return self.telefone
class PessoaFisica(Pessoa):
    sobrenome = models.CharField(max_length=50)
    cpf = models.CharField(max_length=11)
    nascimento = models.DateField(blank=True)

    @property
    def credenciais(self):
        return f"{self.cpf[:3]}.{self.cpf[3:6]}.{self.cpf[6:9]}-{self.cpf[9:]}"

class PessoaJuridica(Pessoa):
    razao_social = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=14)
    inscricao_estadual = models.CharField(max_length=20)

    @property
    def credenciais(self):
        return f"{self.cnpj[:2]}.{self.cnpj[2:5]}.{self.cnpj[5:8]}/{self.cnpj[8:12]}-{self.cnpj[12:14]}"


class Cliente(models.Model):
    limite = models.Q(model = 'pessoafisica') | models.Q(model = 'pessoajuridica')
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING, limit_choices_to=limite) 
    object_id = models.PositiveIntegerField() 
    content_object=GenericForeignKey('content_type', 'object_id')

    def __str__(self) -> str:
        return self.content_object.nome

class Venda(models.Model):
    data = models.DateField()
    cliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING)
    n_nota = models.CharField(max_length=30, default=0)
    total = models.FloatField()
    faturamento = models.CharField(max_length=25)
    vencimento = models.DateField()
    status = models.CharField(max_length=20, default='Em Aberto')

    @property
    def get_data(self):
        return self.data.strftime('%d/%m/%Y')

    @property
    def get_total(self) -> str:
        return f"R$ {localize(self.total)}"

    @property
    def get_vencimento(self):
        return self.vencimento.strftime('%d/%m/%Y')

    def __str__(self) -> str:
        return str(self.id)

class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.DO_NOTHING, default=1)
    unidade = models.CharField(max_length=20, default='KG')
    produto = models.ForeignKey(Produto, on_delete=models.DO_NOTHING, blank=False)
    valor = models.FloatField(default=0)
    quantidade = models.FloatField(blank=False)
    total = models.FloatField(default=0)

    @property
    def get_valor(self) -> str:
        return f"R$ {localize(self.valor)}"

    @property
    def get_total(self) -> str:
        return f"R$ {localize(self.total)}"

    def __str__(self) -> str:
        return f"{self.quantidade} {self.unidade} de {self.produto}"

class EmbalagemProducaoQueijo(models.Model):
    nome = models.ForeignKey(Produto, on_delete=models.CASCADE, default=1)
    embalagem = models.ForeignKey(Estoque, on_delete=models.CASCADE, default=1, related_name='embalagem')
    rotulo = models.ForeignKey(Estoque, on_delete=models.CASCADE, default=1, related_name='rotulo')
    quantidade = models.IntegerField(default=1)


