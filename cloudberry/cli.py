"""Command-line entry point for Cloudberry."""

from __future__ import annotations

import argparse
import logging
import subprocess
import sys
from pathlib import Path

from cloudberry.camera import capture_photo
from cloudberry.common import count_down, get_serial
from cloudberry.config import (
    ensure_config,
    get_aws_credentials,
    get_aws_region,
    get_bool_config,
    get_camera_type,
    get_config,
    get_section_config,
)
from cloudberry.gopro import GoProCtrl, capture_from_gopro
from cloudberry.logging_setup import resolve_log_dir, setup_logging
from cloudberry.queue import (
    collect_upload_candidates,
    load_queue,
    mark_failed,
    queue_paths,
    save_queue,
)
from cloudberry.s3 import build_object_key, create_s3_client, push_picture_to_s3
from cloudberry.secrets import load_secrets
from cloudberry.validate import run_preflight_checks, validate_config

REPO_ROOT = Path(__file__).resolve().parent.parent
IMAGE_DIR = REPO_ROOT / "images"

EXIT_OK = 0
EXIT_CONFIG = 1
EXIT_CAMERA = 2
EXIT_UPLOAD = 3
EXIT_PREFLIGHT = 4


def shutdown_system(logger: logging.Logger | None = None) -> bool:
    """Request an immediate system halt. Requires passwordless sudo for shutdown."""
    log = logger or logging.getLogger("Cloudberry")
    log.info("Requesting system shutdown")
    try:
        result = subprocess.run(
            ["sudo", "shutdown", "-h", "now"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        log.error("Failed to run shutdown command: %s", exc)
        return False

    if result.returncode != 0:
        stderr = result.stderr.strip() or "unknown error"
        log.error("Shutdown command failed (%s): %s", result.returncode, stderr)
        return False

    return True


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Cloudberry camera controller")
    parser.add_argument("--delay", type=int, help="Delay in minutes before capture")
    parser.add_argument("--dry-run", action="store_true", help="Run without uploading to S3")
    parser.add_argument("--no-upload", action="store_true", help="Capture only; skip S3 upload")
    parser.add_argument(
        "--no-capture",
        action="store_true",
        help="Upload any remaining local images without taking a new photo",
    )
    parser.add_argument("--retry-failed", action="store_true", help="Retry images/failed/")
    parser.add_argument("--check-config", action="store_true", help="Validate config and exit")
    parser.add_argument("--skip-preflight", action="store_true", help="Skip preflight checks")
    parser.add_argument("--shutdown", action="store_true", help="Shut down Pi after success")
    return parser.parse_args(argv)


def upload_file(
    logger: logging.Logger,
    *,
    image_path: Path,
    dry_run: bool,
    s3_client,
    bucket: str,
    key_prefix: str,
    make_public: bool,
    failed_dir: Path,
    queue_file: Path,
    queued_paths: list[Path],
) -> bool:
    file_key = build_object_key(key_prefix, image_path.name)
    if dry_run:
        logger.info("Dry run: would upload %s as s3://%s/%s", image_path, bucket, file_key)
        return True

    uploaded = push_picture_to_s3(
        s3_client,
        bucket,
        file_key,
        image_path,
        make_public=make_public,
    )
    if uploaded:
        image_path.unlink(missing_ok=True)
        if image_path in queued_paths:
            queued_paths.remove(image_path)
            save_queue(queue_file, queued_paths)
        logger.info("Removed local file after upload: %s", image_path)
        return True

    failed_path = mark_failed(image_path, failed_dir)
    if failed_path not in queued_paths:
        queued_paths.append(failed_path)
        save_queue(queue_file, queued_paths)
    logger.error("Upload failed; moved to %s", failed_path)
    return False


def report_validation(logger: logging.Logger, result) -> int:
    for warning in result.warnings:
        logger.info(warning)
    for error in result.errors:
        logger.error(error)
    return EXIT_OK if result.ok else EXIT_CONFIG


def capture_images(
    logger: logging.Logger, camera_type: str
) -> tuple[list[tuple[Path, str | None]], GoProCtrl | None]:
    if camera_type == "PICAMERA":
        settings = get_section_config("picamera")
        settings["_device_serial"] = get_serial()
        captured = capture_photo(IMAGE_DIR, settings)
        return [(captured, None)], None

    files, gopro = capture_from_gopro(IMAGE_DIR, camera_type)
    return files, gopro


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    load_secrets()
    ensure_config()
    log_dir = resolve_log_dir(get_config("general", "log_dir"))
    logger = setup_logging(log_dir=log_dir)

    config_result = validate_config()
    if args.check_config:
        preflight = run_preflight_checks(skip_camera=False, skip_s3=False)
        config_result.errors.extend(preflight.errors)
        config_result.warnings.extend(preflight.warnings)
        return report_validation(logger, config_result)

    if not config_result.ok:
        return report_validation(logger, config_result)

    IMAGE_DIR.mkdir(exist_ok=True)
    _, failed_dir, queue_file = queue_paths(IMAGE_DIR)
    queued_paths = [Path(path) for path in load_queue(queue_file)]

    camera_type = get_camera_type()

    if not args.skip_preflight:
        preflight = run_preflight_checks(
            skip_camera=args.no_capture,
            skip_s3=args.dry_run or args.no_upload,
        )
        if not preflight.ok:
            report_validation(logger, preflight)
            return EXIT_PREFLIGHT

    delay_minutes = args.delay
    if delay_minutes is None:
        delay_minutes = int(get_config("general", "delay", "1"))

    logger.info("Starting Cloudberry controller (%s, boot-once mode)", camera_type)
    if delay_minutes > 0:
        logger.debug("Sleeping for %s minute(s)", delay_minutes)
        count_down(delay_minutes * 60)

    bucket, access_key, secret_key = get_aws_credentials()
    region = get_aws_region()
    make_public = get_bool_config("general", "make_public", default=False)
    configured_prefix = get_config("general", "s3_key_prefix", "") or ""
    key_prefix = configured_prefix.strip() or get_serial()

    dry_run = args.dry_run
    skip_upload = dry_run or args.no_upload
    s3_client = create_s3_client(access_key, secret_key, region) if not skip_upload else None

    upload_failures = 0
    if not skip_upload:
        for image_path in collect_upload_candidates(IMAGE_DIR, include_failed=args.retry_failed):
            if not upload_file(
                logger,
                image_path=image_path,
                dry_run=dry_run,
                s3_client=s3_client,
                bucket=bucket,
                key_prefix=key_prefix,
                make_public=make_public,
                failed_dir=failed_dir,
                queue_file=queue_file,
                queued_paths=queued_paths,
            ):
                upload_failures += 1

    gopro: GoProCtrl | None = None
    if not args.no_capture:
        try:
            captured_files, gopro = capture_images(logger, camera_type)
            for image_path, remote_name in captured_files:
                if skip_upload:
                    continue
                if not upload_file(
                    logger,
                    image_path=image_path,
                    dry_run=dry_run,
                    s3_client=s3_client,
                    bucket=bucket,
                    key_prefix=key_prefix,
                    make_public=make_public,
                    failed_dir=failed_dir,
                    queue_file=queue_file,
                    queued_paths=queued_paths,
                ):
                    upload_failures += 1
                elif gopro and remote_name:
                    gopro.delete(remote_name)
        except (RuntimeError, ValueError) as exc:
            logger.error("%s", exc)
            return EXIT_CAMERA
        except Exception as exc:
            logger.exception("Failed to capture images: %s", exc)
            return EXIT_CAMERA

    if gopro:
        count_down(10)
        gopro.sleep()
        count_down(5)

    if upload_failures:
        logger.error("Cloudberry finished with %s failed upload(s)", upload_failures)
        return EXIT_UPLOAD

    logger.info("Cloudberry controller finished")

    should_shutdown = args.shutdown or get_bool_config("general", "shutdown_after", default=False)
    if should_shutdown and not dry_run:
        if not shutdown_system(logger):
            logger.error("shutdown_after is enabled but shutdown failed (check sudoers)")
            return EXIT_CONFIG

    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
