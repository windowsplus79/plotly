import subprocess
import time
from datetime import datetime

def git_commit_push():
    try:
        # 현재 시간을 커밋 메시지에 포함
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_message = f"Auto commit at {current_time}"
        
        # 변경사항 추가
        subprocess.run(['git', 'add', '.'], check=True)
        
        # 커밋
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        # 푸시
        subprocess.run(['git', 'push', 'origin', 'master'], check=True)
        
        print(f"Successfully committed and pushed at {current_time}")
        
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    while True:
        git_commit_push()
        # 1시간(3600초) 대기
        time.sleep(3600) 