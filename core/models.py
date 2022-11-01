import datetime
import hashlib
import os

import pydicom
from django.core.validators import RegexValidator
from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
from sghc.settings import BASE_DIR, MEDIA_ROOT


class Medicamento(models.Model):
    medicamento = models.CharField(max_length=255)

    def __str__(self):
        return self.medicamento

    class Meta:
        verbose_name = 'Medicamento, sangre y derivados'
        verbose_name_plural = '03 - Medicamentos, sangre y derivados'


class Reaccion(models.Model):
    reaccion = models.CharField(max_length=255)

    def __str__(self):
        return self.reaccion

    class Meta:
        verbose_name = 'Reacción'
        verbose_name_plural = '04 - Reacciones'



class Unidad(models.Model):
    unidad = models.CharField(max_length=255)

    def __str__(self):
        return self.unidad

    class Meta:
        verbose_name = 'Unidad'
        verbose_name_plural = '02 - Unidades'

class HistoriaClinica(models.Model):
    GENERO_CHOICES = (
        ('m','Masculino'),
        ('f', 'Femenino'),
    )
    id = models.CharField(max_length=255, primary_key=True, verbose_name='Identificador de historia clínica')
    unidad = models.ForeignKey(Unidad, on_delete=models.SET_NULL, null=True)
    fecha = models.DateField(verbose_name='Fecha de inscripción')
    apellido1 = models.CharField(max_length=255, verbose_name='Apellido 1')
    apellido2 = models.CharField(max_length=255, verbose_name='Apellido 2')
    nombres = models.CharField(max_length=255, verbose_name='Nombres')
    ci = models.CharField(max_length=11, verbose_name='Carné de indentidad', unique=True, validators=[RegexValidator(regex='^.{11}$', message='Este campo debe tener 11 dígitos', code='nomatch')])
    edad = models.IntegerField(default=0)
    genero = models.CharField(max_length=255, choices=GENERO_CHOICES)

    def __str__(self):
        return self.nombres

    class Meta:
        verbose_name = 'Modelo de historia Clínica'
        verbose_name_plural = '01 - Modelos de historia Clínica'

class MedicamentosNacionales(models.Model):
    hc = models.ForeignKey(HistoriaClinica, on_delete=models.CASCADE, related_name='medicamentos_nacionales')
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Medicamento nacional'
        verbose_name_plural = 'Medicamentos nacionales'

class Fecha(models.Model):
    TIPO_CHOICES = (
        ('1','Positivo'),
        ('2', 'Ingreso'),
        ('3', 'Defuncion'),

    )
    hc = models.ForeignKey(HistoriaClinica, on_delete=models.CASCADE, related_name='fechas')
    tipo = models.CharField(max_length=255, choices=TIPO_CHOICES)
    fecha = models.DateField()
    notas = models.TextField()

    def __str__(self):
        return self.get_tipo_display()

    class Meta:
        verbose_name = 'Fecha'
        verbose_name_plural = 'Fechas'

class Comorbilidad(models.Model):
    hc = models.ForeignKey(HistoriaClinica, on_delete=models.CASCADE, related_name='comorbilidades')
    comorbilidad = models.CharField(max_length=255)

    def __str__(self):
        return self.comorbilidad

    class Meta:
        verbose_name = 'Comorbilidad'
        verbose_name_plural = 'Comorbilidades'

class EstudioRadiologico(models.Model):
    TIPO_CHOICES = (
        ('1','Rayos X'),
        ('2', 'TAC'),
    )
    hc = models.ForeignKey(HistoriaClinica, on_delete=models.CASCADE, related_name='estudios_radiologicos')
    tipo = models.CharField(max_length=255, choices=TIPO_CHOICES)
    imagen = models.FileField(upload_to='imagenes/')
    fecha = models.DateField()

    def  __str__(self):
        return self.tipo

    class Meta:
        verbose_name = 'Estudio radiológico'
        verbose_name_plural = 'Estudios radiológicos'

class TipoVacuna(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Tipo de vacuna'
        verbose_name_plural = 'Tipos de vacuna'

class Vacuna(models.Model):
    hc = models.ForeignKey(HistoriaClinica, on_delete=models.CASCADE, related_name='vacunas')
    tipo = models.ForeignKey(TipoVacuna, on_delete=models.DO_NOTHING, null=True, blank=True)
    dosis = models.IntegerField()
    fecha = models.DateField()

    def __str__(self):
        return str(self.tipo)

    class Meta:
        verbose_name = 'Vacuna'
        verbose_name_plural = 'Vacunas'

class ReactantesFaseAguda(models.Model):
    hc = models.ForeignKey(HistoriaClinica, on_delete=models.CASCADE, related_name= 'reactantes')
    proteinascr = models.FloatField()
    leucocitos_neutrofilo = models.FloatField()
    ferritina = models.FloatField()

    def __str__(self):
        return str(self.proteinascr)

    class Meta:
        verbose_name = 'Reactante de fase aguda'
        verbose_name_plural = 'Reactantes de fase aguda'

class SensibilidadMedicamentosa(models.Model):
    historia_clinica = models.ForeignKey(HistoriaClinica, on_delete=models.CASCADE)
    medicamento = models.ForeignKey(Medicamento, on_delete=models.SET_NULL, null=True,
                                    verbose_name='medicamento, sangre y derivados')
    reccion = models.ForeignKey(Reaccion, on_delete=models.SET_NULL, null=True, verbose_name='Reacción')
    fecha = models.DateField()

    def __str__(self):
        return str(self.medicamento) + ' - ' + str(self.reccion) + ' :' + str(self.fecha)

    class Meta:
        verbose_name = 'Sensibilidad Medicamentosa'
        verbose_name_plural = 'Sensibilidades Medicamentosas'

class RegistroTransfusion(models.Model):
    historia_clinica = models.ForeignKey(HistoriaClinica, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    preparado = models.CharField(max_length=255)
    numero = models.CharField(max_length=255, verbose_name='Número del frasco')
    volumen = models.FloatField(verbose_name='Volúmen')
    paciente = models.CharField(max_length=255)
    frasco = models.CharField(max_length=255)
    tecnico = models.CharField(max_length=255)

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Registro de transfusión'
        verbose_name_plural = 'Registro de transfusiones'

class AspectosPSI(models.Model):
    historia_clinica = models.ForeignKey(HistoriaClinica, on_delete=models.CASCADE)
    observaciones = models.TextField()

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Aspecto Sicosocial e Interrelación médico de sala-médico de la familia'
        verbose_name_plural = 'Aspectos Sicosociales e Interrelaciones médico de sala-médico de la familia'

class HistoriaEnfermedad(models.Model):
    historia_clinica = models.ForeignKey(HistoriaClinica, on_delete=models.CASCADE)
    motivo = models.TextField(verbose_name='Motivo del ingreso')
    historia = models.TextField(verbose_name='Historia de la enfermedad', help_text='Escribir las afecciones refiriendo'
                                                                                    ' su comienzo, la aparición cronológica de los síntomas, su evolución y terapéutica recibida')
    asma_bronquial_texto =  models.CharField(max_length=255, verbose_name='Asma bronquial', blank=True, null=True)
    asma_bronquial_personal = models.BooleanField(verbose_name='Personal', default=False)
    asma_bronquial_padre = models.BooleanField(verbose_name='Padre', default=False)
    asma_bronquial_madre = models.BooleanField(verbose_name='Madre', default=False)
    asma_bronquial_hijo = models.BooleanField(verbose_name='Hijo', default=False)
    asma_bronquial_otro = models.BooleanField(verbose_name='Otro', default=False)
    cardiopatia_isquemica_texto = models.CharField(max_length=255, verbose_name='Cardiopatía isquémica', blank=True, null=True)
    cardiopatia_isquemica_personal = models.BooleanField(verbose_name='Personal', default=False)
    cardiopatia_isquemica_padre = models.BooleanField(verbose_name='Padre', default=False)
    cardiopatia_isquemica_madre = models.BooleanField(verbose_name='Madre', default=False)
    cardiopatia_isquemica_hijo = models.BooleanField(verbose_name='Hijo', default=False)
    cardiopatia_isquemica_otro = models.BooleanField(verbose_name='Otro', default=False)
    hipertension_arterial_texto = models.CharField(max_length=255, verbose_name='Hipertensión arterial', blank=True, null=True)
    hipertension_arterial_personal = models.BooleanField(verbose_name='Personal', default=False)
    hipertension_arterial_padre = models.BooleanField(verbose_name='Padre', default=False)
    hipertension_arterial_madre = models.BooleanField(verbose_name='Madre', default=False)
    hipertension_arterial_hijo = models.BooleanField(verbose_name='Hijo', default=False)
    hipertension_arterial_otro = models.BooleanField(verbose_name='Otro', default=False)
    enfermedad_cerebro_vascular_texto = models.CharField(max_length=255, verbose_name='Enfermedad cerebro vascular', blank=True, null=True)
    enfermedad_cerebro_vascular_personal = models.BooleanField(verbose_name='Personal', default=False)
    enfermedad_cerebro_vascular_padre = models.BooleanField(verbose_name='Padre', default=False)
    enfermedad_cerebro_vascular_madre = models.BooleanField(verbose_name='Madre', default=False)
    enfermedad_cerebro_vascular_hijo = models.BooleanField(verbose_name='Hijo', default=False)
    enfermedad_cerebro_vascular_otro = models.BooleanField(verbose_name='Otro', default=False)
    epilepsia_texto = models.CharField(max_length=255, verbose_name='Epilepsia', blank=True, null=True)
    epilepsia_personal = models.BooleanField(verbose_name='Personal', default=False)
    epilepsia_padre = models.BooleanField(verbose_name='Padre', default=False)
    epilepsia_madre = models.BooleanField(verbose_name='Madre', default=False)
    epilepsia_hijo = models.BooleanField(verbose_name='Hijo', default=False)
    epilepsia_otro = models.BooleanField(verbose_name='Otro', default=False)
    diabetes_mellitus_texto = models.CharField(max_length=255, verbose_name='Diabetes mellitus', blank=True, null=True)
    diabetes_mellitus_personal = models.BooleanField(verbose_name='Personal', default=False)
    diabetes_mellitus_padre = models.BooleanField(verbose_name='Padre', default=False)
    diabetes_mellitus_madre = models.BooleanField(verbose_name='Madre', default=False)
    diabetes_mellitus_hijo = models.BooleanField(verbose_name='Hijo', default=False)
    diabetes_mellitus_otro = models.BooleanField(verbose_name='Otro', default=False)
    hepatitis_viral_texto = models.CharField(max_length=255, verbose_name='Hepatitis viral', blank=True, null=True)
    hepatitis_viral_personal = models.BooleanField(verbose_name='Personal', default=False)
    hepatitis_viral_padre = models.BooleanField(verbose_name='Padre', default=False)
    hepatitis_viral_madre = models.BooleanField(verbose_name='Madre', default=False)
    hepatitis_viral_hijo = models.BooleanField(verbose_name='Hijo', default=False)
    hepatitis_viral_otro = models.BooleanField(verbose_name='Otro', default=False)
    dengue_texto = models.CharField(max_length=255, verbose_name='Dengue', blank=True, null=True)
    dengue_personal = models.BooleanField(verbose_name='Personal', default=False)
    dengue_padre = models.BooleanField(verbose_name='Padre', default=False)
    dengue_madre = models.BooleanField(verbose_name='Madre', default=False)
    dengue_hijo = models.BooleanField(verbose_name='Hijo', default=False)
    dengue_otro = models.BooleanField(verbose_name='Otro', default=False)
    sifilis_texto = models.CharField(max_length=255, verbose_name='Sífilis', blank=True, null=True)
    sifilis_personal = models.BooleanField(verbose_name='Personal', default=False)
    sifilis_padre = models.BooleanField(verbose_name='Padre', default=False)
    sifilis_madre = models.BooleanField(verbose_name='Madre', default=False)
    sifilis_hijo = models.BooleanField(verbose_name='Hijo', default=False)
    sifilis_otro = models.BooleanField(verbose_name='Otro', default=False)
    blenorragia_texto = models.CharField(max_length=255, verbose_name='Blenorragia', blank=True, null=True)
    blenorragia_personal = models.BooleanField(verbose_name='Personal', default=False)
    blenorragia_padre = models.BooleanField(verbose_name='Padre', default=False)
    blenorragia_madre = models.BooleanField(verbose_name='Madre', default=False)
    blenorragia_hijo = models.BooleanField(verbose_name='Hijo', default=False)
    blenorragia_otro = models.BooleanField(verbose_name='Otro', default=False)
    tuberculosis_texto = models.CharField(max_length=255, verbose_name='Tuberculosis', blank=True, null=True)
    tuberculosis_personal = models.BooleanField(verbose_name='Personal', default=False)
    tuberculosis_padre = models.BooleanField(verbose_name='Padre', default=False)
    tuberculosis_madre = models.BooleanField(verbose_name='Madre', default=False)
    tuberculosis_hijo = models.BooleanField(verbose_name='Hijo', default=False)
    tuberculosis_otro = models.BooleanField(verbose_name='Otro', default=False)
    cancer_texto = models.CharField(max_length=255, verbose_name='Cáncer', blank=True, null=True)
    cancer_personal = models.BooleanField(verbose_name='Personal', default=False)
    cancer_padre = models.BooleanField(verbose_name='Padre', default=False)
    cancer_madre = models.BooleanField(verbose_name='Madre', default=False)
    cancer_hijo = models.BooleanField(verbose_name='Hijo', default=False)
    cancer_otro = models.BooleanField(verbose_name='Otro', default=False)
    otras_texto = models.CharField(max_length=255, verbose_name='Otras', blank=True, null=True)
    otras_personal = models.BooleanField(verbose_name='Personal', default=False)
    otras_padre = models.BooleanField(verbose_name='Padre', default=False)
    otras_madre = models.BooleanField(verbose_name='Madre', default=False)
    otras_hijo = models.BooleanField(verbose_name='Hijo', default=False)
    otras_otro = models.BooleanField(verbose_name='Otro', default=False)
    tipo_operacion = models.CharField(max_length=255, verbose_name='Tipo de operación', blank=True, null=True)
    secuelas = models.TextField(verbose_name='Secuelas', blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Historia de la enfermedad actual'
        verbose_name_plural = 'Historias de enfermedades'

def hash_string(string):
    return hashlib.sha256(string.encode('utf-8')).hexdigest()

class TAC(models.Model):
    historia_clinica = models.ForeignKey(HistoriaClinica, on_delete=models.CASCADE, null=True, blank=True)
    directorio = models.FileField(upload_to='TAC/')
    cant = models.IntegerField(default=0, blank=True, null=True)


    def __str__(self):
        return 'TAC ' + str(self.pk)

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        super().save(force_insert, force_update, *args, **kwargs)
        base = str(self.directorio.path)
        fichero = ""
        for char in reversed(base):
            if str(char).isdigit() or str(char) == '.':
                fichero = fichero + str(char)
            else:
                break
        pass_dicom = ''
        for char in reversed(fichero):
            pass_dicom = pass_dicom + str(char)
        pos = 0
        for char in reversed(base):
            pos = pos - 1
            if str(char) == '\\':
                pos = pos + 1
                break
        base = base[:pos]
        # enter DICOM image name for pattern
        # result is a list of 1 element
        filename = pydicom.data.data_manager.get_files(base, pass_dicom)[0]
        ds = pydicom.dcmread(filename)
        user = None
        for usuario in HistoriaClinica.objects.all():
            if usuario.ci == str(ds.get('PatientID')):
                user = usuario
        if user == None:
            nombre = str(ds.get('PatientName')).replace('^', ' ')
            nombre = nombre.replace('  ', ' ')
            nombre = nombre.replace('   ', ' ')
            nombre = nombre.split(' ')
            print(nombre)
            try:
                nombres = nombre[2] + ' ' + nombre[3]
            except IndexError:
                nombres = nombre[2]
            user = HistoriaClinica(id=hash_string(str(ds.get('PatientID'))),ci=str(ds.get('PatientID')), nombres=nombres, apellido1=nombre[0], apellido2=nombre[1], fecha=datetime.datetime.now())
            user.save()
        self.historia_clinica = user
        super().save(force_insert, force_update, *args, **kwargs)
        directorio = self.directorio
        if directorio:
            # Create new filename, using primary key and file extension
            path = os.path.join(MEDIA_ROOT, 'TAC\\' + str(self.historia_clinica.ci))
            if not os.path.isdir('/media/TAC/' + str(self.historia_clinica.ci)):
                os.mkdir(path)
        super().save(force_insert, force_update, *args, **kwargs)

    class Meta:
        verbose_name = 'Tomografía axial computarizada'
        verbose_name_plural = '05 - Tomografías axiales computarizadas'


