# AASist Tools

**AASist Tools**는 중소벤처기업부의 *제조데이터 표준 참조모델 활용 기반 조성 사업*의 일환으로 개발된 Python 기반의 참조모델 지원 도구 모음입니다.  
 AAS(Asset Administration Shell) 표준 참조모델 활용을 위해 다음 두 기능을 별도의 GUI 소프트웨어 형태로 제공합니다:

- **AASist Guidance**는 AAS 참조모델 가이던스 작성 시, 참조모델과 가이던스 서브모델 데이터의 일관성을 확보할 수 있도록 지원하는 도구입니다.

- **AASist Test**는 AAS 참조모델 표준 제약조건 검증 오픈소스 [`aas-test-engines v1.0.2`](https://github.com/admin-shell-io/aas-test-engines)에 기반하여 표준 유효성 검사를 시각적으로 수행할 수 있도록 지원하는 도구입니다.

<br>

# AASist Guidance

> [!NOTE]
> 해당 문서는 현재 작성 중입니다.

<br>

![Image](https://github.com/user-attachments/assets/4ee9b503-77c2-497c-9bc2-71360ed03b51)

<br>
<br>
<br>

# AASist Test

> [!NOTE]
> 해당 문서는 현재 작성 중입니다.

<br>

![Image](https://github.com/user-attachments/assets/05c0b4d9-7cc2-4555-9e2d-cc9df15bca02)

<br>
<br>

# Usage

참조모델 지원 도구의 최신 버전 실행 파일은 [여기](https://github.com/DEV-asdf-516/aasist-tools/releases)에서 다운로드할 수 있습니다.  
다운로드한 `.exe` 파일은 설치 과정 없이 바로 실행 가능합니다.

<br>

# Use CLI build

### Requirements

- Python 3.11+ installed

```
pip install git+https://github.com/DEV-asdf-516/AASist-tools.git

aasist-build <guidance | test | one>
```

- 특정 모듈만 빌드하려면 `guidance`, ` test`, `one` 중 하나를 선택해 실행하세요.

- 별도의 모듈 이름 없이 `aasist-build` 만 실행하는 경우 모든 모듈에 대해 실행파일을 생성합니다.

### Quick start

```
pip install git+https://github.com/DEV-asdf-516/AASist-tools.git

aasist-run <guidance | test | one>
```

- `.exe` 파일 생성 없이 곧바로 GUI 프로그램을 실행합니다.

<br>

# TO DO

참조모델 지원 도구 통합 소프트웨어:

- **AASist One**은 `AASist Guidance`,`AASist Test`를 단일 소프트웨어로 통합한 참조모델 지원 도구입니다.
