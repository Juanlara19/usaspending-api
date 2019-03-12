import boto3
import logging
import math
import os
import pandas as pd

from datetime import datetime
from django.conf import settings
from rest_framework.exceptions import ParseError

from usaspending_api.common.exceptions import InvalidParameterException

logger = logging.getLogger("console")


def check_types_and_assign_defaults(old_dict, new_dict, defaults_dict):
    """Validates the types of the old_dict, and assigns them to the new_dict"""
    for field in defaults_dict.keys():
        # Set the new value to the old value, or the default if it doesn't exist
        new_dict[field] = old_dict.get(field, defaults_dict[field])

        # Validate the field's data type
        if not isinstance(new_dict[field], type(defaults_dict[field])):
            type_name = type(defaults_dict[field]).__name__
            raise InvalidParameterException("{} parameter not provided as a {}".format(field, type_name))

        # Remove empty filters
        if new_dict[field] == defaults_dict[field]:
            del (new_dict[field])


def parse_limit(json_request):
    """Validates the limit from a json_request
    Returns the limit as an int"""
    limit = json_request.get("limit")
    if limit:
        try:
            limit = int(json_request["limit"])
        except (ValueError, TypeError):
            raise ParseError('Parameter "limit" must be int; {} given'.format(limit))
        if limit > settings.MAX_DOWNLOAD_LIMIT:
            msg = "Requested limit {} beyond max supported ({})"
            raise ParseError(msg.format(limit, settings.MAX_DOWNLOAD_LIMIT))
    else:
        limit = settings.MAX_DOWNLOAD_LIMIT
    return limit  # None is a workable slice argument


def validate_time_periods(filters, new_request):
    """Validates passed time_period filters, or assigns the default values.
    Returns the number of days selected by the user"""
    default_date_values = {
        "start_date": "1000-01-01",
        "end_date": datetime.strftime(datetime.utcnow(), "%Y-%m-%d"),
        "date_type": "action_date",
    }

    # Enforcing that time_period always has content
    if len(filters.get("time_period", [])) == 0:
        filters["time_period"] = [default_date_values]
    new_request["filters"]["time_period"] = filters["time_period"]

    total_range_count = 0
    for date_range in new_request["filters"]["time_period"]:
        # Empty strings, Nones, or missing keys should be replaced with the default values
        for key in default_date_values:
            date_range[key] = date_range.get(key, default_date_values[key])
            if date_range[key] == "":
                date_range[key] = default_date_values[key]

        # Validate date values
        try:
            d1 = datetime.strptime(date_range["start_date"], "%Y-%m-%d")
            d2 = datetime.strptime(date_range["end_date"], "%Y-%m-%d")
        except ValueError:
            raise InvalidParameterException("Date Ranges must be in the format YYYY-MM-DD.")

        # Add to total_range_count for year-constraint validations
        total_range_count += (d2 - d1).days

        # Validate and derive date type
        if date_range["date_type"] not in ["action_date", "last_modified_date"]:
            raise InvalidParameterException(
                "Invalid parameter within time_period's date_type: {}".format(date_range["date_type"])
            )

    return total_range_count


def verify_requested_columns_available(sources, requested):
    """Ensures the user-requested columns are availble to write to"""
    bad_cols = set(requested)
    for source in sources:
        bad_cols -= set(source.columns(requested))
    if bad_cols:
        raise InvalidParameterException("Unknown columns: {}".format(bad_cols))


def multipart_upload(bucketname, regionname, source_path, keyname):
    s3client = boto3.client("s3", region_name=regionname)
    source_size = os.stat(source_path).st_size
    # Sets the chunksize at minimum ~5MB to sqrt(5MB) * sqrt(source size)
    bytes_per_chunk = max(int(math.sqrt(5242880) * math.sqrt(source_size)), 5242880)
    config = boto3.s3.transfer.TransferConfig(multipart_chunksize=bytes_per_chunk)
    transfer = boto3.s3.transfer.S3Transfer(s3client, config)
    transfer.upload_file(source_path, bucketname, os.path.basename(keyname))


def write_to_download_log(message, download_job=None, is_debug=False, is_error=False, other_params={}):
    """Handles logging for the downloader instance"""
    if settings.IS_LOCAL:
        log_dict = message
    else:
        log_dict = {"message": message, "message_type": "USAspendingDownloader"}

        if download_job:
            log_dict["download_job_id"] = download_job.download_job_id
            log_dict["file_name"] = download_job.file_name
            log_dict["json_request"] = download_job.json_request
            if download_job.error_message:
                log_dict["error_message"] = download_job.error_message

        for param in other_params:
            if param not in log_dict:
                log_dict[param] = other_params[param]

    if is_error:
        logger.exception(log_dict)
    elif is_debug:
        logger.debug(log_dict)
    else:
        logger.info(log_dict)


def pull_modified_agencies_cgacs():
    # Get a cgac_codes from the modified_agencies_list
    file_path = os.path.join(settings.BASE_DIR, "usaspending_api", "data", "modified_authoritative_agency_list.csv")
    with open(file_path, encoding="Latin-1") as modified_agencies_list_csv:
        mod_gencies_list_df = pd.read_csv(modified_agencies_list_csv, dtype=str)

    mod_gencies_list_df = mod_gencies_list_df[["CGAC AGENCY CODE"]]
    mod_gencies_list_df["CGAC AGENCY CODE"] = mod_gencies_list_df["CGAC AGENCY CODE"].apply(lambda x: x.zfill(3))

    # Return list of CGAC codes
    return [row["CGAC AGENCY CODE"] for _, row in mod_gencies_list_df.iterrows()]
