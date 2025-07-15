# Stage 1: Build React app
FROM node:20-alpine AS frontend-builder

WORKDIR /app/react-test
COPY react-test/package*.json ./
RUN npm install
COPY react-test/ ./
RUN npm run build

# Stage 2: FastAPI backend
FROM python:3.11-slim AS backend

WORKDIR /app
COPY backend/ ./backend/
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy built frontend
RUN mkdir -p backend/app/static
COPY --from=frontend-builder /app/react-test/dist ./backend/app/static/

EXPOSE 8000
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "backend.main:app", "--bind", "0.0.0.0:8000"]

