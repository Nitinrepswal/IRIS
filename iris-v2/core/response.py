class IRISResponse:
    def __init__(
        self,
        success,
        content="",
        response_type="text",
        source="system",
        error=None
    ):
        self.success = success
        self.content = content
        self.response_type = response_type
        self.source = source
        self.error = error

    def to_dict(self):
        return {
            "success": self.success,
            "type": self.response_type,
            "content": self.content,
            "source": self.source,
            "error": self.error
        }

    @classmethod
    def success_response(
        cls,
        content,
        source="system",
        response_type="text"
    ):
        return cls(
            success=True,
            content=content,
            response_type=response_type,
            source=source
        )

    @classmethod
    def error_response(
        cls,
        content,
        source="system",
        error=None
    ):
        return cls(
            success=False,
            content=content,
            response_type="error",
            source=source,
            error=error
        )