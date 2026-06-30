# GitHub repository settings (owner checklist)

Apply these under **Settings** after merging v3.0 to `master`.

## About

**Description:**

> Raspberry Pi field rig: GoPro HERO3/4 and Pi camera capture with S3 upload for Pinchard's Island

**Website:** https://www.pinchards.is

## Topics

Suggested topics:

- `raspberry-pi`
- `gopro`
- `s3`
- `wittypi`
- `picamera`
- `field-camera`

## License

Confirm GitHub detects **MIT** from the `LICENSE` file (Settings → General → License).

## Security

Enable **Private vulnerability reporting** (Settings → Code security → Private vulnerability reporting). The repo is public; see [SECURITY.md](../SECURITY.md).

## Releases

After merging v3.0 to `master`:

1. Move or recreate tag `v3.0.0` on the merge commit
2. Publish a GitHub Release using [CHANGELOG.md](../CHANGELOG.md) § 3.0.0

## Archive piberry

Once v3.0 is released, archive or delete the deprecated **piberry** repo and add a pointer in its README to this repository.
