import loguru
from opentelemetry import metrics
from opentelemetry import trace, context
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.propagate import extract
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.semconv.trace import SpanAttributes
from pydantic import BaseModel

from web.kernel.tracing.base_tracer import AppTraceProvider
from web.kernel.types import ConfAble, AppNameAble, SignalType
from web.trend.rest.transport import RestTransport

SANIC_CTX_SPAN_KEY = "span"


class OpenTelemetryConf(BaseModel):
    enable_trace: bool
    enable_tortoise_trace: bool = False
    trace_entrypoint: str
    trace_endpoint: str = 'v1/traces'
    enable_metrics: bool | None
    metrics_entrypoint: str | None
    metrics_endpoint: str = 'v1/metrics'


class OpenTelemetryAppTracer(AppTraceProvider, AppNameAble, ConfAble[OpenTelemetryConf]):
    resource: Resource
    tracer_provider: TracerProvider
    tracer: trace.Tracer

    async def init(self, app: "WebApp"):
        self.resource = Resource(attributes={
            SERVICE_NAME: self.app_name
        })
        self.tracer_provider = TracerProvider(resource=self.resource)
        if self.conf.enable_tortoise_trace:
            try:
                from opentelemetry.instrumentation.tortoiseorm import TortoiseORMInstrumentor
                TortoiseORMInstrumentor().instrument(tracer_provider=self.tracer_provider)
            except ImportError:
                loguru.logger.warning(
                    "Can't import opentelemetry.instrumentation.tortoiseorm. For get tortoise traces use pip install web-foundation[telemetry_tortoise]")
                raise RuntimeError("opentelemetry.instrumentation.tortoiseorm is not installed on your system. Try pip install web-foundation[telemetry_tortoise]")

    async def init_rest(self, transport: RestTransport):
        if not self.conf.enable_trace and not self.conf.enable_metrics:
            return

        if self.conf.enable_trace:
            processor = BatchSpanProcessor(
                OTLPSpanExporter(endpoint=f"{self.conf.trace_entrypoint}/{self.conf.trace_endpoint}"))
            self.tracer_provider.add_span_processor(processor)
            trace.set_tracer_provider(self.tracer_provider)
            self.tracer = trace.get_tracer(transport.channel.name)

            @transport.sanic.on_request
            def before_request(request):
                context.attach(extract(request.headers))
                span = self.tracer.start_span(
                    "sanic.request",
                    kind=trace.SpanKind.SERVER,
                )
                activation = trace.use_span(span, end_on_exit=True)
                activation.__enter__()

                span.set_attribute(SpanAttributes.HTTP_METHOD, request.method)
                span.set_attribute(SpanAttributes.HTTP_ROUTE, request.path)
                span.set_attribute(SpanAttributes.CLIENT_ADDRESS, request.ip)

                request.ctx.tracing = {SANIC_CTX_SPAN_KEY: span, 'activation': activation}

            @transport.sanic.on_response
            def on_after_request(req, res):
                if hasattr(req.ctx, "tracing"):
                    req.ctx.tracing[SANIC_CTX_SPAN_KEY].set_attribute(SpanAttributes.HTTP_STATUS_CODE, res.status)
                    req.ctx.tracing['activation'].__exit__(None, None, None)

        if self.conf.enable_metrics:
            reader = PeriodicExportingMetricReader(
                OTLPMetricExporter(endpoint=f"{self.conf.metrics_entrypoint}/{self.conf.metrics_endpoint}")
            )
            meter_provider = MeterProvider(resource=self.resource, metric_readers=[reader])
            metrics.set_meter_provider(meter_provider)

    def set_traces_app(self, app: "WebApp"):
        app.on_signal(SignalType.BEFORE_APP_RUN, self.init)

    def set_traces_rest_transport(self, transport: "RestTransport"):
        transport.on_signal(SignalType.BEFORE_TRANSPORT_WORK, self.init_rest)

    def set_traces_grpc_transport(self, transport: "GrpcTransport"):  # todo
        pass
