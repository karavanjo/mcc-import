import click
import yaml
import logging

from mcc_import import import_observations, import_stations


@click.command()
@click.option('--config', default='config.yaml', help='YAML config')
def import_all(config: str):
    with open(config, "r") as f:
        yaml_config = yaml.safe_load(f)
        import_stations(yaml_config['DATABASE']['URI'], yaml_config['DATABASE']['CERT'])
        import_observations(yaml_config['DATABASE']['URI'], yaml_config['DATABASE']['CERT'])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    import_all()
