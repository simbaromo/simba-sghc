from rest_framework import serializers

from core.models import *

class ReaccionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reaccion
        fields = ('__all__')

class MedicamentoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Medicamento
        fields = ('__all__')

class UnidadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Unidad
        fields = ('__all__')

class MedicamentosNacionalesSerializer(serializers.ModelSerializer):

    class Meta:
        model = MedicamentosNacionales
        fields = ('__all__')

class FechaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fecha
        fields = ('__all__')

class ComorbilidadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comorbilidad
        fields = ('__all__')

class EstudioRadiologicoSerializer(serializers.ModelSerializer):

    class Meta:
        model = EstudioRadiologico
        fields = ('__all__')

class VacunaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vacuna
        fields = ('__all__')

class ReactantesFaseAgudaSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReactantesFaseAguda
        fields = ('__all__')

class SensibilidadMedicamentosaSerializer(serializers.ModelSerializer):
    medicamento = MedicamentoSerializer()
    reccion = ReaccionSerializer()

    class Meta:
        model = SensibilidadMedicamentosa
        fields = ('__all__')

class RegistroTransfusionSerializer(serializers.ModelSerializer):

    class Meta:
        model = RegistroTransfusion
        fields = ('__all__')

class HistoriaClinicaSerializer(serializers.ModelSerializer):
    unidad = UnidadSerializer()
    medicamentos_nacionales = MedicamentosNacionalesSerializer(many=True)
    fechas = FechaSerializer(many=True)
    comorbilidades = ComorbilidadSerializer(many=True)
    estudios_radiologicos = EstudioRadiologicoSerializer(many=True)
    vacunas = VacunaSerializer(many=True)
    reactantes = ReactantesFaseAgudaSerializer(many=True)
    sensibilidadmedicamentosa_set = SensibilidadMedicamentosaSerializer(many=True)
    registrotransfusion_set = RegistroTransfusionSerializer(many=True)

    class Meta:
        model = HistoriaClinica
        fields = '__all__'
