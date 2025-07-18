from rest_framework import serializers
from  reconhecimento.models import Previsao

class PrevisaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Previsao
        fields = ['id', 'imagem', 'nome_personagem', 'anime', 'data_criacao','probabilidade']
        read_only_fields = ['nome_personagem', 'anime', 'data_criacao','probabilidade']
        
class ImagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Previsao  # ou outro modelo que contenha o campo imagem
        fields = ['imagem']  # liste os campos que você quer serializar, no mínimo o campo 'imagem'