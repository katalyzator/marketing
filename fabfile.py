import datetime
from fabric.context_managers import cd, prefix
from fabric.operations import sudo, run, local
from fabric.state import env

from marketing.parameters import ROOT_FOLDER

PROJECT_NAME = 'newlife'
PROJECT_ROOT = '/var/www/html/newlife'
VENV_DIR = '/var/www/html/py3newlife_env'
REPO = ''


def migrate():
    local('./manage.py makemigrations')
    local('./manage.py migrate')


def commit():
    local('pip freeze > req.txt')
    local('git add .')
    local('git commit -m "' + str(datetime.datetime.today().date()) + '"')
    local('git push origin master')


def deploy():
    migrate()
    commit()
    env.host_string = '185.243.247.23'
    env.user = 'root'
    env.password = 'izpodkaptal96'
    with cd(PROJECT_ROOT):
        sudo('git stash')
        sudo('git pull origin master')
        with prefix('source ' + VENV_DIR + '/bin/activate'):
            run('pip install -r req.txt')
            run('cp ' + ROOT_FOLDER + '/parameters.py.dist ' + ROOT_FOLDER + '/parameters.py')
            run('./manage.py collectstatic --noinput')
            run('./manage.py migrate')
            # try:
            #     run('test -e main/parameters.py')
            # except:
            #     run('cp main/parameters.py.dis main/parameters.py')
            sudo('service apache2 restart')
            # sudo('service marketing restart')
            # sudo('service nginx restart')
