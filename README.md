# TTS Service API (Python)

The collection of gRPC APIs for TTS Service solutions supplied as a Python package.

## Setup

The project setup is not mandatory; it will work as is. The installation of all required packages for preparing the package will take place in a virtual environment.

### Requirements

- [Python](https://www.python.org/) >=3.6.13

## Installation

### Virtual environment

Example:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install --require-virtualenv --upgrade pip
pip install -r requirements.txt
pip install --require-virtualenv .
```

## Usage

Official [documentation](https://docs.techmo.ai/tts/tts_grpc_api.html).

### Import

The package provides a precompiled collection of .proto files. These can be imported directly or through the alias modules.

Example:

- import from an alias module

```python
>>> from tts_service_api import techmo_tts_api as api
>>> hasattr(api, "SynthesizeRequest")
True
```

### Invoke RPC

Invoking RPC simply requires to call a desired method on a [_stub_](https://grpc.io/docs/what-is-grpc/core-concepts/#using-the-api) object dedicated to a specific _service_.

Getting service version:

```python
import grpc
from tts_service_api import techmo_tts_api as api

# This example assumes that the endpoint is an instance
# of techmo.tts.api.v3.TTS service listening on the local 30384 port.
grpc_service_address = "127.0.0.1:30384"

with grpc.insecure_channel(grpc_service_address) as grpc_channel:
    tts_stub = api.TTSStub(grpc_channel)
    request = api.GetServiceVersionRequest()
    response = tts_stub.GetServiceVersion(request, timeout=10)
    print(response)
```

Listing available voices:

```python
import grpc
from tts_service_api import techmo_tts_api as api

# This example assumes that the endpoint is an instance
# of techmo.tts.api.v3.TTS service listening on the local 30384 port.
grpc_service_address = "127.0.0.1:30384"

with grpc.insecure_channel(grpc_service_address) as grpc_channel:
    tts_stub = api.TTSStub(grpc_channel)
    request = api.ListVoicesRequest()
    response = tts_stub.ListVoices(request, timeout=10)
    print(response)

```

Synthesize in streaming mode:

```python

import grpc
import wave
from tts_service_api import techmo_tts_api as api

# This example assumes that the endpoint is an instance
# of techmo.tts.api.v3.TTS service listening on the local 30384 port.
grpc_service_address = "127.0.0.1:30384"
    
synthesis_config = api.SynthesisConfig(
    language_code="pl",
    voice=api.Voice(
        name="masza",
        variant=1,)
)


output_config = api.OutputConfig(audio_encoding=api.AudioEncoding.PCM16, sampling_rate_hz = 22500, max_frame_size=0)


with grpc.insecure_channel(grpc_service_address) as grpc_channel:
    tts_stub = api.TTSStub(grpc_channel)
    request = api.SynthesizeRequest(text="Jestem syntezatorem mowy Techmo, porozmawiajmy!", synthesis_config=synthesis_config, output_config=output_config)
    responses = b''
    for response in tts_stub.SynthesizeStreaming(request):
        responses+=response.audio
        with wave.open('output.wav', 'wb') as wav_file:
            n_channels = 1
            sampwidth = 2 # set properly! variable based on audio_encoding=api.AudioEncoding.PCM16
            framerate = output_config.sampling_rate_hz
            n_frames = len(responses) // sampwidth

            wav_file.setnchannels(n_channels)
            wav_file.setsampwidth(sampwidth)
            wav_file.setframerate(framerate)
            wav_file.setnframes(n_frames)

            wav_file.writeframes(responses)
```

Generated audio will be saved in working directory as `output.wav`.
