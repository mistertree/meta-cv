from fabric.api import local, env, prompt, shell_env
import time

#Environments
def _define_env(compose_files, name, django_env, 
                webattached=False, password=None, secret_key=None,
                google_analytics_key = None):
    env.compose_files = compose_files
    env.project_name = name
    env.webattached = webattached
    def _(variable, message, dummydata=None):
        return variable if (variable is not None) else prompt(message,
            default=dummydata)
        
    env.shell_env_vars = {
        'POSTGRES_PASSWORD': _(password, "Database password:", "sideshow"),
        'SECRET_KEY' : _(secret_key, "Django's secret key:", "sideshow"),
        'DJANGO_SETTINGS_MODULE' : "metacvserver.conf.%s" % django_env,
        'GOOGLE_ANALYTICS_KEY': _(google_analytics_key, 
            'Google Analytics Key:', "UA-0-1")
    }

def localhost():
    _define_env(["local"], "local", "localhost", True, 
        "fakeAsth3$pecial3d1710|\|s", "thiskeyissosecretololololololo",
        "UA-0-0")

def pylint():
    _define_env(["pylint"], "pylint", "localhost", True, "fakepassword", 
        "petitecle", "UA-0-0")

def production():
    _define_env(["production", "nginx"], "production", "production")

#Commands
def _compose_command(command):
    with shell_env(**env.shell_env_vars):
        local("docker-compose -f docker-compose.yml\
              {files} -p {project} {command}".format(
            files = " ".join(["-f docker-compose.{name}.yml".format(name=name) 
                              for name in env.compose_files]),
            project = "metacv{name}".format(name = env.project_name),
            command = command
        ))

def _setup():
    _compose_command("build")
    _compose_command("up -d db")
    time.sleep(10)
    _compose_command("run web python3.4 ./manage.py migrate")
    _compose_command("run web python3.4 ./manage.py collectstatic --noinput")

def up():
    _setup()
    _compose_command("up -d")
    if env.webattached:
        _compose_command("kill web")
        _compose_command("rm -f web")
        _compose_command("run --service-ports web")

def management_command(command):
    _setup()
    _compose_command("run web python3.4 ./manage.py "+command)
    
def ps():
    _compose_command("ps")

def rm():
    _compose_command("kill web db")
    _compose_command("rm web db")

def rm_db():
    _compose_command("rm dbdata webmedia")

def logs(container):
    _compose_command("logs "+container)
