- 아직 미검증된 설치 스크립트
- 한 줄 씩 따로 실행하는 것을 추천
- sudo init.sh로 실행하지 말 것 -> 내부 %USER가 root 계정이 되어 버림
- 메이지웰, docker-compose는 웬만하면 버전 업데이트 되면 그것을 사용할 것
- 우분투 서버에서 실행될 것을 가정함, wifi 와 같은 건 데스크탑 버전에 이미 있음
- 00-installer-config-yaml 은 netplan을 가졍한 파일로, `/etc/netplan/00-installer-config.yaml` 에 옮기면 됨
- 내부의 장비명 eno1, enx201312130040, wlx909f330c4eee (nic1, nic2, wifi1) 은 장비에 맞게 변경 필요
 - `ifconfig -a` 로 알아낼 수 있음
 - wifi도 환경에 맞게 설정