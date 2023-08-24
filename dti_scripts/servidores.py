import functools
import getpass

import fabric
import termcolor


def obter_senha_sudo(func=None, prompt='Senha administrador: '):
    def config(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            senha = getpass.getpass(prompt)
            config = fabric.Config(overrides=dict(sudo=dict(password=senha)))
            kwargs['config'] = config
            return func(*args, **kwargs)

        return wrapper

    return config if func is None else config(func)


@obter_senha_sudo(prompt='Senha administrador (192.168.0.190): ')
def reiniciar_apache_mobile2(config):
    termcolor.cprint(' ● Reiniciando apache do balanceador sigmobile', 'cyan')
    with fabric.Connection('balanceador-mobile2', config=config) as conn:
        conn.sudo('/etc/init.d/apache2 restart')

    termcolor.cprint(' ✔ Apache reinicializado com sucesso.\n', 'green')


@obter_senha_sudo(prompt='Senha administrador (192.168.0.191): ')
def reiniciar_polare_treinamento(config):
    reiniciar_apache_mobile2()

    termcolor.cprint(' ● Reiniciando polare treinamento', 'cyan')
    with fabric.Connection('polare-treinamento', config=config) as conn:
        with conn.cd('ambiente-polare'):
            conn.run('docker-compose down; docker-compose up -d')

    termcolor.cprint(' ✔ Polare treinamento reiniciado com sucesso.\n', 'green')


@obter_senha_sudo(prompt='Senha administrador (192.168.0.161): ')
def reiniciar_polare_producao(config):
    reiniciar_apache_mobile2()

    termcolor.cprint(' ● Reiniciando polare produção', 'cyan')
    with fabric.Connection('polare-producao', config=config) as conn:
        with conn.cd('ambiente-polare'):
            conn.run('docker-compose down; docker-compose up -d')

    termcolor.cprint(' ✔ Polare produção reiniciado com sucesso.\n', 'green')
