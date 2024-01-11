

import os
import click
from dotenv import load_dotenv

from fmo.nmea import parse_nmea_file
from fmo.api import FMO, login_to_get_token, FMO_API_URL
from fmo.simulate import PathCreator
from fmo.draw import preview_geojson

from fmo.cli import lease

load_dotenv()


@click.group()
def cli():
    pass

@cli.command()
@click.argument('file')
def nmea(file):
    click.echo(file)
    if not file.endswith(".csv"):
        click.echo("Expecting a CSV file")
        return

    df = parse_nmea_file(file)
    print(df)

@cli.command()
@click.option("--url", prompt=True, default=FMO_API_URL)
@click.option("--farm", prompt=True, default="demo")
@click.option("--user", prompt=True)
@click.option("--password", prompt=True, hide_input=True)
def authenticate(url, farm, user, password):
    try:
        token = login_to_get_token(url, farm, user, password)
    except Exception as ex:
        click.echo(f"Authentication failed: {ex}")
        return

    # Write the token to the .env file
    with open(".env", "a") as f:
        f.write(f"# Added by FMO-CLI\n")
        f.write(f"FMO_TOKEN={token}\n")
        f.write(f"FMO_API_URL={url}\n")

    click.echo("Authentication successful. Token written to .env file.")
    click.echo("The token is a secret. Do not share it or commit it to git.")

@cli.command()
@click.option('--format', default="CSV", help="What format is the file? NMEA, CSV, GEOJSON")
@click.argument('file')
def upload_path(file, format):

    fmo_token = os.getenv("FMO_TOKEN")
    fmo_url = os.getenv("FMO_API_URL", FMO_API_URL)

    fmo = FMO(fmo_token, fmo_url)

    if format.lower() == "nmea":
        path = parse_nmea_file(file)
        df = path.dataframe()
        print(df)
        fmo.upload_path(path)
        return

    click.echo(f"Unexpected format: {format}")

@cli.command()
@click.option('--format', default="geojson", help="What format is the file? NMEA, CSV, GEOJSON")
@click.argument('file')
def preview_path(file, format):
    if format.lower() == "nmea":
        path = parse_nmea_file(file)
        preview_geojson(path.geojson())
        return
    
    if format.lower() == "geojson":
        preview_geojson(file)
        return

    click.echo(f"Unexpected format: {format}")
    

@cli.command()
@click.option("--output", "-o", default="output.json", help="Where to save the geojson result")
def generate_harvest_path(output):
    pc = PathCreator()
    points = pc.create_path()
    geojson_str = pc.gps_to_geojson(points)
    with open(output,'w+') as output_file:
        output_file.write(geojson_str)

@cli.command()
@click.argument('file')
def preview(file):
    # location=(38.91168873268766, -76.48163041965763)
    preview_geojson(file)

# Register sub-commands
lease.register_command(cli)

if __name__ == '__main__':
    cli()