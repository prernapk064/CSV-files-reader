from django.db import models

class CSVFile(models.Model):
    csv_file = models.FileField(upload_to='csv_files/')

