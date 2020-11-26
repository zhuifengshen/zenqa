from fabric import Connection
from invoke import Responder
from _credentials import github_username, github_password, server_ip, server_password


def _get_github_auth_responders():
    """
    返回 GitHub 用户名密码自动填充器
    """
    username_responder = Responder(
        pattern="Username for 'https://github.com':",
        response='{}\n'.format(github_username)
    )
    password_responder = Responder(
        pattern="Password for 'https://{}@github.com':".format(github_username),
        response='{}\n'.format(github_password)
    )
    return [username_responder, password_responder]


if __name__ == '__main__':
    supervisor_conf_path = './'
    supervisor_program_name = 'zenqa'
    project_root_path = '~/apps/zenqa/'

    c = Connection(server_ip, connect_kwargs={"password": server_password})
    
    # 先停止应用
    with c.cd(project_root_path):
        cmd = 'pipenv run supervisorctl stop {}'.format(supervisor_program_name)
        c.run(cmd)

    # 进入项目根目录，从 Git 拉取最新代码
    with c.cd(project_root_path):
        cmd = 'git pull'
        responders = _get_github_auth_responders()
        c.run(cmd, watchers=responders)

    # 安装依赖，迁移数据库，收集静态文件
    with c.cd(project_root_path):
        c.run('pipenv install --deploy --ignore-pipfile')
        c.run('pipenv run python manage.py migrate')
        c.run('pipenv run python manage.py collectstatic --noinput')

    # 重新启动应用
    with c.cd(project_root_path):      
        cmd = 'pipenv run supervisorctl start {}'.format(supervisor_program_name)
        c.run(cmd)
