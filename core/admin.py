from django.contrib import admin
from .models import (
    Especialidade, Convenio, Medico, Paciente,
    Atendimento, Prescricao, Exame, SolicitacaoExame
)


# Inline para prescrições
class PrescricaoInline(admin.TabularInline):
    model = Prescricao
    extra = 1
    fields = ("texto", "data")
    readonly_fields = ("data",)


# Inline para solicitações de exames
class SolicitacaoExameInline(admin.TabularInline):
    model = SolicitacaoExame
    extra = 1
    fields = ("exame", "realizado", "resultado", "solicitado_em")
    readonly_fields = ("solicitado_em",)


@admin.register(Atendimento)
class AtendimentoAdmin(admin.ModelAdmin):
    list_display = ("id", "data_hora", "paciente", "medico", "status", "valor")
    list_filter = ("status", "medico", "data_hora")
    search_fields = ("paciente__nome", "medico__nome")
    date_hierarchy = "data_hora"
    ordering = ("-data_hora",)
    inlines = [PrescricaoInline, SolicitacaoExameInline]

    fields = (
        "paciente", "medico", "data_hora", "motivo",
        "descricao", "status", "valor"
    )


@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ("nome", "crm", "email")
    list_filter = ("especialidades",)
    search_fields = ("nome", "crm", "email")
    filter_horizontal = ("especialidades",)


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ("nome", "cpf", "convenio", "data_nascimento", "telefone")
    list_filter = ("convenio",)
    search_fields = ("nome", "cpf", "email", "telefone")


@admin.register(Convenio)
class ConvenioAdmin(admin.ModelAdmin):
    list_display = ("nome", "cnpj", "ativo", "telefone", "email")
    list_filter = ("ativo",)
    search_fields = ("nome", "cnpj")


@admin.register(Especialidade)
class EspecialidadeAdmin(admin.ModelAdmin):
    list_display = ("nome",)
    search_fields = ("nome",)


@admin.register(Prescricao)
class PrescricaoAdmin(admin.ModelAdmin):
    list_display = ("atendimento", "data")
    list_filter = ("data",)
    search_fields = ("atendimento__paciente__nome", "atendimento__medico__nome", "texto")


@admin.register(Exame)
class ExameAdmin(admin.ModelAdmin):
    list_display = ("nome",)
    search_fields = ("nome",)


@admin.register(SolicitacaoExame)
class SolicitacaoExameAdmin(admin.ModelAdmin):
    list_display = ("atendimento", "exame", "realizado", "solicitado_em")
    list_filter = ("realizado", "exame", "solicitado_em")
    search_fields = ("atendimento__paciente__nome", "exame__nome")
