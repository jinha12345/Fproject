class TokenExpireError(Exception):
    def __init__(self):
        super().__init__('임시 및 appdata 토큰 만료. 파일을 다시 받아주십시오.')