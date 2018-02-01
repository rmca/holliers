import click

@click.command()
@click.argument('username', default='rob')
@click.option('--password')
def greet(username, password):
    click.echo('Hello %s %s!' % (username, password))

if __name__ == '__main__':
    greet(auto_envvar_prefix='GREETER')

