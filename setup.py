from pathlib import Path
from typing import List

import setuptools

project_root = Path(__file__).parent


def protoc(args: List[str]):
    import pkg_resources
    from grpc_tools import protoc

    command = [
        "grpc_tools.protoc",
        "--proto_path={}".format(
            Path(pkg_resources.resource_filename("grpc_tools", "_proto"))
        ),
    ] + args

    if protoc.main(command) != 0:
        raise Exception("error: {} failed".format(command))


def build_package_grpc_protos(
    protos_paths: List[Path], import_directory_paths: List[Path] = []
):
    protoc(
        [
            "--proto_path={}".format(Path(import_directory_path))
            for import_directory_path in import_directory_paths
        ]
        + ["--grpc_python_out=./tts_service_api"]
        + protos_paths,
    )


def build_package_protos(
    protos_paths: List[Path], import_directory_paths: List[Path] = []
):
    protoc(
        [
            "--proto_path={}".format(Path(import_directory_path))
            for import_directory_path in import_directory_paths
        ]
        + ["--python_out=./tts_service_api"]
        + protos_paths,
    )


def replace_imports_to_relatives(compiled_files: List[Path]):
    for compiled_file in compiled_files:
        with open(compiled_file, "r") as read_file:
            file_content = read_file.read()

        with open(compiled_file, "w") as write_file:
            file_content = file_content.replace(
                "import techmo_tts_pb2 as techmo__tts__pb2",
                "import tts_service_api.techmo_tts_pb2 as techmo__tts__pb2",
            )
            write_file.write(file_content)


build_package_protos(
    protos_paths=[
        "./proto/techmo_tts.proto",
    ],
    import_directory_paths=[
        "./proto",
    ],
)
build_package_grpc_protos(
    protos_paths=[
        "./proto/techmo_tts.proto",
    ],
    import_directory_paths=[
        "./proto",
    ],
)
replace_imports_to_relatives(
    compiled_files=[
        "tts_service_api/techmo_tts_pb2.py",
        "tts_service_api/techmo_tts_pb2_grpc.py",
    ]
)

setuptools.setup( name='techmo-tts-api',
 version='1.0.0-python36+support.001',
 packages=setuptools.find_packages()
 )
