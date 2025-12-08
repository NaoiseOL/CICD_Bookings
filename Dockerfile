FROM python:3.11-slim AS builder
WORKDIR /bookings_service
RUN pip install --upgrade pip wheel
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt
FROM python:3.11-slim AS runtime
WORKDIR /bookings_service
RUN useradd -m appuser
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels
COPY . .
USER appuser
EXPOSE 8000
CMD ["uvicorn", "bookings_service.bookings:app", "--host=0.0.0.0", "--port=8000"]