FROM python:3.11-slim

# Create user to run the app safely (required by Hugging Face Spaces)
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:${PATH}"

WORKDIR /app

# Copy requirements and install dependencies
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy application files
COPY --chown=user . .

# Expose the port Hugging Face Spaces expects (7860)
EXPOSE 7860

# Start FastAPI server on port 7860
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
