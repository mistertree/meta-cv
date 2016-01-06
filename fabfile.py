from fabric.api import local, env, prompt, shell_env
import time

#Environments
def _define_env(compose_files, name, 
                webattached=False, password=None):
    env.compose_files = compose_files
    env.project_name = name
    env.webattached = webattached
    env.postgres_password = password if (password is not None) else prompt(
        "Database password:")
    
def localhost():
    _define_env(["local"], "local", True, "fakeAsth3$pecial3d1710|\|s")

def pylint():
    _define_env(["pylint"], "pylint", True, "fakepassword")

def production():
    _define_env(["production", "nginx"], "production")

#Commands
def _compose_command(command):
    with shell_env(POSTGRES_PASSWORD=env.postgres_password):
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
