import sys
import os
import django
#path to the project folder
sys.path.append('C:/Users/acer-pc/Documents/ET/my_project_folder/cpm_django/src/')
#project name
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
django.setup()

import openpyxl
#app name
from cpm.models import OrderPriority, Material
#from mysite import settings
#from django.core.management import setup_environ

#setup_environ(settings)

def update_priority():
    materials = Material.objects.all()
    for mat in materials:
      print mat.id
      try:
        p = Material.objects.get(id=mat.id)
        print 'in here'
        #print 'value is',p.order_priority.priority_id - this print breaks the script
        #if not p.order_priority.priority_id:
          #p.order_priority.priority_id = 300
        p.order_priority= OrderPriority.objects.get(priority_id=300)
        print p.order_priority
        p.save(update_fields=['order_priority'])
      except Exception as e:
           print str(e)


if __name__ == "__main__":
    update_priority()