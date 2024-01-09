def format_price(input_number):
    # 숫자를 문자열로 변환하고 뒤집기
    reversed_str = str(input_number)[::-1]

    # 세 자리마다 쉼표 추가
    formatted_str = ",".join([reversed_str[i:i+3] for i in range(0, len(reversed_str), 3)])

    # 다시 뒤집기
    result_str = formatted_str[::-1]

    # ₩ 기호와 함께 반환
    return f"₩{result_str}"