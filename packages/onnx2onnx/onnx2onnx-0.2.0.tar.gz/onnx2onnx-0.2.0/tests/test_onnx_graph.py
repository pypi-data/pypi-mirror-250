"""
Copyright Wenyi Tang 2024

:Author: Wenyi Tang
:Email: wenyitang@outlook.com

"""
# pylint: disable=missing-function-docstring

import random
import tempfile

import numpy as np
import onnx
import pooch

from onnx2onnx import OnnxGraph
from onnx2onnx.passes import initializer_to_constant


def _pick_random_nodes(graph: OnnxGraph, num_nodes: int = 1):
    indices = list(range(len(graph)))
    random.shuffle(indices)
    node_names = np.array(graph)[indices[:num_nodes]].tolist()
    if len(node_names) == 1:
        return node_names[0]
    return node_names


def test_loading_models(classification_models):
    model_url, hash_value = classification_models
    model = onnx.load_model(pooch.retrieve(model_url, hash_value))
    OnnxGraph(model)


def test_add_remove_node(classification_models):
    model_url, hash_value = classification_models
    model = onnx.load_model(pooch.retrieve(model_url, hash_value))

    graph = OnnxGraph(model)
    node_name = _pick_random_nodes(graph)
    node = graph.nodes[node_name]["pb"]
    graph.remove_onnx_node(node)
    onnx.checker.check_model(graph.model)

    graph.add_onnx_node(node)
    onnx.checker.check_model(graph.model)

    graph.remove_onnx_node(node.name)
    onnx.checker.check_model(graph.model)

    graph.add_onnx_node(node)
    onnx.checker.check_model(graph.model)


def test_make_subgraph(classification_models):
    model_url, hash_value = classification_models
    model = onnx.load_model(pooch.retrieve(model_url, hash_value))

    graph = OnnxGraph(model)
    graph = initializer_to_constant(graph)

    sub_node_names = _pick_random_nodes(graph, len(graph) // 5)
    sub_nodes = [graph.nodes[i]["pb"] for i in sub_node_names]

    sub_from_nodes = graph.onnx_subgraph(sub_nodes)
    sub_from_names = graph.onnx_subgraph(sub_node_names)
    onnx.checker.check_model(sub_from_nodes.model)
    onnx.checker.check_model(sub_from_names.model)


def test_tensor_info(classification_models):
    model_url, hash_value = classification_models
    model = onnx.load_model(pooch.retrieve(model_url, hash_value))

    graph = OnnxGraph(model)
    node_name = _pick_random_nodes(graph)
    node = graph.nodes[node_name]["pb"]
    for input_name in node.input:
        graph.tensor_info(input_name)
    for output_name in node.output:
        graph.tensor_info(output_name)


def test_model_save(classification_models):
    model_url, hash_value = classification_models
    model = onnx.load_model(pooch.retrieve(model_url, hash_value))

    graph = OnnxGraph(model)
    with tempfile.TemporaryDirectory() as tmpdir:
        graph.save(tmpdir + "/model")
        # text format is too slow
        # graph.save(tmpdir + "/model", format="textproto")
        # graph.save(tmpdir + "/model", format="json")
        # graph.save(tmpdir + "/model", format="onnxtxt")
