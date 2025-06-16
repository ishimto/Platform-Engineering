FROM syseleven/kubectl-helm AS tools


FROM python:3.12-slim

COPY --from=tools /usr/bin/kubectl /usr/local/bin/kubectl
COPY --from=tools /usr/bin/helm /usr/local/bin/helm

RUN useradd --create-home nonroot
RUN chown -R nonroot:nonroot /usr/local/bin/
USER nonroot
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD python app.py
