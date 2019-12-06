FROM python:3-alpine

ADD setup.py app/
ADD pwresource app/pwresource
RUN pip install --no-cache-dir app/ --install-option="--install-scripts=/opt/resource"
