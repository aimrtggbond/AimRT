#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2023, AgiBot Inc.
# All rights reserved.

import sys

from google.protobuf.compiler import plugin_pb2 as plugin
from google.protobuf.compiler.plugin_pb2 import \
    CodeGeneratorRequest as CodeGeneratorRequest
from google.protobuf.compiler.plugin_pb2 import \
    CodeGeneratorResponse as CodeGeneratorResponse
from google.protobuf.descriptor_pb2 import \
    FileDescriptorProto as FileDescriptorProto


class AimRTCodeGenerator:
    t_pyfile: str = r"""# This file was generated by protoc-gen-aimrt_rpc which is a self-defined pb compiler plugin, do not edit it!!!

from typing import overload

import aimrt_py
import google.protobuf
import {{py_package_name}}
{{pyfile_import_dependency_py_package}}

{{for service begin}}
class {{service_name}}(aimrt_py.ServiceBase):
    def __init__(self):
        super().__init__("pb", "{{package_name}}.{{service_name}}")

{{for method begin}}
        # {{rpc_func_name}}
        {{simple_rpc_req_name}}_aimrt_ts = aimrt_py.TypeSupport()
        {{simple_rpc_req_name}}_aimrt_ts.SetTypeName("pb:" + {{full_rpc_req_py_name}}.DESCRIPTOR.full_name)
        {{simple_rpc_req_name}}_aimrt_ts.SetSerializationTypesSupportedList(["pb", "json"])

        {{simple_rpc_rsp_name}}_aimrt_ts = aimrt_py.TypeSupport()
        {{simple_rpc_rsp_name}}_aimrt_ts.SetTypeName("pb:" + {{full_rpc_rsp_py_name}}.DESCRIPTOR.full_name)
        {{simple_rpc_rsp_name}}_aimrt_ts.SetSerializationTypesSupportedList(["pb", "json"])

        def {{rpc_func_name}}AdapterFunc(ctx_ref, req_str):
            serialization_type = ctx_ref.GetSerializationType()

            try:
                req = {{full_rpc_req_py_name}}()
                if(serialization_type == "pb"):
                    req.ParseFromString(req_str)
                elif(serialization_type == "json"):
                    google.protobuf.json_format.Parse(req_str, req)
                else:
                    return (aimrt_py.RpcStatus(aimrt_py.RpcStatusRetCode.SVR_INVALID_SERIALIZATION_TYPE), "")
            except Exception as e:
                return (aimrt_py.RpcStatus(aimrt_py.RpcStatusRetCode.SVR_DESERIALIZATION_FAILED), "")

            try:
                st, rsp = self.{{rpc_func_name}}(ctx_ref, req)
            except Exception as e:
                return (aimrt_py.RpcStatus(aimrt_py.RpcStatusRetCode.SVR_HANDLE_FAILED), "")

            try:
                rsp_str = ""
                if(serialization_type == "pb"):
                    rsp_str = rsp.SerializeToString()
                elif(serialization_type == "json"):
                    rsp_str = google.protobuf.json_format.MessageToJson(rsp)
                else:
                    return (aimrt_py.RpcStatus(aimrt_py.RpcStatusRetCode.SVR_INVALID_SERIALIZATION_TYPE), "")
            except Exception as e:
                return (aimrt_py.RpcStatus(aimrt_py.RpcStatusRetCode.SVR_SERIALIZATION_FAILED), "")

            return (st, rsp_str)

        self.RegisterServiceFunc("{{rpc_func_name}}",
                                 {{simple_rpc_req_name}}_aimrt_ts, {{simple_rpc_rsp_name}}_aimrt_ts, {{rpc_func_name}}AdapterFunc)

{{method end}}
{{for method begin}}
    def {{rpc_func_name}}(self, ctx_ref, req):
        return (aimrt_py.RpcStatus(aimrt_py.RpcStatusRetCode.SVR_NOT_IMPLEMENTED), {{full_rpc_rsp_py_name}}())

{{method end}}
{{service end}}

{{for service begin}}
class {{service_name}}Proxy(aimrt_py.ProxyBase):
    def __init__(self, rpc_handle_ref=aimrt_py.RpcHandleRef()):
        super().__init__(rpc_handle_ref, "pb", "{{package_name}}.{{service_name}}")
        self.rpc_handle_ref = rpc_handle_ref

{{for method begin}}
    @overload
    def {{rpc_func_name}}(
        self, req: {{full_rpc_req_py_name}}
    ) -> tuple[aimrt_py.RpcStatus, {{full_rpc_rsp_py_name}}]: ...

    @overload
    def {{rpc_func_name}}(
        self, ctx_ref: aimrt_py.RpcContext, req: {{full_rpc_req_py_name}}
    ) -> tuple[aimrt_py.RpcStatus, {{full_rpc_rsp_py_name}}]: ...

    @overload
    def {{rpc_func_name}}(
        self, ctx_ref: aimrt_py.RpcContextRef, req: {{full_rpc_req_py_name}}
    ) -> tuple[aimrt_py.RpcStatus, {{full_rpc_rsp_py_name}}]: ...

    def {{rpc_func_name}}(self, *args):
        if len(args) == 1:
            ctx = super().NewContextSharedPtr()
            req = args[0]
        elif len(args) == 2:
            ctx = args[0]
            req = args[1]
        else:
            raise TypeError(f"{{rpc_func_name}} expects 1 or 2 arguments, got {len(args)}")

        if isinstance(ctx, aimrt_py.RpcContext):
            ctx_ref = aimrt_py.RpcContextRef(ctx)
        elif isinstance(ctx, aimrt_py.RpcContextRef):
            ctx_ref = ctx
        else:
            raise TypeError(f"ctx must be 'aimrt_py.RpcContext' or 'aimrt_py.RpcContextRef', got {type(ctx)}")

        if ctx_ref:
            if ctx_ref.GetSerializationType() == "":
                ctx_ref.SetSerializationType("pb")
        else:
            real_ctx = aimrt_py.RpcContext()
            ctx_ref = aimrt_py.RpcContextRef(real_ctx)
            ctx_ref.SetSerializationType("pb")

        serialization_type = ctx_ref.GetSerializationType()

        rsp = {{full_rpc_rsp_py_name}}()

        try:
            req_str = ""
            if serialization_type == "pb":
                req_str = req.SerializeToString()
            elif serialization_type == "json":
                req_str = google.protobuf.json_format.MessageToJson(req)
            else:
                return (aimrt_py.RpcStatus(aimrt_py.RpcStatusRetCode.CLI_INVALID_SERIALIZATION_TYPE), rsp)
        except Exception as e:
            return (aimrt_py.RpcStatus(aimrt_py.RpcStatusRetCode.CLI_SERIALIZATION_FAILED), rsp)

        status, rsp_str = self.rpc_handle_ref.Invoke("pb:/{{package_name}}.{{service_name}}/{{rpc_func_name}}",
                                                     ctx_ref, req_str)

        try:
            if serialization_type == "pb":
                rsp.ParseFromString(rsp_str)
            elif serialization_type == "json":
                google.protobuf.json_format.Parse(rsp_str, rsp)
            else:
                return (aimrt_py.RpcStatus(aimrt_py.RpcStatusRetCode.CLI_INVALID_SERIALIZATION_TYPE), rsp)
        except Exception as e:
            return (aimrt_py.RpcStatus(aimrt_py.RpcStatusRetCode.CLI_DESERIALIZATION_FAILED), rsp)

        return (status, rsp)

{{method end}}

    @staticmethod
    def RegisterClientFunc(rpc_handle):
{{for method begin}}
        # {{rpc_func_name}}
        {{simple_rpc_req_name}}_aimrt_ts = aimrt_py.TypeSupport()
        {{simple_rpc_req_name}}_aimrt_ts.SetTypeName("pb:" + {{full_rpc_req_py_name}}.DESCRIPTOR.full_name)
        {{simple_rpc_req_name}}_aimrt_ts.SetSerializationTypesSupportedList(["pb", "json"])

        {{simple_rpc_rsp_name}}_aimrt_ts = aimrt_py.TypeSupport()
        {{simple_rpc_rsp_name}}_aimrt_ts.SetTypeName("pb:" + {{full_rpc_rsp_py_name}}.DESCRIPTOR.full_name)
        {{simple_rpc_rsp_name}}_aimrt_ts.SetSerializationTypesSupportedList(["pb", "json"])

        ret = rpc_handle.RegisterClientFunc("pb:/{{package_name}}.{{service_name}}/{{rpc_func_name}}",
                                            {{simple_rpc_req_name}}_aimrt_ts, {{simple_rpc_rsp_name}}_aimrt_ts)
        if(not ret):
            return False

{{method end}}
        return True
{{service end}}
"""

    class MethodNode:
        def __init__(self):
            self.kv = {}

    class ServiceNode:
        def __init__(self):
            self.kv = {}
            self.method_vec = []

    class PackageNode:
        def __init__(self):
            self.kv = {}
            self.service_vec = []

    @staticmethod
    def gen_method_code(temp, method_node) -> str:
        result = temp
        for key, value in method_node.kv.items():
            result = result.replace(key, value)
        return result

    @staticmethod
    def gen_service_code(temp, service_node) -> str:
        result = temp

        for key, value in service_node.kv.items():
            result = result.replace(key, value)

        method_begin_flag = "{{for method begin}}\n"
        method_end_flag = "{{method end}}\n"

        cur_pos = 0
        while True:
            begin_pos = result.find(method_begin_flag, cur_pos)
            if begin_pos == -1:
                break
            end_pos = result.find(method_end_flag, begin_pos + len(method_begin_flag))
            if end_pos == -1:
                break

            cur_temp = result[begin_pos + len(method_begin_flag):end_pos]
            cur_result = ""
            for node in service_node.method_vec:
                cur_result += AimRTCodeGenerator.gen_method_code(cur_temp, node)

            result = result[:begin_pos] + cur_result + result[end_pos + len(method_end_flag):]
            cur_pos = begin_pos + len(cur_result)

        return result

    @staticmethod
    def gen_package_code(temp, package_node) -> str:
        result = temp

        for key, value in package_node.kv.items():
            result = result.replace(key, value)

        service_begin_flag = "{{for service begin}}\n"
        service_end_flag = "{{service end}}\n"

        cur_pos = 0
        while True:
            begin_pos = result.find(service_begin_flag, cur_pos)
            if begin_pos == -1:
                break
            end_pos = result.find(service_end_flag, begin_pos + len(service_begin_flag))
            if end_pos == -1:
                break

            cur_temp = result[begin_pos + len(service_begin_flag):end_pos]
            cur_result = ""
            for node in package_node.service_vec:
                cur_result += AimRTCodeGenerator.gen_service_code(cur_temp, node)

            result = result[:begin_pos] + cur_result + result[end_pos + len(service_end_flag):]
            cur_pos = begin_pos + len(cur_result)

        return result

    @staticmethod
    def gen_simple_name_str(ns: str) -> str:
        return ns.split(".")[-1]

    def generate(self, request: CodeGeneratorRequest) -> CodeGeneratorResponse:
        """Generate code for the given request"""

        # create message type py name dict
        message_type_py_name_dict = {}
        for proto_file in request.proto_file:
            file_name: str = proto_file.name
            package_name: str = proto_file.package
            py_package_name: str = file_name.replace('.proto', '_pb2').replace("/", ".")

            for message_type in proto_file.message_type:
                message_type_full_name = "." + package_name + "." + message_type.name
                message_type_py_name = py_package_name + "." + message_type.name
                message_type_py_name_dict[message_type_full_name] = message_type_py_name

        # Generate code for each file
        response: CodeGeneratorResponse = CodeGeneratorResponse()
        for proto_file in request.proto_file:
            if len(proto_file.service) == 0:
                continue

            file_name: str = proto_file.name
            package_name: str = proto_file.package
            py_package_name: str = file_name.replace('.proto', '_pb2').replace("/", ".")
            aimrt_rpc_py_file_name: str = file_name.replace('.proto', '_aimrt_rpc_pb2.py')

            pyfile_import_dependency_py_package: str = ""
            for dependency_proto_file in proto_file.dependency:
                import_dependency_py_package: str = "import " + \
                    dependency_proto_file.replace('.proto', '_pb2').replace("/", ".")
                pyfile_import_dependency_py_package = pyfile_import_dependency_py_package + import_dependency_py_package + "\n"

            package_node = AimRTCodeGenerator.PackageNode()
            package_node.kv["{{py_package_name}}"] = py_package_name
            package_node.kv["{{package_name}}"] = package_name
            package_node.kv["{{pyfile_import_dependency_py_package}}"] = pyfile_import_dependency_py_package

            for ii in range(0, len(proto_file.service)):
                service = proto_file.service[ii]

                service_node = AimRTCodeGenerator.ServiceNode()
                service_node.kv["{{service_name}}"] = service.name

                for jj in range(0, len(service.method)):
                    method = service.method[jj]

                    method_node = AimRTCodeGenerator.MethodNode()

                    method_node.kv["{{rpc_func_name}}"] = method.name
                    method_node.kv["{{simple_rpc_req_name}}"] = self.gen_simple_name_str(method.input_type)
                    method_node.kv["{{simple_rpc_rsp_name}}"] = self.gen_simple_name_str(method.output_type)
                    method_node.kv["{{full_rpc_req_py_name}}"] = message_type_py_name_dict[method.input_type]
                    method_node.kv["{{full_rpc_rsp_py_name}}"] = message_type_py_name_dict[method.output_type]

                    service_node.method_vec.append(method_node)

                package_node.service_vec.append(service_node)

            # pyfile
            pyfile: CodeGeneratorResponse.File = CodeGeneratorResponse.File()
            pyfile.name = aimrt_rpc_py_file_name
            pyfile.content = AimRTCodeGenerator.gen_package_code(self.t_pyfile, package_node)
            response.file.append(pyfile)

        return response


def generate():
    request: CodeGeneratorRequest = CodeGeneratorRequest.FromString(sys.stdin.buffer.read())

    aimrt_code_generator: AimRTCodeGenerator = AimRTCodeGenerator()

    response: CodeGeneratorResponse = aimrt_code_generator.generate(request)

    sys.stdout.buffer.write(response.SerializeToString())


if __name__ == "__main__":
    generate()
