#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Build Tailwind CSS
echo "Installing Node.js dependencies and building Tailwind..."
cd theme/static_src
npm install
npm run build
cd ../..

python manage.py collectstatic --no-input
python manage.py migrate
python manage.py sync_media
