#!/command/with-contenv bash
# shellcheck shell=bash
# setup pulse user and pulse-access group

set -o errexit -o nounset -o pipefail

echo "Creating user pulse and group pulse-access";
adduser --home /usr/local/pulseaudio/var/run/pulse --disabled-password --disabled-login --gecos "" pulse \
&& addgroup pulse-access \
&& adduser pulse pulse-access \
&& adduser root pulse \
&& adduser root pulse-access \

mkdir -p /usr/local/pulseaudio/var/lib/pulse
chown pulse.pulse /usr/local/pulseaudio/var/lib/pulse
chmod 644 /usr/local/pulseaudio/var/lib/pulse

echo "Done.";

# Overwrite the default config files with ours
cp -av /etc/pulse /usr/local/pulseaudio/etc/
