from django.db import models


class Tabela(models.Model):
    nome = models.CharField(max_length=255)
    val_ener = models.CharField(max_length=255)
    val_ener_vd = models.CharField(max_length=255)

    val_carbo = models.CharField(max_length=255)
    val_carbo_vd = models.CharField(max_length=255)

    val_prote = models.CharField(max_length=255)
    val_prote_vd = models.CharField(max_length=255)

    val_gtotal = models.CharField(max_length=255)
    val_gtotal_vd = models.CharField(max_length=255)

    val_gsatu = models.CharField(max_length=255)
    val_gsatu_vd = models.CharField(max_length=255)

    val_gtrans = models.CharField(max_length=255)
    val_gtrans_vd = models.CharField(max_length=255)

    val_fibra = models.CharField(max_length=255)
    val_fibra_vd = models.CharField(max_length=255)

    val_sodio = models.CharField(max_length=255)
    val_sodio_vd = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.nome


class Linha(models.Model):
    nome = models.CharField(max_length=255)
    imagem = models.ImageField(null=True)

    def __str__(self) -> str:
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=255)
    imagem = models.ImageField(null=True)
    ingredientes = models.TextField()
    tabela_nutricional = models
    validade = models.TextField()
    linha = models.ForeignKey(Linha, on_delete=models.CASCADE, null=True)
    tabela = models.ForeignKey(Tabela, on_delete=models.DO_NOTHING, null=True)
    ativo = models.BooleanField()

    def p_nome(self) -> str:
        nome = self.nome.split(' ')
        nome.pop(-1)
        return ''.join(nome)

    def s_nome(self) -> str:
        nome = self.nome.split(' ')
        return nome[-1]

    def __str__(self) -> str:
        return self.nome
