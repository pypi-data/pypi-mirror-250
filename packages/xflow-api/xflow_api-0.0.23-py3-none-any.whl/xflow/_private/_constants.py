from dataclasses import dataclass


@dataclass
class Actors:
    MANAGER: str = "manager"
    XFLOW_WORKER: str = "xflow_worker"


@dataclass
class RequestPath:
    pipeline_export_component: str = "/api/v0/pipeline/component/export"
    pipeline_get_component: str = "/api/v0/pipeline/component"
    pipeline_exist_component: str = "/api/v0/pipeline/component/exist"
    deploy_export_converter: str = "/api/v0/inference/converter/export"


@dataclass
class PipelineType:
    data_pipeline: str = '1'
    experiment_pipeline: str = '2'
