"""
Copyright 2024 Intel Corporation

:Author: Wenyi Tang
:Email: wenyi.tang@intel.com

"""
# pylint: disable=missing-function-docstring

import numpy as np
import onnx
from onnx.helper import (
    make_graph,
    make_model,
    make_node,
    make_operatorsetid,
    make_tensor_type_proto,
    make_value_info,
)
from onnx.numpy_helper import from_array, to_array

from onnx2onnx import OnnxGraph, PassManager


def _build_test_graph1():
    conv0 = make_node("Conv", inputs=["a", "w0"], outputs=["c"], group=4, name="conv0")
    conv1 = make_node("Conv", inputs=["c", "w1"], outputs=["d"], group=1, name="conv1")
    graph = make_graph(
        [conv0, conv1],
        name="graph",
        inputs=[],
        outputs=[make_value_info("d", make_tensor_type_proto(1, None))],
        initializer=[
            from_array(np.random.normal(size=[1, 4, 128, 127]).astype("float32"), "a"),
            from_array(np.random.normal(size=[4, 1, 3, 3]).astype("float32"), "w0"),
            from_array(np.random.normal(size=[8, 4, 3, 3]).astype("float32"), "w1"),
        ],
    )
    model = make_model(graph, opset_imports=[make_operatorsetid("", 19)])
    return model


def _build_test_graph2():
    shape = make_node("Shape", inputs=["a"], outputs=["b"], name="shape")
    add = make_node("Add", inputs=["b", "x"], outputs=["c"], name="add")
    graph = make_graph(
        [shape, add],
        name="graph",
        inputs=[make_value_info("a", make_tensor_type_proto(1, [1, 32]))],
        outputs=[
            make_value_info("c", make_tensor_type_proto(onnx.TensorProto.INT64, [2]))
        ],
        initializer=[
            from_array(np.array([32, 1]).astype("int64"), "x"),
        ],
    )
    model = make_model(graph, opset_imports=[make_operatorsetid("", 19)])
    return model


def _build_test_graph3():
    shape = make_node("Shape", inputs=["a"], outputs=["b"], name="shape")
    add = make_node("Add", inputs=["b", "x"], outputs=["c"], name="add")
    graph = make_graph(
        [shape, add],
        name="graph",
        inputs=[make_value_info("a", make_tensor_type_proto(1, ["N", 32]))],
        outputs=[
            make_value_info("c", make_tensor_type_proto(onnx.TensorProto.INT64, [2]))
        ],
        initializer=[
            from_array(np.array([32, 1]).astype("int64"), "x"),
        ],
    )
    model = make_model(graph, opset_imports=[make_operatorsetid("", 19)])
    return model


def test_fold_constant():
    graph = OnnxGraph(_build_test_graph1())
    passes = PassManager(["initializer_to_constant", "fold_constant"])
    folded_graph = passes.optimize(graph)
    assert len(folded_graph) == 1


def test_fold_shape():
    graph = OnnxGraph(_build_test_graph2())
    passes = PassManager(
        ["initializer_to_constant", "shape_to_constant", "fold_constant"]
    )
    folded_graph = passes.optimize(graph)
    assert len(folded_graph) == 1
    for node in folded_graph.nodes.values():
        assert np.all(to_array(node["pb"].attribute[0].t) == [33, 33])


def test_fold_dynamic_shape():
    graph = OnnxGraph(_build_test_graph3())
    passes = PassManager(
        ["initializer_to_constant", "shape_to_constant", "fold_constant"]
    )
    folded_graph = passes.optimize(graph)
    assert len(folded_graph) == 3
