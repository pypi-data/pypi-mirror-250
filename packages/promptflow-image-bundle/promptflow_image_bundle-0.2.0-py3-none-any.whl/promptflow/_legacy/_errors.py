from promptflow.exceptions import ErrorTarget, SystemErrorException, ValidationException


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


class NodeNotFoundByName(InvalidNodeRequest):
    pass


class SingleNodeModeNotSupportedForReduce(InvalidNodeRequest):
    pass


class ToolNotFoundInFlow(InvalidNodeRequest):
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


class EmptyInputError(InvalidRequest):
    pass


class InputConvertTypeError(InvalidNodeRequest):
    pass


class ToolLoadError(ToolValidationError):
    pass


class ToolTypeNotSupported(ToolValidationError):
    pass


class ToolNotFound(ValidationException):
    pass


class UnexpectedValueError(SystemErrorException):
    def __init__(self, **kwargs):
        super().__init__(target=ErrorTarget.EXECUTOR, **kwargs)


class InvalidRunMode(InvalidRequest):
    pass


class RequestTypeNotSupported(InvalidRequest):
    pass


class ConnectionNotFound(InvalidRequest):
    pass


class EvaluationFlowNotSupported(InvalidRequest):
    pass


class InvalidBulkTestRequest(ValidationException):
    def __init__(
        self,
        target: ErrorTarget = ErrorTarget.EXECUTOR,
        **kwargs,
    ):
        super().__init__(
            target=target,
            **kwargs,
        )


class BaselineVariantIdNotFound(InvalidBulkTestRequest):
    pass


class BaselineVariantInVariants(InvalidBulkTestRequest):
    pass


class BulkTestIdNotFound(InvalidBulkTestRequest):
    pass


class InvalidEvalFlowRequest(ValidationException):
    def __init__(
        self,
        target: ErrorTarget = ErrorTarget.EXECUTOR,
        **kwargs,
    ):
        super().__init__(
            target=target,
            **kwargs,
        )


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


class DuplicateVariantId(InvalidEvalFlowRequest):
    pass


class EvalMappingSourceNotFound(InvalidEvalFlowRequest):
    pass


class EvaluationFlowRunIdNotFound(InvalidBulkTestRequest):
    pass


class InvalidEvalFlowRequest(ValidationException):
    def __init__(
        self,
        target: ErrorTarget = ErrorTarget.EXECUTOR,
        **kwargs,
    ):
        super().__init__(
            target=target,
            **kwargs,
        )


class MissingBulkInputs(InvalidEvalFlowRequest):
    pass


class NoValidOutputLine(InvalidEvalFlowRequest):
    pass


class NumberOfInputsAndOutputsNotEqual(InvalidEvalFlowRequest):
    pass


class VariantIdNotFound(InvalidEvalFlowRequest):
    pass


class VariantCountNotMatchWithRunCount(InvalidBulkTestRequest):
    pass


class InvalidConnectionType(InvalidFlowRequest):
    pass


class NodeInputValidationError(InvalidFlowRequest):
    pass


class NodeOfVariantNotFound(InvalidFlowRequest):
    pass


class ToolOfVariantNotFound(InvalidFlowRequest):
    pass


class ValueTypeUnresolved(ValidationException):
    pass


class InputNotFound(InvalidFlowRequest):
    pass
