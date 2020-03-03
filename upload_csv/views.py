from django.shortcuts import render
from django.views.generic import View
from django.urls import reverse
from django.http import HttpResponseRedirect
import csv
import tempfile
import uuid


class ViewUploadCSV(View):
    template_name = "read_cvs.html"

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}

        def handle_upload_csv(file):
            # nombre de archivo uuid y extencion .csv
            filename = str(uuid.uuid4()) + '.csv'

            # Crear directorio temporal
            with tempfile.TemporaryDirectory() as tmpdirname:

                # Crear un archivo temporal con los datos del archivo que se sube
                with open(tmpdirname + '/' + filename, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)

                # Recorer el archivo temporal
                with open(tmpdirname + '/' + filename) as csvfile:
                    reader = csv.DictReader(csvfile)  # Diccionario del csv
                    # Recorer datos uno por uno segun columna
                    for row in reader:
                        print(row['name'], row['age'])

        # iniciar funcion, enviar el objecto File
        handle_upload_csv(request.FILES['file_csv'])

        return HttpResponseRedirect(reverse('upload_csv'))
