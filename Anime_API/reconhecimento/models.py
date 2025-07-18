from django.db import models


class Previsao(models.Model):
    imagem = models.ImageField(upload_to='image_anime')
    nome_personagem = models.CharField(max_length=100)
    anime = models.CharField(max_length=100)
    data_criacao = models.DateField(auto_now_add=True)
    probabilidade = models.FloatField(null=True, blank=True) 
    def __str__(self):
        return f"{self.nome_personagem} - {self.anime}"