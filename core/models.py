from django.db import models


class Especialidade(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.nome


class Convenio(models.Model):
    nome = models.CharField(max_length=120, unique=True)
    cnpj = models.CharField(max_length=18, unique=True)
    telefone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class Medico(models.Model):
    nome = models.CharField(max_length=120)
    crm = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)
    especialidades = models.ManyToManyField(
        Especialidade, related_name="medicos", blank=True
    )

    def __str__(self):
        return f"{self.nome} (CRM {self.crm})"


class Paciente(models.Model):
    nome = models.CharField(max_length=120)
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField(blank=True)
    data_nascimento = models.DateField()
    telefone = models.CharField(max_length=20, blank=True)
    convenio = models.ForeignKey(
        Convenio, on_delete=models.SET_NULL, null=True, blank=True, related_name="pacientes"
    )

    def __str__(self):
        return f"{self.nome} - {self.cpf}"


class Atendimento(models.Model):
    class Status(models.TextChoices):
        AGENDADO = "AG", "Agendado"
        CONFIRMADO = "CF", "Confirmado"
        ATENDIDO = "AT", "Atendido"
        CANCELADO = "CA", "Cancelado"

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name="atendimentos")
    medico = models.ForeignKey(Medico, on_delete=models.PROTECT, related_name="atendimentos")
    data_hora = models.DateTimeField()
    motivo = models.CharField(max_length=200, blank=True)
    descricao = models.TextField(blank=True, null=True, help_text="Descrição da consulta")
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.AGENDADO)
    valor = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.paciente} - {self.data_hora:%d/%m/%Y %H:%M}"


class Prescricao(models.Model):
    atendimento = models.ForeignKey(Atendimento, on_delete=models.CASCADE, related_name="prescricoes")
    texto = models.TextField()
    data = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Prescrição #{self.id} - {self.atendimento.paciente.nome}"


class Exame(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.nome


class SolicitacaoExame(models.Model):
    atendimento = models.ForeignKey(
        Atendimento, on_delete=models.CASCADE, related_name="solicitacoes_exame"
    )
    exame = models.ForeignKey(Exame, on_delete=models.PROTECT, related_name="solicitacoes")
    realizado = models.BooleanField(default=False)
    resultado = models.TextField(blank=True)
    solicitado_em = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.exame.nome} para {self.atendimento.paciente.nome}"
