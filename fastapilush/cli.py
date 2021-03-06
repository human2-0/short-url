import webbrowser

import click
import requests


@click.group()
def cli():
    pass


@cli.command()
@click.option('--longurl', default=None, prompt='Url to short: ', help="Do not forget about http://")
def make_url(longurl):
    result = requests.post("http://127.0.0.1:8000/url/", json={'longurl': longurl})
    if result.status_code == 422:
        click.echo("invalid or missing URL scheme")
    else:
        click.echo(f"{result.json()}")


@cli.command()
@click.option('--shorturl', default=None,
              prompt='The given url from "make-url" command: ',
              help="Paste the link from make-url command if have got any.")
def url_flow(shorturl):
    webbrowser.open_new_tab(shorturl)

if __name__ == '__main__':
    cli()
