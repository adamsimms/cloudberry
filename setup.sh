#!/usr/bin/env bash
set -euo pipefail

cur_dir="$(cd "$(dirname "$0")" && pwd)"
user="$(id -u -n)"
config_file="${cur_dir}/config.ini"
secrets_file="${cur_dir}/secrets.env"

secure_files() {
  for file in "${config_file}" "${secrets_file}"; do
    if [[ -f "${file}" ]]; then
      chmod 600 "${file}"
      echo "Set ${file} permissions to 600"
    fi
  done
}

echo "Installing Cloudberry dependencies..."
sudo apt update
sudo apt install -y python3 python3-pip python3-venv libcamera-apps

if [[ ! -f "${config_file}" ]]; then
  cp "${cur_dir}/config.ini.example" "${config_file}"
  echo "Created ${config_file} — edit camera_type and delay."
fi

if [[ ! -f "${secrets_file}" ]]; then
  cp "${cur_dir}/.env.example" "${secrets_file}"
  echo "Created ${secrets_file} — add AWS and GoPro credentials."
fi

secure_files

python3 -m venv "${cur_dir}/.venv"
"${cur_dir}/.venv/bin/pip" install -e "${cur_dir}[pi]"

install_systemd="${INSTALL_SYSTEMD:-ask}"
if [[ "${install_systemd}" == "ask" ]]; then
  read -r -p "Install systemd user service? [y/N] " reply
  install_systemd=$([[ "${reply}" =~ ^[Yy]$ ]] && echo yes || echo no)
fi

if [[ "${install_systemd}" == "yes" ]]; then
  service_path="/home/${user}/.config/systemd/user/cloudberry.service"
  mkdir -p "$(dirname "${service_path}")"
  sed "s|%h|/home/${user}|g" "${cur_dir}/scripts/systemd/cloudberry.service" > "${service_path}"
  systemctl --user daemon-reload
  systemctl --user enable cloudberry.service
  echo "Installed ${service_path}"
fi

echo "Setup complete. Run: cloudberry --check-config"
