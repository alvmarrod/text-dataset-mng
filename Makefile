
export PYTHON_BINARY=/usr/bin/python3.11
export DATA=data

export IMAGE_NAME=text-dataset-mng
export IMAGE_VERSION=`cat version.txt`

export CONTAINER_NAME=text-dataset-mng-service
export EXTERNAL_SERVICE_PORT=9000

export DATA_MOUNTPOINT=`pwd`/data

prepare-env:
	@echo "Preparing environment..."
	@if [ -d ".venv" ] && [ -f ".venv/bin/activate" ]; then \
		echo "Virtual environment already exists and is valid. Skipping creation."; \
	else \
		echo "Creating or repairing virtual environment..."; \
		echo "Checking Python version..."; \
		if ! command -v ${PYTHON_BINARY} >/dev/null 2>&1; then \
			echo "Error: ${PYTHON_BINARY} not found. Please install Python or update PYTHON_BINARY."; \
			exit 1; \
		fi; \
		if ! ${PYTHON_BINARY} -c "import sys; assert sys.version_info >= (3, 8), 'Python 3.8 or higher is required.'"; then \
			echo "Error: Incompatible Python version. Python 3.8 or higher is required."; \
			exit 1; \
		fi; \
		${PYTHON_BINARY} -m venv .venv; \
	fi

install-deps: prepare-env
	@echo "Activating virtual environment and installing dependencies..."
	@bash -c ". .venv/bin/activate && \
		echo 'Upgrading pip...' && \
		pip install -q --upgrade pip && \
		echo 'Installing dependencies...' && \
		pip install -q -r requirements.txt"

run: install-deps
	@echo "Running the project..."
	@echo "Checking if the database is already initialized..."
	@. .venv/bin/activate && python app.py

build-docker:
	@echo "Building Docker image..."
	@docker build -t ${IMAGE_NAME}:${IMAGE_VERSION} .

run-docker:
	@echo "Running Docker container..."
	@docker run -d --restart=unless-stopped --name ${CONTAINER_NAME} -v ${DATA_MOUNTPOINT}:/app/data -p ${EXTERNAL_SERVICE_PORT}:5000 ${IMAGE_NAME}:${IMAGE_VERSION}
