from rest_framework import viewsets
from api_telemetria import models
from api_telemetria.api import serializers

class MarcaViewset(viewsets.ModelViewSet):
    serializer_class = serializers.MarcaSerializer
    queryset = models.Marca.objects.all()

class ModeloViewset(viewsets.ModelViewSet):
    serializer_class = serializers.ModeloSerializer
    queryset = models.Modelo.objects.all()

class MedicaoViewset(viewsets.ModelViewSet):
    serializer_class = serializers.MedicaoSerializer
    queryset = models.Medicao.objects.all()

class UnidadeMedidaViewset(viewsets.ModelViewSet):
    serializer_class = serializers.UnidadeMedidaSerializer
    queryset = models.UnidadeMedida.objects.all()

class VeiculoViewset(viewsets.ModelViewSet):
    serializer_class = serializers.VeiculoSerializer
    queryset = models.Veiculo.objects.all()

class MedicaoVeiculoViewset(viewsets.ModelViewSet):
    serializer_class = serializers.MedicaoVeiculoSerializer
    queryset = models.MedicaoVeiculo.objects.all()