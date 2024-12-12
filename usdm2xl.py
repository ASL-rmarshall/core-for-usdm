import os
import click
import pandas as pd
from datetime import datetime
from multiprocessing import freeze_support
from multiprocessing.managers import SyncManager
from cdisc_rules_engine.config.config import ConfigService
from cdisc_rules_engine.services.data_services import USDMDataService
from cdisc_rules_engine.services.cache import (
    InMemoryCacheService,
    RedisCacheService,
)
from cdisc_rules_engine.config import config


class CacheManager(SyncManager):
    pass

def get_cache_service(manager):
    cache_service_type = config.getValue("CACHE_TYPE")
    if cache_service_type == "redis":
        return manager.RedisCacheService(
            config.getValue("REDIS_HOST_NAME"), config.getValue("REDIS_ACCESS_KEY")
        )
    else:
        return manager.InMemoryCacheService()

@click.command()
@click.option(
    "-dp",
    "--dataset-path",
    required=True,
    help="Absolute path to USDM JSON file",
)
def cli(dataset_path: str):
    """
    Convert USDM JSON file to Excel format

    Example:

    python usdm2xl.py -dp /path/to/usdm/json/file
    """
    CacheManager.register("RedisCacheService", RedisCacheService)
    CacheManager.register("InMemoryCacheService", InMemoryCacheService)
    manager = CacheManager()
    manager.start()
    shared_cache = get_cache_service(manager)
    data_service = USDMDataService.get_instance(
        config=ConfigService(), cache_service=shared_cache, dataset_path=dataset_path
    )
    timestamp = (
        datetime.fromisoformat(datetime.now().isoformat())
        .replace(microsecond=0)
        .isoformat()
        .replace(":", "-")
    )
    with pd.ExcelWriter(
        os.path.join(
            "".join(os.path.split(dataset_path)[:1]),
            f"{os.path.basename(dataset_path).split('.')[0]}-{timestamp}.xlsx",
        )
    ) as writer:
        for ds in data_service.dataset_content_index:
            data_service.get_dataset(dataset_name=ds["dataset_name"]).data.to_excel(
                writer,
                sheet_name=f"{ds['domain']}",
                index=False,
            )


if __name__ == "__main__":
    freeze_support()
    cli()
