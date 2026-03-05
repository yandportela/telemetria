from rest_framework import viewsets
from api_telemetria import models
from api_telemetria.api import serializers
from drf_yasg.utils import swagger_auto_schema

class MarcaViewset(viewsets.ModelViewSet):
    serializer_class = serializers.MarcaSerializer
    queryset = models.Marca.objects.all()

    @swagger_auto_schema(
        operation_description="Retorna todas as marcas",
        responses={200: serializers.MarcaSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Cria uma nova marca",
        responses={201: serializers.MarcaSerializer(many=True)}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retorna a marca conforme ID informado",
        responses={200: serializers.MarcaSerializer(many=True)}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Altera a marca conforme dados passados para o ID informado",
        responses={201: serializers.MarcaSerializer(many=True)}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Apaga a marca conforme ID informado",
        responses={201: serializers.MarcaSerializer(many=True)}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class ModeloViewset(viewsets.ModelViewSet):
    serializer_class = serializers.ModeloSerializer
    queryset = models.Modelo.objects.all()

    @swagger_auto_schema(
        operation_description="Retorna todos os modelos",
        responses={200: serializers.ModeloSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Cria um novo modelo",
        responses={201: serializers.ModeloSerializer(many=True)}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retorna o modelo conforme ID informado",
        responses={200: serializers.ModeloSerializer(many=True)}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Altera o modelo conforme dados passados para o ID informado",
        responses={201: serializers.ModeloSerializer(many=True)}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Apaga o modelo conforme ID informado",
        responses={201: serializers.ModeloSerializer(many=True)}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class MedicaoViewset(viewsets.ModelViewSet):
    serializer_class = serializers.MedicaoSerializer
    queryset = models.Medicao.objects.all()
    @swagger_auto_schema(
        operation_description="Retorna todas as informações de tipos de medição",
        responses={200: serializers.MedicaoSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    @swagger_auto_schema(
        operation_description="Cria um novo registro de tipo de medição",
        responses={201: serializers.MedicaoSerializer(many=True)}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    @swagger_auto_schema(
        operation_description="Retorna o registro de tipo de medição conforme ID informado",
        responses={200: serializers.MedicaoSerializer(many=True)}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    @swagger_auto_schema(
        operation_description="Altera o tipo de medição confome dados passados, para o ID informado",
        responses={201: serializers.MedicaoSerializer(many=True)}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    @swagger_auto_schema(
        operation_description="Apaga o registro de tipo de medição conforme ID informado",
        responses={201: serializers.MedicaoSerializer(many=True)}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class UnidadeMedidaViewset(viewsets.ModelViewSet):
    serializer_class = serializers.UnidadeMedidaSerializer
    queryset = models.UnidadeMedida.objects.all()

    @swagger_auto_schema(
        operation_description="Retorna todas as unidades de medida",
        responses={200: serializers.UnidadeMedidaSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Cria uma nova unidade de medida",
        responses={201: serializers.UnidadeMedidaSerializer(many=True)}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retorna a unidade de medida conforme ID informado",
        responses={200: serializers.UnidadeMedidaSerializer(many=True)}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Altera a unidade de medida conforme dados passados para o ID informado",
        responses={201: serializers.UnidadeMedidaSerializer(many=True)}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Apaga a unidade de medida conforme ID informado",
        responses={201: serializers.UnidadeMedidaSerializer(many=True)}
    )
    def destroy(self, request, *args, **kwargs):
        from rest_framework.response import Response
        from rest_framework import status
        from django.db.models import ProtectedError

        instance = self.get_object()
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response({'detail': 'Não é possível deletar: existem medições vinculadas a esta Unidade de Medida.'}, status=status.HTTP_400_BAD_REQUEST)

class VeiculoViewset(viewsets.ModelViewSet):
    serializer_class = serializers.VeiculoSerializer
    queryset = models.Veiculo.objects.all()

    @swagger_auto_schema(
        operation_description="Retorna todos os veículos",
        responses={200: serializers.VeiculoSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Cria um novo veículo",
        responses={201: serializers.VeiculoSerializer(many=True)}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retorna o veículo conforme ID informado",
        responses={200: serializers.VeiculoSerializer(many=True)}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Altera o veículo conforme dados passados para o ID informado",
        responses={201: serializers.VeiculoSerializer(many=True)}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Apaga o veículo conforme ID informado",
        responses={201: serializers.VeiculoSerializer(many=True)}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class MedicaoVeiculoViewset(viewsets.ModelViewSet):
    serializer_class = serializers.MedicaoVeiculoSerializer
    queryset = models.MedicaoVeiculo.objects.all()

    @swagger_auto_schema(
        operation_description="Retorna todas as medições de veículo",
        responses={200: serializers.MedicaoVeiculoSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Cria uma nova medição de veículo",
        responses={201: serializers.MedicaoVeiculoSerializer(many=True)}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retorna a medição de veículo conforme ID informado",
        responses={200: serializers.MedicaoVeiculoSerializer(many=True)}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Altera a medição de veículo conforme dados passados para o ID informado",
        responses={201: serializers.MedicaoVeiculoSerializer(many=True)}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Apaga a medição de veículo conforme ID informado",
        responses={201: serializers.MedicaoVeiculoSerializer(many=True)}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)