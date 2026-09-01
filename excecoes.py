class EstoqueException(Exception):
    pass

class EstoqueInsuficienteError(EstoqueException):
    pass

class MaterialNaoEncontradoError(EstoqueException):
    pass