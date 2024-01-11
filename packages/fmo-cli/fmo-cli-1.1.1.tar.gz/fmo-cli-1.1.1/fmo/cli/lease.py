import os
import click

from fmo.api import FMO, FMO_API_URL
from fmo.draw import preview_lease
from fmo.lease import Lease

@click.group()
def lease():
    pass

@lease.command(name="list")
def list_leases():
    fmo_token = os.getenv("FMO_TOKEN")
    fmo_url = os.getenv("FMO_API_URL", FMO_API_URL)

    fmo = FMO(fmo_token, fmo_url)

    leases = fmo.list_water_leases()
    click.echo(f"{len(leases)} Leases Found")
    click.echo_via_pager("\n".join(f"{l['leaseId']} - {l['state']}" for l in leases))

@lease.command(name="get")
@click.argument('lease_id')
@click.option("--preview", default=False, is_flag=True)
def get_lease(lease_id, preview):
    fmo_token = os.getenv("FMO_TOKEN")
    fmo_url = os.getenv("FMO_API_URL", FMO_API_URL)

    fmo = FMO(fmo_token, fmo_url)

    leases = fmo.list_water_leases()
    leases = list(filter(lambda l: l['leaseId'] == lease_id, leases))
    if len(leases) == 0:
        click.echo("Lease Not Found")
        return
    
    print(leases[0])
    if preview:
        lease = Lease(leases[0])
        preview_lease(lease)
        
    

def register_command(cli):
    cli.add_command(lease)