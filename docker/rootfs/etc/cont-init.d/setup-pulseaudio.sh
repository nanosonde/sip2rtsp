#!/command/with-contenv bash
# shellcheck shell=bash
# setup pulse user and pulse-access group

set -o errexit -o nounset -o pipefail

echo "Creating user pulse and group pulse-access";
adduser --home /usr/local/pulseaudio/var/run/pulse --disabled-password --disabled-login --gecos '' pulse \
&& addgroup pulse-access \
&& adduser pulse pulse-access \
&& adduser root pulse \
&& adduser root pulse-access
echo "Done.";

echo "Setting up pulseaudio runtime path";
mkdir -p /usr/local/pulseaudio/var/lib/pulse
chown pulse.pulse /usr/local/pulseaudio/var/lib/pulse
chmod 644 /usr/local/pulseaudio/var/lib/pulse
echo "Done.";

echo "Modifying pulseaudio client config";
echo "autospawn = no" >> /usr/local/pulseaudio/etc/pulse/client.conf
echo "default-server = unix:/tmp/pulseaudio.socket" >> /usr/local/pulseaudio/etc/pulse/client.conf
echo "enable-shm = no" >> /usr/local/pulseaudio/etc/pulse/client.conf
echo "daemon-binary = /bin/true" >> /usr/local/pulseaudio/etc/pulse/client.conf
cp -av /usr/local/pulseaudio/etc/pulse/client.conf /etc/pulse/client.conf
echo "Done.";

echo "Overwriting the default system mode script";
cp -av /etc/pulse/system.pa /usr/local/pulseaudio/etc/pulse/system.pa
echo "Done.";
