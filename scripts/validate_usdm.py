import logging
import os
from datetime import datetime
from typing import Tuple

from cdisc_rules_engine.enums.default_file_paths import DefaultFilePaths
from cdisc_rules_engine.enums.progress_parameter_options import ProgressParameterOptions
from cdisc_rules_engine.enums.report_types import ReportTypes
from cdisc_rules_engine.enums.dataformat_types import DataFormatTypes
from cdisc_rules_engine.models.validation_args import Validation_args
from scripts.run_validation import run_validation
from cdisc_rules_engine.services.cache.cache_populator_service import CachePopulator
from cdisc_rules_engine.services.cache.cache_service_factory import CacheServiceFactory
from cdisc_rules_engine.services.cdisc_library_service import CDISCLibraryService
from cdisc_rules_engine.utilities.utils import (
    generate_report_filename,
)
from scripts import USDM_VERSION, LOCAL_RULES_PATH


def valid_data_file(data_path: list) -> Tuple[list, set]:
    allowed_formats = [format.value for format in DataFormatTypes]
    found_formats = set()
    file_list = []
    for file in data_path:
        file_extension = os.path.splitext(file)[1][1:].upper()
        if file_extension in allowed_formats:
            found_formats.add(file_extension)
            file_list.append(file)
    if len(found_formats) > 1:
        return [], found_formats
    elif len(found_formats) == 1:
        return file_list, found_formats


def validate_usdm(
    dataset_path: Tuple[str]
):
    """
    Validate USDM data using CDISC Rules Engine

    Example:

    validate_usdm(["/path/to/datasets"])
    """

    # Validate conditional options
    logger = logging.getLogger("validator")

    if dataset_path:
        dataset_paths, found_formats = valid_data_file([dp for dp in dataset_path])
        if len(found_formats) > 1:
            logger.error(
                f"Argument --dataset_path contains more than one allowed file format ({', '.join(found_formats)})."  # noqa: E501
            )
            exit()
    else:
        logger.error(
            "You must pass the following argument: --dataset-path"
        )
        # no need to define dataset_paths here, the program execution will stop
        exit()

    run_validation(
        Validation_args(
            os.path.join(os.path.dirname(__file__), "..", DefaultFilePaths.CACHE.value),
            10,
            dataset_paths,
            "debug",
            DefaultFilePaths.EXCEL_TEMPLATE_FILE.value,
            "usdm",
            USDM_VERSION,
            set(""),  # avoiding duplicates
            generate_report_filename(datetime.now().isoformat()),
            set([ReportTypes.XLSX.value]),  # avoiding duplicates
            False,
            "",
            "",
            "",
            LOCAL_RULES_PATH,
            False,
            "",
            ProgressParameterOptions.BAR.value,
            "",
        )
    )
