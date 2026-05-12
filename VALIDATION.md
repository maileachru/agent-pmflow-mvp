# Validation

## Local review

- Package install: passed
- Pytest: passed

## Install output

```text
already satisfied: pygments>=2.7.2 in /opt/pyvenv/lib/python3.13/site-packages (from pytest>=8.0.0->pmflow-codex==0.3.0) (2.20.0)
Requirement already satisfied: Pillow>=3.3.2 in /opt/pyvenv/lib/python3.13/site-packages (from python-pptx>=0.6.23->pmflow-codex==0.3.0) (12.2.0)
Requirement already satisfied: XlsxWriter>=0.5.7 in /opt/pyvenv/lib/python3.13/site-packages (from python-pptx>=0.6.23->pmflow-codex==0.3.0) (3.2.9)
Requirement already satisfied: lxml>=3.1.0 in /opt/pyvenv/lib/python3.13/site-packages (from python-pptx>=0.6.23->pmflow-codex==0.3.0) (6.1.0)
Requirement already satisfied: typing-extensions>=4.9.0 in /opt/pyvenv/lib/python3.13/site-packages (from python-pptx>=0.6.23->pmflow-codex==0.3.0) (4.15.0)
Requirement already satisfied: charset_normalizer<4,>=2 in /opt/pyvenv/lib/python3.13/site-packages (from requests>=2.31.0->pmflow-codex==0.3.0) (3.4.7)
Requirement already satisfied: idna<4,>=2.5 in /opt/pyvenv/lib/python3.13/site-packages (from requests>=2.31.0->pmflow-codex==0.3.0) (3.13)
Requirement already satisfied: urllib3<3,>=1.21.1 in /opt/pyvenv/lib/python3.13/site-packages (from requests>=2.31.0->pmflow-codex==0.3.0) (2.6.3)
Requirement already satisfied: certifi>=2017.4.17 in /opt/pyvenv/lib/python3.13/site-packages (from requests>=2.31.0->pmflow-codex==0.3.0) (2026.4.22)
Building wheels for collected packages: pmflow-codex
  Building editable for pmflow-codex (pyproject.toml): started
  Building editable for pmflow-codex (pyproject.toml): finished with status 'done'
  Created wheel for pmflow-codex: filename=pmflow_codex-0.3.0-0.editable-py3-none-any.whl size=3087 sha256=3c482eb638c2eccbc9332e8d2e95e9b227a794666258992810feee23649001a0
  Stored in directory: /tmp/pip-ephem-wheel-cache-f98u64bo/wheels/9b/5c/13/185e416e9876f19c9252a187a4766192ec920c7eb5db5572e7
Successfully built pmflow-codex
Installing collected packages: pmflow-codex
Successfully installed pmflow-codex-0.3.0
Spreadsheet runtime warmup failed during python startup
Traceback (most recent call last):
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/patches/warm_spreadsheet_runtime_on_startup.py", line 26, in warm_spreadsheet_runtime_on_startup
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/spreadsheet_warmup.py", line 785, in warm_spreadsheet_runtime
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/spreadsheet_warmup.py", line 720, in _warm_feature_flows
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/spreadsheet_warmup.py", line 704, in _warm_collaboration_flows
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/generated/interface/models.py", line 48821, in hydrate_crdt_from_proto
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/rpc/remote.py", line 747, in __call__
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/rpc/client.py", line 150, in call
artifact_tool.rpc.client.RemoteError: hydrateCrdtFromProto requires an empty collaborative document.

```

## Test output

```text
[32m.[0m[32m.[0m[32m.[0m[32m                                                                      [100%][0m
[32m[32m[1m3 passed[0m[32m in 0.44s[0m[0m
Spreadsheet runtime warmup failed during python startup
Traceback (most recent call last):
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/patches/warm_spreadsheet_runtime_on_startup.py", line 26, in warm_spreadsheet_runtime_on_startup
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/spreadsheet_warmup.py", line 785, in warm_spreadsheet_runtime
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/spreadsheet_warmup.py", line 720, in _warm_feature_flows
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/spreadsheet_warmup.py", line 704, in _warm_collaboration_flows
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/generated/interface/models.py", line 48821, in hydrate_crdt_from_proto
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/rpc/remote.py", line 747, in __call__
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/rpc/client.py", line 150, in call
artifact_tool.rpc.client.RemoteError: hydrateCrdtFromProto requires an empty collaborative document.

```
