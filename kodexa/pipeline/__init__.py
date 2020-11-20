"""
Pipeline
--------

A Pipeline is a way to bring together a Connector, set of steps and then a sink to perform data cleansing, normalization,
analysis and more.
"""
from .pipeline import new_id, PipelineContext, Pipeline, PipelineStatistics, LabelStep
