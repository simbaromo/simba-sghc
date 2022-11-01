from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field

from .actions import download_csv
from .models import *

#inlines
class SensibilidadMedicamentosaInLine(admin.TabularInline):
    model = SensibilidadMedicamentosa
    extra = 0

class TACInLine(admin.TabularInline):
    model = TAC
    extra = 0

class MedicamentosNacionalesInLine(admin.StackedInline):
    model = MedicamentosNacionales
    extra = 0

class FechaInline(admin.StackedInline):
    model = Fecha
    extra = 0

class ComorbilidadInLine(admin.StackedInline):
    model = Comorbilidad
    extra = 0

class EstudioRadiologicoInLine(admin.StackedInline):
    model = EstudioRadiologico
    extra = 0

class VacunaInLine(admin.StackedInline):
    model = Vacuna
    extra = 0

class ReactantesFaseAguda(admin.StackedInline):
    model = ReactantesFaseAguda
    extra = 0

class RegistroTransfusionInLine(admin.StackedInline):
    model = RegistroTransfusion
    extra = 0
    fieldsets = (
        ('', {
            # 'classes': ('collapse',),
            'fields': (('fecha',), ('tecnico', 'preparado'),('numero', 'volumen'), ('paciente', 'frasco'))
        }),
    )

class HistoriaEnfermedadInLine(admin.StackedInline):
    model = HistoriaEnfermedad
    extra = 0
    fieldsets = (
        ('', {
            # 'classes': ('collapse',),
            'fields': ('motivo', 'historia',)
        }),
        ('Antecedentes patológicos, familiares y personales', {
            'classes': ('collapse',),
            'fields': (('asma_bronquial_texto', 'asma_bronquial_personal', 'asma_bronquial_padre', 'asma_bronquial_madre',
                        'asma_bronquial_hijo', 'asma_bronquial_otro'),
                       ('cardiopatia_isquemica_texto', 'cardiopatia_isquemica_personal', 'cardiopatia_isquemica_padre',
                        'cardiopatia_isquemica_madre', 'cardiopatia_isquemica_hijo', 'cardiopatia_isquemica_otro'),
                       ('hipertension_arterial_texto', 'hipertension_arterial_personal', 'hipertension_arterial_padre',
                        'hipertension_arterial_madre', 'hipertension_arterial_hijo', 'hipertension_arterial_otro'),
                       ('enfermedad_cerebro_vascular_texto', 'enfermedad_cerebro_vascular_personal', 'enfermedad_cerebro_vascular_padre',
                        'enfermedad_cerebro_vascular_madre', 'enfermedad_cerebro_vascular_hijo', 'enfermedad_cerebro_vascular_otro'),
                       ('epilepsia_texto', 'epilepsia_personal', 'epilepsia_padre', 'epilepsia_madre', 'epilepsia_hijo',
                        'epilepsia_otro'),
                       ('diabetes_mellitus_texto', 'diabetes_mellitus_personal', 'diabetes_mellitus_padre', 'diabetes_mellitus_madre',
                        'diabetes_mellitus_hijo', 'diabetes_mellitus_otro'),
                       ('hepatitis_viral_texto', 'hepatitis_viral_personal', 'hepatitis_viral_padre',
                        'hepatitis_viral_madre', 'hepatitis_viral_hijo', 'hepatitis_viral_otro'),
                       ('dengue_texto', 'dengue_personal', 'dengue_padre', 'dengue_madre', 'dengue_hijo',
                        'dengue_otro'),
                       ('sifilis_texto', 'sifilis_personal', 'sifilis_padre', 'sifilis_madre', 'sifilis_hijo',
                        'sifilis_otro'),
                       ('blenorragia_texto', 'blenorragia_personal', 'blenorragia_padre', 'blenorragia_madre', 'blenorragia_hijo',
                        'blenorragia_otro'),
                       ('tuberculosis_texto', 'tuberculosis_personal', 'tuberculosis_padre', 'tuberculosis_madre',
                        'tuberculosis_hijo', 'tuberculosis_otro'),
                       ('cancer_texto', 'cancer_personal', 'cancer_padre', 'cancer_madre',
                        'cancer_hijo', 'cancer_otro'),
                       ('otras_texto', 'otras_personal', 'otras_padre', 'otras_madre',
                        'otras_hijo', 'otras_otro'),
                       )}),
        ('Intervenciones quirúrgicas', {
            # 'classes': ('collapse',),
            'fields': (('tipo_operacion', 'secuelas','fecha'), )
        }),
    )

class AspectosPSIInLine(admin.StackedInline):
    model = AspectosPSI
    extra = 0

#model admins
class HistoriaClinicaAdmin(admin.ModelAdmin):
    list_display = ('ci', 'apellido1', 'apellido2', 'nombres', 'unidad')
    list_display_links = ('ci', 'apellido1', 'apellido2', 'nombres')
    list_filter = ('unidad','fecha')
    list_per_page = 10
    search_fields = ['id', 'apellido1', 'apellido2', 'nombres', 'ci']
    fieldsets = (
        ('', {
            # 'classes': ('collapse',),
            'fields': (('id', 'ci',),'nombres', 'genero',('apellido1', 'apellido2'),'fecha', 'unidad')
        }),
    )
    actions = [download_csv,]
    inlines = [SensibilidadMedicamentosaInLine, RegistroTransfusionInLine, AspectosPSIInLine,
               HistoriaEnfermedadInLine, TACInLine, MedicamentosNacionalesInLine, FechaInline,
               ComorbilidadInLine, EstudioRadiologicoInLine, VacunaInLine, ReactantesFaseAguda]






#admin site register
admin.site.register(HistoriaClinica, HistoriaClinicaAdmin)
admin.site.register(Unidad)
admin.site.register(Medicamento)
admin.site.register(Reaccion)
admin.site.register(TAC)
admin.site.register(TipoVacuna)





