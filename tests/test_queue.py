from pathlib import Path

from cloudberry.queue import (
    collect_upload_candidates,
    load_queue,
    mark_failed,
    queue_paths,
    save_queue,
)


def test_queue_paths_creates_directories(tmp_path: Path):
    pending, failed, queue_file = queue_paths(tmp_path)
    assert pending.exists()
    assert failed.exists()
    assert queue_file.name == ".upload-queue.json"


def test_save_and_load_queue(tmp_path: Path):
    _, _, queue_file = queue_paths(tmp_path)
    image = tmp_path / "pending" / "photo.jpg"
    image.parent.mkdir(parents=True, exist_ok=True)
    image.write_text("data", encoding="utf-8")

    save_queue(queue_file, [image])
    assert load_queue(queue_file) == [str(image)]


def test_mark_failed_moves_file(tmp_path: Path):
    _, failed, _ = queue_paths(tmp_path)
    source = tmp_path / "photo.jpg"
    source.write_text("data", encoding="utf-8")

    destination = mark_failed(source, failed)

    assert destination == failed / "photo.jpg"
    assert destination.exists()
    assert not source.exists()


def test_collect_upload_candidates_includes_failed(tmp_path: Path):
    pending, failed, _ = queue_paths(tmp_path)
    pending_file = pending / "pending.jpg"
    failed_file = failed / "failed.jpg"
    pending_file.write_text("a", encoding="utf-8")
    failed_file.write_text("b", encoding="utf-8")

    default_candidates = collect_upload_candidates(tmp_path)
    with_failed = collect_upload_candidates(tmp_path, include_failed=True)

    assert failed_file not in default_candidates
    assert failed_file in with_failed
    assert pending_file in with_failed
