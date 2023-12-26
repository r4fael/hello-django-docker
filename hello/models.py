from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone


#Validators
cpf_validator = RegexValidator(
    regex=r'^(\d{3}\.\d{3}\.\d{3}-\d{2}|\d{11})$',
    message='Formato de CPF inválido'
)

phone_validator = RegexValidator(
    regex=r'^(?:(?:\+|00)?(55)\s?)?(?:(?:(?:\()?\d{2}(?:\)?)\s?)?(\d{4,5})[-.\s]?(\d{4}))$',
    message='Formato de Telefone inválido. Ex (22) 99876-9999'
)


# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nome')
    user = models.OneToOneField(User, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Usuário')
    cpf = models.CharField(max_length=14, unique=True, validators=[cpf_validator], blank=True, verbose_name='CPF')
    phone = models.CharField(max_length=14, null=True, blank=True, validators=[phone_validator], verbose_name="Telefone")
    pages = models.ManyToManyField('Page', through='Contract', verbose_name='Páginas')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    def __str__(self):
        if self.cpf:
            return f'{self.name} - {self.cpf}'
        else:
            return f'{self.name}'

class Contract(models.Model):
    client = models.ForeignKey('Client', on_delete=models.PROTECT, related_name='client', verbose_name='Cliente')
    page = models.ForeignKey('Page', on_delete=models.PROTECT, related_name='page', verbose_name='Página')
    start_date = models.DateField(default=timezone.now, verbose_name='Data Inicial')
    duration = models.IntegerField(verbose_name='Dias de Duração')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Valor')
    flag_active = models.BooleanField(default=True, verbose_name='Ativo')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        ordering = ['-flag_active']

    def __str__(self):
        return f'{self.pk} - Cliente: {self.client.name} - Página: {self.page.title}' 

class Page(models.Model):
    title = models.CharField(max_length=100, verbose_name='Título')
    domain = models.URLField(max_length=200, blank=True)
    description = models.CharField(max_length=250)
    keywords = models.CharField(max_length=200)
    clients = models.ManyToManyField('Client', through='Contract', verbose_name='Clientes')
    flag_active = models.BooleanField(default=True, verbose_name='Ativo')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    def __str__(self):
        if self.domain:
            return f'{self.title} - {self.domain}'
        else:
            return f'{self.title}'
    def getLinks(self):
        return self.links.all()  # related_name='links' in class Page
    
    def get_links_display(self):
        return ", ".join(link.title for link in self.links.all())
        

class Link(models.Model):
    title = models.CharField(max_length=80, verbose_name='Título')
    url = models.URLField(max_length=200, verbose_name='URL')
    _click_count = models.IntegerField(default=0, verbose_name='Nº de Clicks')
    page = models.ForeignKey('Page', on_delete=models.CASCADE, related_name='links', verbose_name='Página')
    flag_active = models.BooleanField(default=True, verbose_name='Ativo')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    def __str__(self):
        return f'{self.title} - {self.url} | {self.page.title}'

    def incrementClick(self):
        self._click_count += 1
        self.save()

    def getClickCount(self):
        return self._click_count