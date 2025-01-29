# Bios-setting-tool
OneCLI와 Python을 활용하여 BIOS 설정을 자동화하는 도구입니다.

## 1. 프로젝트 개요
기존 방식에서는 납품된 270대의 서버에 대해 엔지니어가 일일이 노트북이나 콘솔로 접속한 후, BIOS 설정 화면에서 수작업으로 설정을 변경해야 했습니다.
이 과정은 업무 효율성이 낮고, 휴먼 에러가 발생할 가능성이 높다는 문제점이 있었습니다.

이러한 불편함을 해결하기 위해, Lenovo에서 제공하는 OneCLI 툴을 활용하면 명령어(Command) 기반으로 BIOS 설정을 변경할 수 있다는 점을 알게 되었습니다.
그러나 이 방식 역시 개별적으로 명령어를 입력해야 하므로 여전히 수작업의 한계가 존재했습니다.

이를 자동화하기 위해 Python과 OneCLI를 결합한 BIOS 설정 자동화 도구를 개발하였으며,
사용자가 코드를 이해할 필요 없이 쉽게 활용할 수 있도록 GUI 기반의 툴로 제작하였습니다.

하나의 서버 설정에 약 5분 정도가 소요되며,
허브 또는 스위치를 통해 여러 서버에 동시에 접근할 경우, 엔지니어의 업무 효율성이 더욱 향상됩니다.

## 2. 주요 기능
이 프로젝트는 OneCLI와 Python을 활용하여 Lenovo 서버의 BIOS 설정을 자동화하는 GUI 기반의 도구입니다. 주요 기능은 다음과 같습니다.

✅ BIOS 설정 자동화   
기존의 수작업 방식 대신 OneCLI 명령어를 활용하여 BIOS 설정을 일괄적으로 적용
SystemBootMode, HyperThreading, OperatingMode 등 다양한 설정을 자동으로 변경


✅ GUI 기반 사용 편의성   
Tkinter를 이용한 간단한 GUI 제공
사용자 입력(서버 IP, 계정 정보, OneCLI 폴더 경로) 후 버튼 클릭만으로 설정 가능


✅ 서버 정보 조회 및 저장   
OneCLI를 이용해 서버의 현재 설정값을 조회 후 저장
서버의 Serial Number를 자동으로 추출하여 파일명을 변경


✅ PowerShell 명령어 자동 실행   
Select-String을 사용하여 특정 패턴을 검색하고 결과를 정리
PowerShell과 Windows Batch 파일을 생성 및 실행하여 명령어 자동화


✅ 로그 저장 및 설정 파일 관리   
서버 설정 결과를 .txt 파일로 저장하여 확인 가능
자동으로 파일명을 변경하여 서버별 설정 관리 가능

## 3. 기술 스택
Python: GUI 및 OneCLI 명령 실행 자동화   

Tkinter: GUI 기반 사용자 인터페이스 제공   

OneCLI (Lenovo 서버 툴): 서버의 BIOS 설정값을 조회하고 변경하는 역할   

PowerShell: 서버에서 특정 설정을 검색하여 파일로 저장   

Batch Script (.bat 파일): 여러 개의 OneCLI 명령어를 실행하여 BIOS 설정 변경   


## 4. 설치 및 실행 방법
1️⃣ 필수 요구사항
Windows 환경   
Python 3.x 설치   
OneCLI (Lenovo에서 제공) 설치   
PowerShell 사용 가능   

2️⃣ 프로젝트 다운로드
git clone https://github.com/ImOkay-Ms/bios-setting-tool.git
cd bios-setting-tool

3️⃣ Python 패키지 설치
pip install tk

4️⃣ OneCLI 다운로드 및 폴더 경로 확인
https://support.lenovo.com/kr/ko/solutions/ht116433-lenovo-xclarity-essentials-onecli-onecli
lnvgy_utl_lxce_onecli01z-4.2.0_winsrv_x86-64 version 압축 해제 후 OneCLI 실행 파일 (OneCli.exe) 경로 확인

5️⃣ 프로그램 실행
python main.py

6️⃣ 사용 방법
GUI에서 IP 주소, 사용자 ID, 비밀번호, OneCLI 경로 입력   
"찾아보기" 버튼을 눌러 OneCLI 폴더 선택   
"명령 실행" 버튼 클릭   
자동으로 BIOS 설정이 변경되고, 결과 파일(command_output.txt)이 생성됨   
command_output.txt가 Serial Number 기반의 파일명으로 자동 변경됨   

+ 실행파일로 만들고 싶다면 pyinstaller --onefile /경로/python main.py 실행

## 5. 발전 가능성 및 향후 개선점
FWDeviceOrder 설정 오류 해결   
현재 FWDeviceOrder 설정 시 "General Failure" 오류가 발생하여 적용되지 않는 문제가 있음.   
Lenovo 측에 문의 결과 Onecli 혹은 Server F/W version을 확인하라는 답변을 받음 해당 내용 참고하여 최신버전으로 업그레이드 한 후 테스트 진행 예정임.   
RAID 설정 자동화   
RAID 설정의 경우, 컨트롤러 종류 및 디스크 개수가 서버마다 달라 현재 자동화에서 제외됨.   
향후,특정 모델별 RAID 설정을 지원하는 기능을 추가하면 더 범용적인 도구가 될 것으로 기대됨.

## 6. 참고 자료
https://pubs.lenovo.com/lxce-onecli/onecli_bk.pdf   
https://pcsupport.lenovo.com/us/en/warranty-lookup#/   
