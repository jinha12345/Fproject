import os
import sys
# 리소스에 대한 절대경로 가져오기 (개발환경과 pyinstaller 에서 작동한다)
def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)