import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import re

#파일에서 Serial Number 값을 추출하고, 이를 기반으로 파일명을 변경하는 함수
def extract_and_rename(file_path):
    try:
        # 파일 열기
        with open(file_path, 'r',encoding='UTF-8') as file:
            content = file.read()
        
        # 정규 표현식 패턴: 'SYSTEM_PROD_DATA.SysInfoSerialNum=' 뒤에 나오는 값을 추출
        pattern = r"SYSTEM_PROD_DATA\.SysInfoSerialNum=(\w+)"
        
        # 정규 표현식으로 값 추출
        match = re.search(pattern, content)
        
        if match:
            # 추출된 Serial Number
            serial_number = match.group(1)
            print(f"추출된 Serial Number: {serial_number}")
            
            # 새로운 파일명 생성
            new_filename = f"{serial_number}.txt"
            
            # 기존 파일 경로에서 디렉토리만 추출
            directory = os.path.dirname(file_path)
            
            # 새로운 파일 경로 생성
            new_file_path = os.path.join(directory, new_filename)
            
            # 파일명 변경
            existing_FileName = f"{directory}/command_output.txt"
            os.rename(existing_FileName, new_file_path)
            print(f"파일명이 '{new_file_path}'로 변경되었습니다.")
        else:
            print("Serial Number를 찾을 수 없습니다.")
    
    except Exception as e:
        print(f"오류 발생: {e}")
        
    return new_file_path


def browse_folder():
    """폴더 탐색기에서 onecli 폴더 경로 선택"""
    folder_path = filedialog.askdirectory()
    if folder_path:
        onecli_folder_entry.delete(0, tk.END)
        onecli_folder_entry.insert(0, folder_path)

def execute_command():
    # 입력값 가져오기
    ip_address = ip_entry.get()
    user_id = id_entry.get()
    password = pw_entry.get()
    onecli_folder = onecli_folder_entry.get()

    # 입력값 유효성 검사
    if not ip_address or not user_id or not password or not onecli_folder:
        messagebox.showerror("Error", "모든 입력값을 채워주세요!")
        return

    # onecli 경로 생성
    onecli_path = os.path.join(onecli_folder, "OneCli.exe")
    if not os.path.isfile(onecli_path):
        messagebox.showerror("Error", "선택한 폴더에 'onecli.exe' 파일이 없습니다!")
        return

    # 명령어 구성
    command1 = f"{onecli_path} config show -b {user_id}:{password}@{ip_address} > {onecli_folder}/tmp.txt"
    command2 = "Select-String -Path {}/tmp.txt -Pattern '(?=.*LogicalPort)(?=.*MACAddress).*|IMM.HostName1' | ForEach-Object {{ ($_ -replace '^.*?:\\d+:', '') }} > {}/command_output.txt".format(onecli_folder, onecli_folder)
    command = "SYSTEM_PROD_DATA.SysInfoSerialNum"
    
    # .bat 파일 생성
    bat_file_path = os.path.join(onecli_folder, "execute_commands.bat")
    with open(bat_file_path, "w", encoding="utf-8") as bat_file:
        bat_file.write(f"""
@echo off
"{onecli_path}" config set BootModes.SystemBootMode "UEFI Mode" -b {user_id}:{password}@{ip_address}
"{onecli_path}" config set BootModes.InfiniteBootRetry "Enable" -b {user_id}:{password}@{ip_address}
"{onecli_path}" config set OperatingModes.ChooseOperatingMode "Maximum Performance" -b {user_id}:{password}@{ip_address}
"{onecli_path}" config set Processors.HyperThreading "Enable" -b {user_id}:{password}@{ip_address}
"{onecli_path}" config set DevicesandIOPorts.PCI64BitResourceAllocation "Disable" -b {user_id}:{password}@{ip_address}
"{onecli_path}" config set BootOrder.BootOrder "Hard Disk=Network" -b {user_id}:{password}@{ip_address}
"{onecli_path}" config set IMM.TimeZone "UTC+9:00" -b {user_id}:{password}@{ip_address}
pause
""")
    try:
        # 명령어 실행 및 결과 가져오기
        result = subprocess.run(command1, shell=True, capture_output=True, text=True)
        result = subprocess.run(["powershell", "-Command", command2], shell=False, capture_output=True, text=True)

        subprocess.Popen(bat_file_path, creationflags=subprocess.CREATE_NEW_CONSOLE)
        
        #output = result.stdout

        # 메모장으로 열기
        
        file_path = f"{onecli_folder}/command_output.txt"
        file_path2 = f"{onecli_folder}/tmp.txt"
        new_file_name = extract_and_rename(file_path2)
        os.startfile(new_file_name)
        
        # 명령어 실행 완료 알림
        messagebox.showinfo("완료", "모든 명령이 성공적으로 실행되었습니다.")

    except Exception as e:
        messagebox.showerror("Error", f"명령어 실행 중 오류 발생: {e}")

# GUI 설정
root = tk.Tk()
root.title("명령 실행 GUI")

# 입력 필드 설정
tk.Label(root, text="IP 주소:").pack(pady=5)
ip_entry = tk.Entry(root, width=50)
ip_entry.pack(pady=5)

tk.Label(root, text="사용자 ID:").pack(pady=5)
id_entry = tk.Entry(root, width=50)
id_entry.pack(pady=5)

tk.Label(root, text="사용자 PW:").pack(pady=5)
pw_entry = tk.Entry(root, width=50, show="*")  # 비밀번호는 입력 시 숨김 처리
pw_entry.pack(pady=5)

tk.Label(root, text="onecli 폴더 경로:").pack(pady=5)
onecli_folder_entry = tk.Entry(root, width=50)
onecli_folder_entry.pack(pady=5)

browse_button = tk.Button(root, text="찾아보기", command=browse_folder)
browse_button.pack(pady=5)

# 실행 버튼
execute_button = tk.Button(root, text="명령 실행", command=execute_command)
execute_button.pack(pady=10)

default_text = (
    "Setting Values \n\n"
    "1. SystemBootMode \"UEFI Mode\"\n"
    "2. InfiniteBootRetry \"Enable\"\n"
    "3. OperatingMode \"Maximum Performance\"\n"
    "4. HyperThreading \"Enable\"\n"
    "5. PCI64BitResourceAllocation \"Disable\"\n"
    "6. BootOrder \"Hard Disk=Network\"\n"
    "7. TimeZone \"UTC+9:00\"\n"
)

# **[변경된 부분]**: 텍스트 위젯 설정
result_text_widget = tk.Text(root, height=10, width=50)  # 텍스트 위젯 추가
result_text_widget.pack(pady=10, padx=10)  # 화면에 배치

# 미리 지정된 텍스트 삽입
result_text_widget.insert(tk.END, default_text)

# GUI 실행
root.mainloop()