FROM python:3.13-slim

COPY requirements_docker.txt ./requirements.txt

RUN apt-get update && \
	apt-get upgrade -y && \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/* && \
	pip install --upgrade pip && \
	pip install --no-cache-dir -r requirements.txt

RUN groupadd -g 1000 appuser && \
	useradd -u 1000 -g 1000 nonroot

RUN mkdir -p /app

COPY --chown=1000:1000 app.py /app/
COPY --chown=1000:1000 templates/ /app/templates
COPY --chown=1000:1000 static/ /app/static

EXPOSE 5000

USER 1000:1000
WORKDIR /app

#CMD ["python", "app.py"]
# Recommended: (2 x cores) + 1. We only want to use 1 core.

CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:5000", "app:app"]