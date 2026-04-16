import csv
import os
import uuid
from decimal import Decimal
from datetime import datetime

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import transaction

from api_telemetria.models import MedicaoVeiculo, Veiculo, Medicao





def processar_csv_medicoes(arquivo):
    # Gera um ID único para esta importação, evitando conflito de nomes de arquivos
    arquivoid = str(uuid.uuid4())

    # Define a pasta onde o CSV será salvo fisicamente e a cria se não existir
    pasta_destino = os.path.join(settings.MEDIA_ROOT, "importacoes_medicao")
    os.makedirs(pasta_destino, exist_ok=True)

    # Salva o arquivo no disco com o UUID prefixado para garantir um nome único
    nome_salvo = f"{arquivoid}_{arquivo.name}"
    fs = FileSystemStorage(location=pasta_destino)
    nome_arquivo_salvo = fs.save(nome_salvo, arquivo)
    caminho_completo = os.path.join(pasta_destino, nome_arquivo_salvo)

    # Variáveis de controle para o relatório final
    total_linhas_arquivo = 0
    erros = []
    linhas_para_inserir = []

    # OTIMIZAÇÃO: Busca todos os veículos e medições de uma vez e guarda na memória (cache).
    # Isso evita fazer uma consulta ao banco de dados para CADA linha do CSV,
    # o que deixaria a importação extremamente lenta.
    veiculos_cache = {v.id: v for v in Veiculo.objects.all()}
    medicoes_cache = {m.id: m for m in Medicao.objects.all()}

    # Abre o arquivo. 'utf-8-sig' remove caracteres invisíveis do início do arquivo (BOM)
    with open(caminho_completo, mode="r", encoding="utf-8-sig", newline="") as f:
        # Lê o CSV considerando que as colunas são separadas por ponto e vírgula
        reader = csv.DictReader(f, delimiter=';')

        # Define os nomes exatos das colunas que esperamos encontrar no arquivo
        campos_esperados = {"veiculo", "medicao", "data", "valor"}

        # Valida se o arquivo tem algum cabeçalho
        if not reader.fieldnames:
            raise Exception("O CSV não possui cabeçalho.")

        # Valida se todas as colunas esperadas estão presentes no arquivo
        if not campos_esperados.issubset(set(reader.fieldnames)):
            raise Exception(
                f"Cabeçalho inválido. Esperado: {list(campos_esperados)}. Recebido: {reader.fieldnames}"
            )

        # Percorre cada linha do CSV (começando da linha 2, já que a 1 é o cabeçalho)
        for numero_linha, row in enumerate(reader, start=2):
            total_linhas_arquivo += 1

            try:
                # Extrai os IDs do CSV e converte para número inteiro
                id_veiculo = int(row["veiculo"])
                id_medicao = int(row["medicao"])

                # Busca os objetos reais usando os dicionários em memória criados lá em cima
                veiculo = veiculos_cache.get(id_veiculo)
                if not veiculo:
                    raise Exception(f"Veículo {id_veiculo} não encontrado.")

                medicao = medicoes_cache.get(id_medicao)
                if not medicao:
                    raise Exception(f"Medição {id_medicao} não encontrada.")

                # Converte o texto da data do CSV para um objeto datetime do Python
                data_convertida = datetime.strptime(
                    row["data"].strip(),
                    "%Y-%m-%d %H:%M:%S"
                )

                # Converte o valor para Decimal (melhor formato para valores exatos em Python/Banco)
                valor_convertido = Decimal(row["valor"].strip())

                # Cria a inst�ncia do modelo final em mem�ria (ainda N�O salva no banco)
                linhas_para_inserir.append(
                    MedicaoVeiculo(
                        veiculo_id=veiculo.id,
                        medicao_id=medicao.id,
                        data=data_convertida,
                        valor=valor_convertido,
                    )
                )

            except Exception as e:
                # Se der erro nesta linha específica, não para o processo. 
                # Apenas anota a linha e o erro para retornar ao usuário depois.
                erros.append({
                    "linha": numero_linha,
                    "erro": str(e)
                })
                
    total_linhas_validas = len(linhas_para_inserir)

    # transaction.atomic() garante que tudo dentro deste bloco seja salvo de uma vez.
    # Se der qualquer erro no meio, ele desfaz (rollback) e não salva nada pela metade.
    with transaction.atomic():
        if linhas_para_inserir:
            # bulk_create insere os dados em "pacotes" de 1000 linhas por vez no banco.
            # É mais rápido do que dar um .save() para cada linha.
            MedicaoVeiculo.objects.bulk_create(linhas_para_inserir, batch_size=1000)

        total_linhas_importadas = len(linhas_para_inserir)
        quantidades_conferem = total_linhas_validas == total_linhas_importadas

        # Se salvou no banco exatamente a mesma quantidade que validamos em memória...

    # Retorna um dicionário (que costuma virar um JSON na view) com o resumo da operação
    return {
        "arquivoid": arquivoid,
        "arquivo_salvo": nome_arquivo_salvo,
        "caminho": caminho_completo,
        "total_linhas_arquivo": total_linhas_arquivo,
        "total_linhas_importadas": total_linhas_importadas,
        "quantidades_conferem": total_linhas_arquivo == total_linhas_importadas,
        "erros": erros
    }
