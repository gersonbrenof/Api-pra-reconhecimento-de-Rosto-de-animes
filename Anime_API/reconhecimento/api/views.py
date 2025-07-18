import os
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

from rest_framework import viewsets, status
from rest_framework.response import Response

from reconhecimento.models import Previsao
from reconhecimento.api.serializers import PrevisaoSerializer, ImagemSerializer

# Carrega o modelo treinado apenas uma vez
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMINHO_MODELO = os.path.join(BASE_DIR, 'modelo_melhor.h5')
modelo = load_model(CAMINHO_MODELO)

# Lista de classes, na ordem do treino
classes = [
    {'nome': 'Anna Yamada', 'anime': 'Boku no Kokoro no Yabai Yatsu'},
    {'nome': 'Asuna', 'anime': 'Sword Art Online'},
    {'nome': 'Gojo Satoru', 'anime': 'Jujutsu Kaisen'},
    {'nome': 'Ichika Nakano', 'anime': 'The Quintuplets'},
    {'nome': 'Itsuki Nakano', 'anime': 'The Quintuplets'},
    {'nome': 'Izumi Miyamura', 'anime': 'Horimiya'},
    {'nome': 'Kirito', 'anime': 'Sword Art Online'},
    {'nome': 'Kyoko Hori', 'anime': 'Horimiya'},
    {'nome': 'Levi Ackerman', 'anime': 'Attack on Titan'},
    {'nome': 'Miku Nakano', 'anime': 'The Quintuplets'},
    {'nome': 'Monkey D. Luffy', 'anime': 'One Piece'},
    {'nome': 'Nami', 'anime': 'One Piece'},
    {'nome': 'Naruto Uzumaki', 'anime': 'Naruto'},
    {'nome': 'Nino Nakano', 'anime': 'The Quintuplets'},
    {'nome': 'Noelle Silva', 'anime': 'Black Clover'},
    {'nome': 'Roronoa Zoro', 'anime': 'One Piece'},
    {'nome': 'Yano Tsukasa', 'anime': 'The Quintuplets'},
    {'nome': 'Yotsuba Nakano', 'anime': 'The Quintuplets'},
]

class PrevisaoViewSet(viewsets.ModelViewSet):
    queryset = Previsao.objects.all().order_by('-data_criacao')
    serializer_class = PrevisaoSerializer

    def create(self, request, *args, **kwargs):
        serializer = ImagemSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        imagem = serializer.validated_data['imagem']
        previsao = Previsao(imagem=imagem)

        try:
            # Pré-processamento da imagem
            img = Image.open(imagem).convert('RGB')
            img = img.resize((64, 64))
            img = img_to_array(img) / 255.0
            img = np.expand_dims(img, axis=0)

            # Predição
            pred = modelo.predict(img)
            index = np.argmax(pred)
            probabilidade = float(pred[0][index])

            personagem = classes[index]

            # Salva a previsão com probabilidade
            previsao.nome_personagem = personagem['nome']
            previsao.anime = personagem['anime']
            previsao.probabilidade = round(probabilidade * 100, 2)  # salva como porcentagem
            previsao.save()

            # Serializa resposta
            return Response(PrevisaoSerializer(previsao).data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'erro': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        previsao = self.get_object()
        previsao.delete()
        return Response({'mensagem': 'Previsão excluída com sucesso.'}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
