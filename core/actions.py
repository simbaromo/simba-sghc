import csv
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

from sghc import settings


def download_csv(modeladmin, request, queryset):

    if not request.user.is_staff:
        raise PermissionDenied
    opts = queryset.model._meta
    model = queryset.model
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename=export.csv'
    writer = csv.writer(response)
    field_names = [field.name for field in opts.fields]
    extra_field_names = ['unidad', 'medicamentos_nacionales', 'fechas', 'comorbilidad',
                                 'estudio_radiologico', 'vacuna', 'reactantes', 'sensibilidad_medicamentosa',
                                 'registro_transfusion', ]
    writer.writerow(field_names + extra_field_names)
    for obj in queryset:
        row = [getattr(obj, field) for field in field_names]
        row = row + [obj.unidad]
        medicamentos = ""
        for item in obj.medicamentos_nacionales.all():
            medicamentos = medicamentos + item.nombre + ','
        row = row + [medicamentos]
        notas = ""
        for item in obj.fechas.all():
            notas = notas + item.get_tipo_display() + '-' + str(item.fecha) + '-' + item.notas + ','
        row = row + [notas]
        comorbilidades = ""
        for item in obj.comorbilidades.all():
            comorbilidades = comorbilidades + item.comorbilidad + ','
        row = row + [comorbilidades]
        estudios_radiologicos = ""
        for item in obj.estudios_radiologicos.all():
            estudios_radiologicos = estudios_radiologicos + item.get_tipo_display() + '-' + str(settings.BASE_DIR) + '\media{}'.format(item.imagen) + '-' + str(item.fecha) + ','
        row = row + [estudios_radiologicos]
        vacunas = ""
        for item in obj.vacunas.all():
            vacunas = vacunas + str(item.tipo) + '-' + str(
                item.dosis) + '-' + str(item.fecha) + ','
        row = row + [vacunas]
        reactantes = ""
        for item in obj.reactantes.all():
            reactantes = reactantes + str(item.proteinascr) + '-' + str(
                item.leucocitos_neutrofilo) + '-' + str(item.ferritina) + ','
        row = row + [reactantes]
        sensibilidadmedicamentosa_set = ""
        for item in obj.reacciones.all():
            sensibilidadmedicamentosa_set = sensibilidadmedicamentosa_set + str(item.medicamento) + '-' + str(
                item.reccion) + '-' + str(item.fecha) + ','
        row = row + [sensibilidadmedicamentosa_set]
        registrotransfusion_set = ""
        for item in obj.registrotransfusion_set.all():
            registrotransfusion_set = registrotransfusion_set + str(item.fecha) + '-' + str(
                item.preparado) + '-' + str(item.numero) + '-' + str(item.volumen) + '-' + str(item.paciente)\
                                      + '-' + str(item.frasco) + '-' + str(item.tecnico)+ ','
        row = row + [registrotransfusion_set]
        writer.writerow(row)
    return response
download_csv.short_description = "Exportar a CSV"