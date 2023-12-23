from typing import Any
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone

#Validators
cpf_validator = RegexValidator(
    regex=r'^(\d{3}\.\d{3}\.\d{3}-\d{2}|\d{11})$',
    message='Formato de CPF inválido'
)


# Create your models here.
class Page(models.Model):
    title = models.CharField(max_length=100, verbose_name='Título')
    domain = models.URLField(max_length=200, blank=True)
    flag_active = models.BooleanField(default=True, verbose_name='Ativo')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    def __str__(self):
        if self.domain:
            return f'{self.title} - {self.domain}'
        else:
            return f'{self.title}'



class Link(models.Model):
    title = models.CharField(max_length=80, verbose_name='Título')
    url = models.URLField(max_length=200, verbose_name='URL')
    click_count = models.IntegerField(default=0, verbose_name='Nº de Clicks')
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='links', verbose_name='Página')
    flag_active = models.BooleanField(default=True, verbose_name='Ativo')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    def __str__(self):
        return f'{self.title} - Página: {self.url}' 
    
    def __init__(self, title, url, page):
        self.title = title
        self.url = url
        self.page = page


    def incrementClick(self):
        self.click_count += 1
        self.save()

    def getClickCount(self):
        return self.click_count



class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nome')
    user = models.OneToOneField(User, on_delete=models.PROTECT, blank=True, verbose_name='Usuário')
    cpf = models.CharField(max_length=14, unique=True, validators=[cpf_validator], blank=True, verbose_name='CPF')
    phone = models.CharField(max_length=15, null=True, verbose_name='Telefone')
    pages = models.ManyToManyField(Page, through='Contract', verbose_name='Páginas')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    def __str__(self):
        if self.cpf:
            return f'{self.name} - {self.cpf}'
        else:
            return f'{self.name}'
        
    def __init__(self, name, user='', cpf=''):
        self.name = name
        self.user = user
        self.cpf = cpf

class Contract(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='contracts', verbose_name='Cliente')
    page = models.ForeignKey(Page, on_delete=models.PROTECT, verbose_name='Página')
    start_date = models.DateField(verbose_name='Data Inicial')
    duration = models.IntegerField(verbose_name='Dias de Duração')
    flag_active = models.BooleanField(default=True, verbose_name='Ativo')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    def __str__(self):
        return f'{self.pk} - Cliente {self.client.name} - Página: {self.page.title}' 
    
    def __init__(self, client, page, start_date, duration):
        self.client = client
        self.page = page
        self.start_date = start_date
        self.duration = duration


