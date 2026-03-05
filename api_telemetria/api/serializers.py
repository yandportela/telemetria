from rest_framework import serializers
from api_telemetria import models

class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Marca
        fields = "__all__"
        extra_kwargs = {
            'id': {'help_text': 'Identificador da marca'},
            'nome': {'help_text': 'Nome da marca'},
        }

class ModeloSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Modelo
        fields = "__all__"
        extra_kwargs = {
            'id': {'help_text': 'Identificador do modelo'},
            'nome': {'help_text': 'Nome do modelo'},
        }

class VeiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Veiculo
        fields = "__all__"
        extra_kwargs = {
            'id': {'help_text': 'Identificador do veículo'},
            'descricao': {'help_text': 'Descrição do veículo'},
            'marca': {'help_text': 'Identificador da marca. Use GET da API marca'},
            'modelo': {'help_text': 'Identificador do modelo. Use GET da API modelo'},
            'ano': {'help_text': 'Ano de fabricação do veículo'},
            'horimetro': {'help_text': 'Horímetro atual do veículo'},
        }

class MedicaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Medicao
        fields = "__all__"
        extra_kwargs = {
            'id': {'help_text': 'Identificador da medição'},
            'tipo': {'help_text': 'Tipo da medição'},
            'unidadeMedida': {'help_text': 'Identificador da unidade de medida. Use GET da API unidadeMedida'},
        }

class UnidadeMedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UnidadeMedida
        fields = "__all__"
        extra_kwargs = {
            'id': {'help_text': 'Identificador da unidade de medida'},
            'nome': {'help_text': 'Nome da unidade de medida'},
        }

class MedicaoVeiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MedicaoVeiculo
        fields = "__all__"
        extra_kwargs = {
            'id': {'help_text': 'Identificador da medição do veículo'},
            'veiculo': {'help_text': 'Identificador do veículo. Buscar no Get da API veiculo'},
            'medicao': {'help_text': 'Identificador da medição. Buscar no Get da API medicao'},
            'data': {'help_text': 'Data e hora da medição, essa informação deve vir da automação'},
            'valor': {'help_text': 'Valor medido na automação.'},
            }