# 시스템 리소스 메트릭 수집 시스템 PRD

## 1. 개요

### 1.1 문서 정보
- **문서명**: 시스템 리소스 메트릭 수집 시스템 요구사항 정의서
- **버전**: 1.0
- **작성일**: 2026-02-02
- **상태**: Draft

### 1.2 목적
서버의 핵심 시스템 리소스를 실시간으로 수집, 저장, 모니터링하여 시스템 상태를 효과적으로 파악하고 장애를 사전에 예방하기 위한 메트릭 수집 시스템을 구축한다.

### 1.3 범위
본 시스템은 다음의 5가지 핵심 시스템 리소스 메트릭을 수집한다:
- CPU 사용률
- 메모리 사용량
- 디스크 I/O
- 네트워크 대역폭
- 디스크 사용률

---

## 2. 비즈니스 요구사항

### 2.1 배경
- 서버 장애의 70% 이상이 리소스 부족으로 인해 발생
- 실시간 모니터링 부재로 인한 사후 대응의 한계
- 리소스 사용 추세 분석을 통한 용량 계획 필요

### 2.2 목표
- **정량적 목표**
  - 메트릭 수집 주기: 10초 이하
  - 데이터 손실률: 0.1% 이하
  - 시스템 오버헤드: CPU 5% 이하
  - 데이터 보존 기간: 최소 30일

- **정성적 목표**
  - 운영팀의 시스템 가시성 향상
  - 장애 대응 시간 단축
  - 근거 기반의 용량 계획 수립

### 2.3 성공 지표
- 장애 사전 감지율 80% 이상
- 평균 장애 대응 시간(MTTR) 30% 단축
- 시스템 가용성 99.9% 이상 유지

---

## 3. 기능 요구사항

### 3.1 CPU 메트릭 수집

#### 3.1.1 수집 항목
| 메트릭명 | 설명 | 단위 | 수집 주기 |
|---------|------|------|----------|
| cpu_usage_percent | 전체 CPU 사용률 | % | 10초 |
| cpu_usage_per_core | 코어별 CPU 사용률 | % | 10초 |
| cpu_user_time | User 모드 CPU 시간 | % | 10초 |
| cpu_system_time | System 모드 CPU 시간 | % | 10초 |
| cpu_idle_time | Idle CPU 시간 | % | 10초 |
| cpu_iowait_time | I/O 대기 시간 | % | 10초 |
| load_average_1m | 1분 평균 부하 | - | 10초 |
| load_average_5m | 5분 평균 부하 | - | 10초 |
| load_average_15m | 15분 평균 부하 | - | 10초 |

#### 3.1.2 알림 기준
- CPU 사용률 80% 이상 5분 지속: Warning
- CPU 사용률 95% 이상 1분 지속: Critical
- Load Average > CPU 코어 수 * 2: Warning

### 3.2 메모리 메트릭 수집

#### 3.2.1 수집 항목
| 메트릭명 | 설명 | 단위 | 수집 주기 |
|---------|------|------|----------|
| memory_total | 전체 메모리 용량 | bytes | 10초 |
| memory_used | 사용 중인 메모리 | bytes | 10초 |
| memory_free | 사용 가능한 메모리 | bytes | 10초 |
| memory_available | 실제 가용 메모리 | bytes | 10초 |
| memory_usage_percent | 메모리 사용률 | % | 10초 |
| memory_cached | 캐시된 메모리 | bytes | 10초 |
| memory_buffers | 버퍼 메모리 | bytes | 10초 |
| swap_total | 전체 Swap 용량 | bytes | 10초 |
| swap_used | 사용 중인 Swap | bytes | 10초 |
| swap_free | 사용 가능한 Swap | bytes | 10초 |
| swap_usage_percent | Swap 사용률 | % | 10초 |

#### 3.2.2 알림 기준
- 메모리 사용률 85% 이상: Warning
- 메모리 사용률 95% 이상: Critical
- Swap 사용률 50% 이상: Warning
- OOM Killer 발동: Critical

### 3.3 디스크 I/O 메트릭 수집

#### 3.3.1 수집 항목
| 메트릭명 | 설명 | 단위 | 수집 주기 |
|---------|------|------|----------|
| disk_read_bytes | 디스크 읽기 속도 | bytes/s | 10초 |
| disk_write_bytes | 디스크 쓰기 속도 | bytes/s | 10초 |
| disk_read_ops | 읽기 IOPS | ops/s | 10초 |
| disk_write_ops | 쓰기 IOPS | ops/s | 10초 |
| disk_read_time | 읽기 소요 시간 | ms | 10초 |
| disk_write_time | 쓰기 소요 시간 | ms | 10초 |
| disk_io_util_percent | I/O 사용률 | % | 10초 |
| disk_queue_length | I/O 대기 큐 길이 | - | 10초 |
| disk_await_time | 평균 I/O 대기 시간 | ms | 10초 |

#### 3.3.2 알림 기준
- I/O 사용률 80% 이상 5분 지속: Warning
- I/O 대기 시간 100ms 이상: Warning
- I/O 대기 시간 500ms 이상: Critical

### 3.4 네트워크 대역폭 메트릭 수집

#### 3.4.1 수집 항목
| 메트릭명 | 설명 | 단위 | 수집 주기 |
|---------|------|------|----------|
| network_bytes_sent | 송신 트래픽 | bytes/s | 10초 |
| network_bytes_recv | 수신 트래픽 | bytes/s | 10초 |
| network_packets_sent | 송신 패킷 수 | packets/s | 10초 |
| network_packets_recv | 수신 패킷 수 | packets/s | 10초 |
| network_errors_in | 수신 에러 | errors/s | 10초 |
| network_errors_out | 송신 에러 | errors/s | 10초 |
| network_drops_in | 수신 드롭 | drops/s | 10초 |
| network_drops_out | 송신 드롭 | drops/s | 10초 |
| network_bandwidth_usage | 대역폭 사용률 | % | 10초 |
| network_connections | 활성 연결 수 | - | 10초 |

#### 3.4.2 알림 기준
- 대역폭 사용률 80% 이상: Warning
- 대역폭 사용률 95% 이상: Critical
- 패킷 드롭률 1% 이상: Warning
- 네트워크 에러 발생 시: Warning

### 3.5 디스크 사용률 메트릭 수집

#### 3.5.1 수집 항목
| 메트릭명 | 설명 | 단위 | 수집 주기 |
|---------|------|------|----------|
| disk_total | 전체 디스크 용량 | bytes | 60초 |
| disk_used | 사용 중인 디스크 | bytes | 60초 |
| disk_free | 사용 가능한 디스크 | bytes | 60초 |
| disk_usage_percent | 디스크 사용률 | % | 60초 |
| inode_total | 전체 inode 수 | - | 60초 |
| inode_used | 사용 중인 inode | - | 60초 |
| inode_free | 사용 가능한 inode | - | 60초 |
| inode_usage_percent | inode 사용률 | % | 60초 |

#### 3.5.2 알림 기준
- 디스크 사용률 80% 이상: Warning
- 디스크 사용률 90% 이상: Critical
- inode 사용률 80% 이상: Warning
- 디스크 증가율이 일주일 내 100% 도달 예상: Critical

---

## 4. 기술 요구사항

### 4.1 시스템 아키텍처

```
[서버] → [수집 에이전트] → [메트릭 저장소] → [시각화 대시보드]
                                   ↓
                              [알림 시스템]
```

### 4.2 기술 스택 (권장)

#### 4.2.1 수집 에이전트
- **Python 기반**: psutil, py-cpuinfo 라이브러리 활용
- **Go 기반**: gopsutil, shirou/gopsutil 패키지 활용
- **Node.js 기반**: systeminformation, node-os-utils 모듈 활용
- **기존 솔루션**: Prometheus Node Exporter, Telegraf

#### 4.2.2 메트릭 저장소
- **시계열 DB**: Prometheus, InfluxDB, TimescaleDB
- **보존 정책**:
  - 10초 해상도: 7일
  - 1분 해상도: 30일
  - 1시간 해상도: 1년

#### 4.2.3 시각화
- Grafana
- Kibana
- Custom Dashboard (React + Chart.js)

#### 4.2.4 알림
- Prometheus Alertmanager
- PagerDuty
- Slack/Discord 웹훅

### 4.3 성능 요구사항
- 메트릭 수집 오버헤드: CPU 5% 이하, 메모리 100MB 이하
- 데이터 저장 용량: 서버당 1GB/월 이하 (압축 적용 시)
- 쿼리 응답 시간: 1초 이하 (최근 24시간 데이터)

### 4.4 보안 요구사항
- 메트릭 전송 시 TLS 암호화 적용
- 인증된 클라이언트만 메트릭 조회 가능
- 민감한 정보(프로세스명, 파일 경로 등) 마스킹 처리
- 접근 로그 기록 및 감사

### 4.5 확장성 요구사항
- 최소 1,000대 서버 동시 모니터링 지원
- 수평 확장 가능한 아키텍처
- 멀티 리전 지원

---

## 5. 데이터 모델

### 5.1 메트릭 포맷 (Prometheus 형식 예시)

```
# CPU 메트릭
cpu_usage_percent{hostname="web-01",core="all"} 45.2
cpu_usage_percent{hostname="web-01",core="0"} 52.1
cpu_usage_percent{hostname="web-01",core="1"} 38.3

# 메모리 메트릭
memory_used_bytes{hostname="web-01"} 8589934592
memory_available_bytes{hostname="web-01"} 7516192768

# 디스크 I/O 메트릭
disk_read_bytes_per_sec{hostname="web-01",device="sda"} 10485760
disk_write_bytes_per_sec{hostname="web-01",device="sda"} 5242880

# 네트워크 메트릭
network_bytes_sent_per_sec{hostname="web-01",interface="eth0"} 104857600
network_bytes_recv_per_sec{hostname="web-01",interface="eth0"} 52428800

# 디스크 사용률 메트릭
disk_usage_percent{hostname="web-01",mountpoint="/",device="sda1"} 75.5
```

### 5.2 라벨링 전략
- **필수 라벨**: hostname, timestamp
- **선택 라벨**: environment(prod/staging), region, datacenter, role

---

## 6. 구현 단계

### Phase 1: MVP (4주)
- CPU 및 메모리 메트릭 수집
- 로컬 파일 기반 저장
- 기본 CLI 출력
- 간단한 임계값 알림

### Phase 2: 기본 기능 완성 (6주)
- 디스크 I/O, 네트워크, 디스크 사용률 추가
- Prometheus/InfluxDB 연동
- Grafana 대시보드 구축
- 알림 시스템 고도화

### Phase 3: 고도화 (8주)
- 멀티 서버 지원
- 이상 탐지 (Anomaly Detection)
- 트렌드 분석 및 예측
- API 제공

---

## 7. 테스트 계획

### 7.1 단위 테스트
- 각 메트릭 수집 함수의 정확성 검증
- 에러 핸들링 테스트

### 7.2 통합 테스트
- 수집 → 저장 → 조회 전체 플로우 테스트
- 알림 발생 시나리오 테스트

### 7.3 부하 테스트
- 100대 서버 동시 메트릭 수집 시나리오
- 장기 실행 안정성 테스트 (72시간+)

### 7.4 UAT (User Acceptance Test)
- 운영팀과 함께 실제 환경에서 1주일 파일럿 운영

---

## 8. 운영 및 유지보수

### 8.1 모니터링
- 메트릭 수집 에이전트 자체의 헬스체크
- 데이터 손실률 모니터링
- 저장소 용량 모니터링

### 8.2 백업 및 복구
- 메트릭 데이터 일일 백업 (압축)
- 7일 이내 데이터 복구 가능

### 8.3 문서화
- API 문서 (OpenAPI 3.0)
- 운영 가이드
- 트러블슈팅 가이드

---

## 9. 리스크 및 대응

| 리스크 | 영향도 | 발생 확률 | 대응 방안 |
|--------|--------|-----------|-----------|
| 에이전트 장애로 인한 데이터 손실 | 높음 | 중간 | 에이전트 자동 재시작, 로컬 버퍼링 |
| 저장소 용량 부족 | 높음 | 낮음 | 자동 데이터 압축, 보존 정책 적용 |
| 네트워크 단절 | 중간 | 중간 | 로컬 캐싱, 재전송 메커니즘 |
| 메트릭 수집 오버헤드 | 중간 | 낮음 | 샘플링 주기 조정, 경량화 |

---

## 10. 부록

### 10.1 참고 자료
- Prometheus Best Practices: https://prometheus.io/docs/practices/naming/
- Google SRE Book - Monitoring: https://sre.google/workbook/monitoring/
- The Four Golden Signals: https://sre.google/sre-book/monitoring-distributed-systems/

### 10.2 용어 정의
- **IOPS**: Input/Output Operations Per Second (초당 입출력 작업 수)
- **MTTR**: Mean Time To Recovery (평균 복구 시간)
- **OOM**: Out Of Memory (메모리 부족)
- **Load Average**: 시스템의 평균 작업 부하

### 10.3 변경 이력
| 버전 | 날짜 | 작성자 | 변경 내용 |
|------|------|--------|-----------|
| 1.0 | 2026-02-02 | - | 초안 작성 |
