from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator


# Create your models here.

class Marca(models.Model):
    nome = models.CharField(max_length=30)
    
    def __str__(self):
        return self.nome


class Modelo(models.Model):
    nome = models.CharField(max_length=30)

    def __str__(self):
        return self.nome

class Veiculo(models.Model):
    
    descricao = models.CharField(max_length=100)
    marca = models.ForeignKey(Marca, on_delete=models.DO_NOTHING)
    modelo = models.ForeignKey(Modelo, on_delete=models.DO_NOTHING)
    ano = models.IntegerField( 
        validators=[ 
            MinValueValidator(1000),
        ] 
    )
    def __str__(self):
        return self.descricao
    horimetro = models.PositiveBigIntegerField()

class UnidadeMedida(models.Model):
    nome = models.CharField(max_length=30)
    def __str__(self):
        return self.nome

class Medicao(models.Model):
    tipo = models.CharField(max_length=45)
    def __str__(self):
        return self.tipo
    unidadeMedida = models.ForeignKey(UnidadeMedida, on_delete=models.PROTECT)

class MedicaoVeiculo(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.DO_NOTHING)
    medicao = models.ForeignKey(Medicao, on_delete=models.DO_NOTHING)
    data = models.DateTimeField()
    valor = models.DecimalField(decimal_places=2, max_digits=6)