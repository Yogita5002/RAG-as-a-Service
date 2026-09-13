class AppError(Exception):
    status_code = 400

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.message = message
        if status_code is not None:
            self.status_code = status_code


class UnsupportedFileTypeError(AppError):
    status_code = 400


class EmptyDocumentError(AppError):
    status_code = 400


class EmbeddingDimensionError(AppError):
    status_code = 500


class ProviderConfigError(AppError):
    status_code = 500


class DatabaseError(AppError):
    status_code = 503
