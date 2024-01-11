from promptflow.exceptions import ErrorTarget, SystemErrorException, ValidationException


class ToolValidationError(ValidationException):
    def __init__(
        self,
        target: ErrorTarget = ErrorTarget.EXECUTOR,
        **kwargs,
    ):
        super().__init__(
            target=target,
            **kwargs,
        )


class ToolLoadError(ToolValidationError):
    pass


class InvalidNodeRequest(ValidationException):
    def __init__(
        self,
        target: ErrorTarget = ErrorTarget.EXECUTOR,
        **kwargs,
    ):
        super().__init__(
            target=target,
            **kwargs,
        )


class ToolNotFoundInFlow(InvalidNodeRequest):
    pass


class ToolTypeNotSupported(ToolValidationError):
    pass


class ToolNotFound(ValidationException):
    pass


class InvalidRequest(ValidationException):
    def __init__(
        self,
        target: ErrorTarget = ErrorTarget.EXECUTOR,
        **kwargs,
    ):
        super().__init__(
            target=target,
            **kwargs,
        )


class ConnectionNotFound(InvalidRequest):
    pass


class InvalidFlowRequest(ValidationException):
    def __init__(
        self,
        target: ErrorTarget = ErrorTarget.EXECUTOR,
        **kwargs,
    ):
        super().__init__(
            target=target,
            **kwargs,
        )


class InvalidConnectionType(InvalidFlowRequest):
    pass


class NodeInputValidationError(InvalidFlowRequest):
    pass


class NodeOfVariantNotFound(InvalidFlowRequest):
    pass


class ToolOfVariantNotFound(InvalidFlowRequest):
    pass


class UnexpectedValueError(SystemErrorException):
    def __init__(self, **kwargs):
        super().__init__(target=ErrorTarget.EXECUTOR, **kwargs)


class ValueTypeUnresolved(ValidationException):
    pass
