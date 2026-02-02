# CLAUDE.md

이 파일은 이 저장소에서 작업할 때 Claude Code (claude.ai/code)에 대한 가이드를 제공합니다.

## 프로젝트 개요

서버 메트릭을 실시간으로 모니터링하고 수집하도록 설계된 **시스템 리소스 메트릭 수집 시스템**입니다. 이 시스템은 5가지 핵심 메트릭 카테고리를 수집합니다: CPU, 메모리, 디스크 I/O, 네트워크 대역폭, 디스크 사용률.

**핵심 성능 목표:**
- 수집 주기: 10초 이하
- 시스템 오버헤드: CPU 5% 이하, 메모리 100MB 이하
- 데이터 손실률: 0.1% 이하
- 데이터 보존 기간: 최소 30일

## 아키텍처

```
[서버] → [수집 에이전트] → [메트릭 저장소] → [시각화 대시보드]
                                   ↓
                              [알림 시스템]
```

## 기술 스택

**선택된 기술 스택:**
- **에이전트**: Python 3.9+ with psutil
  - 간단하고 빠른 프로토타이핑
  - psutil을 통한 크로스 플랫폼 시스템 메트릭 수집
  - 풍부한 라이브러리 생태계
- **저장소**: Prometheus
  - 시계열 데이터에 특화된 TSDB
  - Pull 기반 메트릭 수집
  - PromQL을 통한 강력한 쿼리 기능
  - 자동 데이터 압축 및 보존 정책
- **시각화**: Grafana
  - Prometheus와 네이티브 통합
  - 풍부한 시각화 옵션 및 대시보드 템플릿
  - 알림 규칙 및 대시보드 공유 기능
- **알림**: Prometheus Alertmanager
  - Prometheus와 완벽한 통합
  - 알림 라우팅, 그룹화, 중복 제거
  - 여러 채널 지원 (이메일, Slack, PagerDuty, 웹훅)

**추가 의존성:**
- **Python 라이브러리**:
  - `psutil` - 시스템 및 프로세스 메트릭 수집
  - `prometheus-client` - Prometheus exporter
  - `pyyaml` - 설정 파일 파싱
  - `requests` - HTTP 클라이언트
- **인프라**:
  - Docker & Docker Compose - 컨테이너화 및 로컬 개발
  - Systemd - 프로덕션 환경 서비스 관리

## 디렉토리 구조

```
new_test/
├── src/
│   ├── collectors/       # 메트릭 수집 모듈 (CPU, 메모리, 디스크, 네트워크)
│   ├── storage/          # 저장소 백엔드 (Prometheus, InfluxDB 커넥터)
│   ├── api/              # 메트릭 조회용 REST API
│   ├── alerting/         # 알림 규칙 엔진 및 알림 핸들러
│   └── utils/            # 공통 유틸리티 및 헬퍼
├── tests/
│   ├── unit/             # 각 수집기별 단위 테스트
│   └── integration/      # 전체 플로우 테스트 (수집 → 저장 → 조회)
├── config/               # 설정 파일 (임계값, 주기, 엔드포인트)
├── scripts/              # 배포 및 유지보수 스크립트
├── dashboards/           # Grafana/Kibana 대시보드 정의
└── docs/                 # 문서 및 PRD
    └── README.md         # 제품 요구사항 정의서
```

## 메트릭 명세

### 1. CPU 메트릭 (9개 메트릭, 10초 주기)
- `cpu_usage_percent` - 전체 CPU 사용률
- `cpu_usage_per_core` - 코어별 CPU 사용률
- `cpu_user_time`, `cpu_system_time`, `cpu_idle_time`, `cpu_iowait_time`
- `load_average_1m`, `load_average_5m`, `load_average_15m`

**알림 기준:**
- Warning: CPU ≥80% 5분 지속
- Critical: CPU ≥95% 1분 지속

### 2. 메모리 메트릭 (11개 메트릭, 10초 주기)
- `memory_total`, `memory_used`, `memory_free`, `memory_available`
- `memory_usage_percent`, `memory_cached`, `memory_buffers`
- `swap_total`, `swap_used`, `swap_free`, `swap_usage_percent`

**알림 기준:**
- Warning: 메모리 ≥85%
- Critical: 메모리 ≥95% 또는 OOM Killer 발동

### 3. 디스크 I/O 메트릭 (9개 메트릭, 10초 주기)
- `disk_read_bytes`, `disk_write_bytes` (bytes/s)
- `disk_read_ops`, `disk_write_ops` (IOPS)
- `disk_read_time`, `disk_write_time`, `disk_await_time` (ms)
- `disk_io_util_percent`, `disk_queue_length`

**알림 기준:**
- Warning: I/O 사용률 ≥80% 5분 지속 또는 대기 시간 ≥100ms
- Critical: 대기 시간 ≥500ms

### 4. 네트워크 메트릭 (10개 메트릭, 10초 주기)
- `network_bytes_sent`, `network_bytes_recv` (bytes/s)
- `network_packets_sent`, `network_packets_recv` (packets/s)
- `network_errors_in`, `network_errors_out`, `network_drops_in`, `network_drops_out`
- `network_bandwidth_usage` (%), `network_connections`

**알림 기준:**
- Warning: 대역폭 ≥80% 또는 패킷 드롭률 ≥1%
- Critical: 대역폭 ≥95%

### 5. 디스크 사용률 메트릭 (8개 메트릭, 60초 주기)
- `disk_total`, `disk_used`, `disk_free`, `disk_usage_percent`
- `inode_total`, `inode_used`, `inode_free`, `inode_usage_percent`

**알림 기준:**
- Warning: 디스크 사용률 ≥80% 또는 inode ≥80%
- Critical: 디스크 사용률 ≥90% 또는 7일 내 100% 도달 예상

## 메트릭 포맷 (Prometheus 스타일)

모든 메트릭은 다음 라벨링 규칙을 따릅니다:

```
<metric_name>{hostname="<host>",<additional_labels>} <value>
```

**필수 라벨:** `hostname`, `timestamp`
**선택 라벨:** `environment`, `region`, `datacenter`, `role`

예시:
```
cpu_usage_percent{hostname="web-01",core="all"} 45.2
memory_used_bytes{hostname="web-01"} 8589934592
disk_read_bytes_per_sec{hostname="web-01",device="sda"} 10485760
network_bytes_sent_per_sec{hostname="web-01",interface="eth0"} 104857600
```

## 구현 단계

### Phase 1: MVP
- CPU 및 메모리 수집기
- 로컬 파일 기반 저장
- CLI 출력
- 기본 임계값 알림

### Phase 2: 핵심 기능
- 디스크 I/O, 네트워크, 디스크 사용률 수집기 추가
- Prometheus/InfluxDB 통합
- Grafana 대시보드
- 향상된 알림 시스템

### Phase 3: 고급 기능
- 멀티 서버 지원
- 이상 탐지 (Anomaly Detection)
- 트렌드 분석 및 예측
- REST API

## 개발 가이드라인

### 수집기 구현
- 각 수집기는 `src/collectors/`에 독립적인 모듈로 구현
- 수집기는 오류를 우아하게 처리해야 함 (네트워크 장애, 권한 문제 등)
- 블로킹을 방지하기 위해 비동기 수집 사용
- 네트워크 복원력을 위해 로컬 버퍼링 구현
- 에이전트를 중단시키지 않고 수집 실패를 로깅

### 저장소 통합
- 어댑터 패턴을 통한 플러그형 저장소 백엔드 지원
- 데이터 보존 정책 구현 (10초→7일, 1분→30일, 1시간→1년)
- 히스토리 데이터 자동 압축
- 로컬 캐싱으로 저장소 백엔드 장애 처리

### 알림 규칙
- 알림 규칙을 하드코딩하지 않고 설정 파일에 정의
- 여러 알림 채널 지원 (이메일, Slack, PagerDuty)
- 알림 폭주를 방지하기 위한 알림 제한 구현
- 알림에 컨텍스트 포함 (현재 값, 임계값, 히스토리 트렌드)

### 보안
- 모든 메트릭 전송 시 TLS 암호화 사용
- 민감한 정보 마스킹 (프로세스명, 파일 경로)
- 메트릭 조회를 위한 인증 구현
- 모든 접근 시도 로깅

### 테스트
- 각 메트릭 수집기의 정확성 단위 테스트
- 전체 수집 → 저장 → 조회 파이프라인 통합 테스트
- 100대 이상의 시뮬레이션된 서버로 부하 테스트
- 72시간 이상 연속 운영 안정성 테스트

## 일반적인 함정

- **과도한 수집:** 대부분의 메트릭은 10초보다 짧은 간격으로 수집하지 말 것 (디스크 사용률은 60초 가능)
- **리소스 누수:** 파일 핸들, 네트워크 연결, 데이터베이스 세션을 항상 닫을 것
- **라벨 누락:** 모든 메트릭에 hostname과 timestamp 포함 확인
- **알림 피로:** 플래핑 알림을 방지하기 위해 적절한 임계값과 히스테리시스 설정
- **시간대 문제:** 내부적으로 항상 UTC 타임스탬프 사용
- **메트릭 명명:** Prometheus 명명 규칙 준수 (카운터는 `_total`, 크기는 `_bytes` 사용)

## 참고 문서

- 제품 요구사항: `docs/README.md`
- Prometheus Best Practices: https://prometheus.io/docs/practices/naming/
- Google SRE Book - Monitoring: https://sre.google/workbook/monitoring/
- The Four Golden Signals: https://sre.google/sre-book/monitoring-distributed-systems/

## 용어집

- **IOPS**: Input/Output Operations Per Second (초당 입출력 작업 수)
- **MTTR**: Mean Time To Recovery (평균 복구 시간)
- **OOM**: Out Of Memory (Linux 커널 메커니즘)
- **Load Average**: 실행 가능 또는 중단 불가능 상태의 프로세스 수
