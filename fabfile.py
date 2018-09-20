import datetime
from fabric.context_managers import cd, prefix
from fabric.operations import sudo, run, local
from fabric.state import env

PROJECT_NAME = 'marketing'
PROJECT_ROOT = '/var/www/html/marketing'
VENV_DIR = '/var/www/html/marketing_env'
REPO = ''


def migrate():
    local('./manage.py makemigrations')
    local('./manage.py migrate')


def commit():
    local('pip freeze > req.txt')
    local('git add .')
    local('git commit -m "' + str(datetime.datetime.today()) + '"')
    local('git push origin master')


def deploy():
    migrate()
    commit()
    env.host_string = '37.46.128.80'
    env.user = 'root'
    env.password = 'V7eWTZ1603Zc'
    with cd(PROJECT_ROOT):
        sudo('git stash')
        sudo('git pull origin master')
        with prefix('source ' + VENV_DIR + '/bin/activate'):
            run('pip install -r req.txt')
            run('./manage.py collectstatic --noinput')
            run('./manage.py migrate')
            # try:
            #     run('test -e main/parameters.py')
            # except:
            #     run('cp main/parameters.py.dis main/parameters.py')
            sudo('service marketing restart')
            sudo('service nginx restart')
