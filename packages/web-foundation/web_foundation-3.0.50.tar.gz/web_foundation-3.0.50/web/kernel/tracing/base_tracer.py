from abc import ABC, abstractmethod


class AppTraceProvider(ABC):
    @abstractmethod
    def set_traces_app(self, app: "WebApp"):
        pass

    @abstractmethod
    def set_traces_rest_transport(self, transport: "RestTransport"):
        pass

    @abstractmethod
    def set_traces_grpc_transport(self, transport: "GrpcTransport"):
        pass
