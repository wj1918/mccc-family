import subprocess,os,io,sys,django
from subprocess import Popen, PIPE
from tempfile import NamedTemporaryFile
from django.db import connection, transaction

def import_mdb_schema (mdbfile,table_name,prefix):
    mdbschema=os.environ['OPENSHIFT_RUNTIME_DIR']+"/libs/bin/mdb-schema"
    cmd = [mdbschema, '-N', prefix,'-T', table_name,'--drop-table', mdbfile, 'mysql']

    f = NamedTemporaryFile(delete=False)
    p = subprocess.Popen(cmd, stdout=f)
    filename=f.name 
    errcode = p.wait()
    f.close()
    if errcode:
        errmess = p.stderr.read()
        log.error('cmd failed <%s>: %s' % (errcode,errmess))

    return filename

def import_mdb_data (mdbfile,table_name,prefix):
    mdbexport=os.environ['OPENSHIFT_RUNTIME_DIR']+"/libs/bin/mdb-export"
    cmd = [mdbexport, '-N', prefix,'-I', 'mysql', mdbfile, table_name]

    f = NamedTemporaryFile(delete=False)
    p = subprocess.Popen(cmd, stdout=f)
    filename=f.name 
    errcode = p.wait()
    f.close()
    if errcode:
        errmess = p.stderr.read()
        log.error('cmd failed <%s>: %s' % (errcode,errmess))

    return filename
    

def execure_file(filename):
    os.environ['DJANGO_SETTINGS_MODULE'] = os.environ['OPENSHIFT_DJANGO_PROJECT_NAME']+'.settings'
    sys.path.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'wsgi', os.environ['OPENSHIFT_DJANGO_PROJECT_NAME']))
    django.setup()
    cursor = connection.cursor()
    f = open(filename)
#    response = cursor.execute(f.read())  
    for line in open(filename):
        print (line)
        cursor.execute(line)

datafile=import_mdb_data('/tmp/family.mdb','Person','MCCC2');
print(datafile)
execure_file(datafile)

#schemafile=import_mdb_schema('/tmp/family.mdb','Person','MCCC2');
#print(schemafile)
#execure_file(schemafile)



