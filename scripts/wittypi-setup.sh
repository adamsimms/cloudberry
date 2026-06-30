#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
witty_pi_dir="${HOME}/wittyPi"
config_file="${repo_root}/config.ini"
sudoers_src="${repo_root}/docs/sudoers-cloudberry-shutdown"
sudoers_dest="/etc/sudoers.d/cloudberry-shutdown"

echo "Installing WittyPi 2 tooling from UUGear..."
tmp_installer="$(mktemp)"
curl -fsSL "http://www.uugear.com/repo/WittyPi2/installWittyPi.sh" -o "${tmp_installer}"
sudo sh "${tmp_installer}"
rm -f "${tmp_installer}"

enable_shutdown="${ENABLE_SHUTDOWN:-ask}"
if [[ "${enable_shutdown}" == "ask" ]]; then
  read -r -p "Enable shutdown_after in config.ini for WittyPi boot-once? [y/N] " reply
  enable_shutdown=$([[ "${reply}" =~ ^[Yy]$ ]] && echo yes || echo no)
fi

if [[ "${enable_shutdown}" == "yes" ]]; then
  if [[ -f "${config_file}" ]]; then
    if grep -q "^shutdown_after" "${config_file}"; then
      sed -i 's/^shutdown_after = .*/shutdown_after = true/' "${config_file}"
    else
      printf '\nshutdown_after = true\n' >> "${config_file}"
    fi
    chmod 600 "${config_file}"
    echo "Set shutdown_after = true in ${config_file}"
  else
    echo "Warning: ${config_file} not found. Copy config.ini.example first."
  fi

  echo "Installing sudoers rule for passwordless shutdown..."
  sudo cp "${sudoers_src}" "${sudoers_dest}"
  sudo chmod 440 "${sudoers_dest}"
  sudo visudo -cf "${sudoers_dest}"
  echo "Installed ${sudoers_dest}"
fi

echo
echo "WittyPi installed. Configure schedules with:"
echo "  cd ${witty_pi_dir} && sudo ./wittyPi.sh"
echo
echo "Cloudberry boot-once workflow:"
echo "  1. WittyPi powers the Pi on at the scheduled time"
echo "  2. systemd starts Cloudberry once at boot"
echo "  3. Cloudberry waits, captures, uploads, then exits"
echo "  4. With shutdown_after=true, Cloudberry shuts the Pi down automatically"
echo
echo "Install Cloudberry with: ${repo_root}/setup.sh"
echo "Or run once manually: cloudberry --shutdown"
