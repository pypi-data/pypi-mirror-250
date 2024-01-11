## Core-SDK (Dalpha-ai 라이브러리) 

### Introduction 
- 달파 AI 팀 내부에서 개발한 라이브러리로, 자주 사용되는 AI 모델들을 빠르고 편리하게 사용하는 목적으로 만들어진 python library, package입니다.
- 현재는 Classifier Train & Inference / Zero-Shot Classifier를 지원하며, 추후에는 Clip training / Vector similarity search / Detector 등등을 지원할 예정입니다.

### Update
****v0.2.5****
- map_location error 수정
- train dataloader shuffle 추가
- find_unused_parameter true 설정 (roberta류 모델)
- electra, roberta type 지원 & electra Head classifier 추가
- negative sample 지원 (Label -1일 때)
- requirements.txt 느슨하게
- pipeline inference 시 only_backbone=True면 backbone embedding만 output.
- train_config.json utf-8 인코딩 및 가독성 개선 

### Installation

```
#### GPU 
pip install dalpha-ai
#### CPU
pip install dalpha-ai-cpu
```

### QuickStart

`` examples/HowToStart.ipynb ``
