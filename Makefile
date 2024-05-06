build:
	docker build -t image-api-service .

dev: build
	docker run -p 8000:8000 -v $(PWD)/app:/app --name image-api-service --rm image-api-service

prod: build
	docker run -p 8000:8000 --name image-api-service --rm image-api-service fastapi run
