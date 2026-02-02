# 시스템 리소스 메트릭 수집 시스템 - 개발 계획

## Phase 1: MVP (Minimum Viable Product)

### 1.1 프로젝트 초기 설정
- [ ] Python 가상 환경 설정
- [ ] 의존성 패키지 설치 (psutil, prometheus-client, pyyaml, requests)
- [ ] requirements.txt 작성
- [ ] 기본 디렉토리 구조 생성
- [ ] 로깅 시스템 구성

### 1.2 CPU 메트릭 수집기
- [ ] `src/collectors/cpu_collector.py` 구현
  - [ ] cpu_usage_percent (전체 CPU 사용률)
  - [ ] cpu_usage_per_core (코어별 CPU 사용률)
  - [ ] cpu_user_time, cpu_system_time, cpu_idle_time, cpu_iowait_time
  - [ ] load_average_1m, load_average_5m, load_average_15m
- [ ] CPU 수집기 단위 테스트 작성
- [ ] 10초 주기 수집 구현

### 1.3 메모리 메트릭 수집기
- [ ] `src/collectors/memory_collector.py` 구현
  - [ ] memory_total, memory_used, memory_free, memory_available
  - [ ] memory_usage_percent, memory_cached, memory_buffers
  - [ ] swap_total, swap_used, swap_free, swap_usage_percent
- [ ] 메모리 수집기 단위 테스트 작성
- [ ] 10초 주기 수집 구현

### 1.4 로컬 파일 기반 저장소
- [ ] `src/storage/file_storage.py` 구현
- [ ] JSON/CSV 형식으로 메트릭 저장
- [ ] 타임스탬프 기반 파일 로테이션
- [ ] 로컬 버퍼링 구현

### 1.5 CLI 출력
- [ ] `src/cli.py` 구현
- [ ] 실시간 메트릭 출력
- [ ] 포맷팅 및 컬러링
- [ ] 상태 표시 (정상/경고/위험)

### 1.6 기본 알림 시스템
- [ ] `src/alerting/basic_alerting.py` 구현
- [ ] CPU 임계값 알림 (80% Warning, 95% Critical)
- [ ] 메모리 임계값 알림 (85% Warning, 95% Critical)
- [ ] 콘솔 알림 출력
- [ ] 알림 기록 로깅

### 1.7 설정 파일 시스템
- [ ] `config/default.yaml` 작성
- [ ] 수집 주기 설정
- [ ] 임계값 설정
- [ ] 설정 파일 파서 구현

### 1.8 MVP 테스트 및 검증
- [ ] 전체 통합 테스트
- [ ] 성능 요구사항 검증 (CPU 5% 이하, 메모리 100MB 이하)
- [ ] 10초 주기 수집 검증
- [ ] 버그 수정 및 리팩토링

---

## Phase 2: 핵심 기능

### 2.1 디스크 I/O 메트릭 수집기
- [ ] `src/collectors/disk_io_collector.py` 구현
  - [ ] disk_read_bytes, disk_write_bytes (bytes/s)
  - [ ] disk_read_ops, disk_write_ops (IOPS)
  - [ ] disk_read_time, disk_write_time, disk_await_time (ms)
  - [ ] disk_io_util_percent, disk_queue_length
- [ ] 디스크별 메트릭 수집
- [ ] 단위 테스트 작성
- [ ] 알림 규칙 구현 (I/O 사용률 ≥80%, 대기 시간 ≥100ms)

### 2.2 네트워크 메트릭 수집기
- [ ] `src/collectors/network_collector.py` 구현
  - [ ] network_bytes_sent, network_bytes_recv (bytes/s)
  - [ ] network_packets_sent, network_packets_recv (packets/s)
  - [ ] network_errors_in, network_errors_out
  - [ ] network_drops_in, network_drops_out
  - [ ] network_bandwidth_usage (%), network_connections
- [ ] 인터페이스별 메트릭 수집
- [ ] 단위 테스트 작성
- [ ] 알림 규칙 구현 (대역폭 ≥80%, 패킷 드롭률 ≥1%)

### 2.3 디스크 사용률 메트릭 수집기
- [ ] `src/collectors/disk_usage_collector.py` 구현
  - [ ] disk_total, disk_used, disk_free, disk_usage_percent
  - [ ] inode_total, inode_used, inode_free, inode_usage_percent
- [ ] 파티션별 메트릭 수집
- [ ] 60초 주기 수집 구현
- [ ] 단위 테스트 작성
- [ ] 알림 규칙 구현 (디스크 ≥80%, inode ≥80%)

### 2.4 Prometheus 통합
- [ ] `src/storage/prometheus_storage.py` 구현
- [ ] Prometheus exporter 엔드포인트 구현
- [ ] 메트릭 라벨링 (hostname, environment, region 등)
- [ ] Prometheus 명명 규칙 준수
- [ ] Docker Compose로 Prometheus 설정
- [ ] 데이터 보존 정책 설정
- [ ] 통합 테스트

### 2.5 Grafana 대시보드
- [ ] Grafana 설치 및 설정
- [ ] Prometheus 데이터 소스 연결
- [ ] CPU 메트릭 대시보드 생성
- [ ] 메모리 메트릭 대시보드 생성
- [ ] 디스크 I/O 메트릭 대시보드 생성
- [ ] 네트워크 메트릭 대시보드 생성
- [ ] 디스크 사용률 메트릭 대시보드 생성
- [ ] 통합 대시보드 생성
- [ ] 대시보드 JSON 파일 저장 (`dashboards/`)

### 2.6 Prometheus Alertmanager 통합
- [ ] Alertmanager 설치 및 설정
- [ ] 알림 규칙 YAML 파일 작성
- [ ] 이메일 알림 채널 설정
- [ ] Slack 알림 채널 설정
- [ ] 알림 그룹화 및 중복 제거 설정
- [ ] 알림 제한 (rate limiting) 구현
- [ ] 테스트 및 검증

### 2.7 어댑터 패턴으로 저장소 추상화
- [ ] `src/storage/base_storage.py` 인터페이스 정의
- [ ] FileStorage 어댑터 구현
- [ ] PrometheusStorage 어댑터 구현
- [ ] 설정 기반 저장소 선택
- [ ] 단위 테스트 작성

### 2.8 Phase 2 테스트 및 검증
- [ ] 전체 통합 테스트 (5개 수집기)
- [ ] Prometheus + Grafana 통합 테스트
- [ ] 알림 시스템 엔드투엔드 테스트
- [ ] 성능 요구사항 재검증
- [ ] 데이터 손실률 검증 (≤0.1%)
- [ ] 버그 수정 및 최적화

---

## Phase 3: 고급 기능

### 3.1 REST API
- [ ] `src/api/` 구조 설계
- [ ] Flask/FastAPI 프레임워크 선택
- [ ] 메트릭 조회 API 구현
  - [ ] GET /metrics/{hostname}/{metric_name}
  - [ ] GET /metrics/{hostname}/latest
  - [ ] GET /metrics/{hostname}/range?start=&end=
- [ ] 헬스체크 엔드포인트
- [ ] API 인증 구현 (API key/JWT)
- [ ] API 문서 생성 (OpenAPI/Swagger)
- [ ] API 테스트

### 3.2 멀티 서버 지원
- [ ] 서버 등록 시스템 구현
- [ ] 중앙 집중식 메트릭 수집 아키텍처
- [ ] 서버별 메트릭 격리
- [ ] 서버 그룹 관리
- [ ] 멀티 서버 대시보드
- [ ] 부하 테스트 (100대 이상 시뮬레이션)

### 3.3 이상 탐지 (Anomaly Detection)
- [ ] 베이스라인 학습 알고리즘 구현
- [ ] 통계 기반 이상 탐지 (z-score, moving average)
- [ ] 머신러닝 모델 통합 (선택적)
- [ ] 이상 탐지 알림 규칙
- [ ] 이상 탐지 대시보드
- [ ] 정확도 검증

### 3.4 트렌드 분석 및 예측
- [ ] 시계열 분석 구현
- [ ] 리소스 사용량 예측 모델
- [ ] 용량 계획 리포트 생성
- [ ] 예측 기반 알림 (7일 내 100% 도달 예상)
- [ ] 트렌드 시각화

### 3.5 보안 강화
- [ ] TLS 암호화 구현
- [ ] 민감한 정보 마스킹
- [ ] 접근 로깅
- [ ] 보안 감사
- [ ] 취약점 스캔

### 3.6 고급 테스트
- [ ] 72시간 연속 운영 안정성 테스트
- [ ] 장애 복구 테스트
- [ ] 네트워크 단절 시나리오 테스트
- [ ] 저장소 백엔드 장애 시나리오 테스트
- [ ] 메모리 누수 검증
- [ ] 리소스 누수 검증

---

## 추가 작업

### 문서화
- [ ] 설치 가이드 작성
- [ ] 사용자 매뉴얼 작성
- [ ] API 문서 작성
- [ ] 운영 가이드 작성
- [ ] 트러블슈팅 가이드 작성
- [ ] 아키텍처 다이어그램 작성

### 배포
- [ ] Docker 이미지 생성
- [ ] Docker Compose 설정
- [ ] Systemd 서비스 파일 작성
- [ ] 배포 스크립트 작성
- [ ] CI/CD 파이프라인 구성

### 유지보수
- [ ] 모니터링 셋업
- [ ] 백업 전략 수립
- [ ] 업그레이드 절차 문서화
- [ ] 롤백 절차 문서화
