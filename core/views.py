import os
import shutil
from zipfile import ZipFile

from django.shortcuts import render
from django.views.generic.edit import FormView

from sghc import settings
from .forms import FileFieldForm
from .models import TAC, EstudioRadiologico, HistoriaClinica
from datetime import date
import pydicom
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib import messages

def handle_uploaded_file(f, ci):
    media_root = settings.MEDIA_ROOT
    with open(media_root.replace('/', '\\') + '\\imagenes\\' + 'ci\\' + str(ci) + '\\' + str(f), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
        return destination

def handle_uploaded_file_x(f, ci):
    media_root = settings.MEDIA_ROOT
    with open(media_root.replace('/', '\\') + '\\imagenes\\' + 'ci\\' + str(ci) + '\\' + str(f) + '_' + str(date.today()), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
        return destination

class FileFieldFormView(FormView):
    form_class = FileFieldForm
    template_name = 'dicom_uploader.html'  # Replace with your template.
    success_url = '/admin/'  # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            media_root = settings.MEDIA_ROOT
            estudio_radiologico = EstudioRadiologico()
            if len(files) > 1:
                estudio_radiologico.tipo = '2'
                primero = True
                zipObj = None
                hc = None
                for f in files:
                    if primero:
                        ds = pydicom.filereader.dcmread(f)
                        ci = ds[0x10, 0x20].value
                        if len(ci) > 11:
                            ci = ci[:11]
                        directory = 'ci\\{}'.format(ci)
                        parent_dir = media_root + 'imagenes\\'
                        path = os.path.join(parent_dir, directory)
                        mode = 0o666
                        try:
                            os.makedirs(path.replace('/', '\\'), mode)
                        except OSError as error:
                            print(error)
                        tmp_file = handle_uploaded_file(f, ci)
                        try:
                            hc = HistoriaClinica.objects.get(ci=ci)
                            estudio_radiologico.hc = hc
                        except:
                            messages.add_message(request, messages.ERROR,
                                                 'No existe Historia Clínica con este CI: {}'.format(ci))
                            return self.form_invalid(form)
                        estudio_radiologico.imagen = 'imagenes\\' + 'ci\\' + str(ci) +'\\' + str(ci) + '_' +\
                                                     str(date.today()) + '.zip'
                        estudio_radiologico.fecha = date.today()
                        estudio_radiologico.save()
                        zipObj = ZipFile(str(ci) + '_' + str(date.today()) + '.zip', 'w')
                        zipObj.write(tmp_file.name, os.path.basename(tmp_file.name))
                        primero = False
                    else:
                        ds = pydicom.filereader.dcmread(f)
                        ci = ds[0x10, 0x20].value
                        tmp_file = handle_uploaded_file(f, ci)
                        zipObj.write(tmp_file.name, os.path.basename(tmp_file.name))
                    os.remove(tmp_file.name)
                zipObj.close()
                shutil.copy(zipObj.filename, str(path).replace('/', '\\'))
                os.remove(zipObj.filename)
                messages.add_message(request, messages.SUCCESS, 'Se agregó un TAC de {} imágenes a '
                                                                'la Historia Clínica {}'.format(len(files), hc.id))
                return self.form_valid(form)
            else:
                estudio_radiologico.tipo = '1'
                ds = pydicom.filereader.dcmread(files[0])
                ci = ds[0x10, 0x20].value
                if len(ci) > 11:
                    ci = ci[:11]
                directory = 'ci\\{}'.format(ci)
                parent_dir = media_root + 'imagenes\\'
                path = os.path.join(parent_dir, directory)
                mode = 0o666
                try:
                    os.makedirs(path.replace('/', '\\'), mode)
                except OSError as error:
                    print(error)
                tmp_file = handle_uploaded_file_x(files[0], ci)
                try:
                    hc = HistoriaClinica.objects.get(ci=ci)
                    estudio_radiologico.hc = hc
                except:
                    messages.add_message(request, messages.ERROR,
                                         'No existe Historia Clínica con este CI: {}'.format(ci))
                    return self.form_invalid(form)
                estudio_radiologico.imagen = '\\imagenes\\' + 'ci\\' + str(ci) + '\\' + str(files[0]) + '_' + str(date.today())
                estudio_radiologico.fecha = date.today()
                estudio_radiologico.save()
                messages.add_message(request, messages.SUCCESS,'Se agregó la Imagen de Rayos X a la Historia '
                                                               'Clínica {}'.format(hc.id))
                return self.form_valid(form)
        else:
            return self.form_invalid(form)

def subir_dicom(request):
    return render(request, 'dicom_uploader.html', {})