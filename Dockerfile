FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir .
COPY samples ./samples
USER 65532:65532
ENTRYPOINT ["feature-consistency-guard"]
CMD ["samples/compliant-contract.yaml"]
