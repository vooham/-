""" streamlit 
굉장히 편하게 인터페이스 제작을 도움.
이미지를 표시, 버튼을 눌렀을 때의 반응.
"""
import streamlit as st
import openai

# key를 감추기 위해 파일(secrets.toml을 만듬)
#openai.api_key = "sk-0sDzORXMEVijzUlltLT3BlbkFJWXGvRn4MFkm55yz7aMJa" -> (키 원본과 다르게 수정했음)

# 만들어둔 파일(secrets.toml)에서 꺼내서 쓴다(키를 노출하지 않아도 된다).
openai.api_key = st.secrets["api_key"]

# 제목
st.title("ChatGPT plus DALL-E!")

# st.text_input("prompt")
# 사용자들이 입력할 수 있는 공간
# ("Prompt")
# 사용자들이 입력할 수 있는 공간의 이름

# st.text_input에서 받은 ("prompt")를 user_input에 저장.
# user_input = st.text_input("prompt")

# 위의 user_input에서 받은 값을 st.write를 이용해서 나타냄.
# st.write(user_input)

# Local URL: http://localhost:8501
# Network URL: http://10.101.85.69:8501 - 같은 네트워크 사용시 같이 이용

# form
# "form" - 큰 따옴표 안에 있는 form은 'key'(고유한 값)다. 
# form이 여러개일 수 있으니 고유 값을 입력한다.
with st.form("form"):
# form 안에 우리가 만든 input을 넣기 위해서 들여쓰기(Tab)를 해서
    #************** form 안에 input을 넣는다.
    user_input = st.text_input("Prompt")
    size = st.selectbox("Size", ["1024x1024", "512x512", "256x256"])
    # submit = 버튼
    submit = st.form_submit_button("Submit")

# ---------- chat gpt에게 명령을 내리는 코드
# submit을 눌렀을 때와 user_input이 들어가 있을 때만 실행히랴.
if submit and user_input:
    # [{ 여기에 gpt한테 명령을 내릴 프롬프트 작성}]
    # [{"role" "system"}] -> 명령을 내리기 위한 역할(시스템 역할) 지정
    gpt_prompt = [{"role": "system",
                   # "입력의 세부적인 모양을 상상해 보십시오."
                   "content": "Imagine the detail appeareance of the input. Response it shortly in 20 words."}]
    
    # ------ 유저들이 입력한 인풋 넣기
    gpt_prompt.append({"role": "user", 
    # user input을 보고 chat gpt가 문장을 내줄 것이다.
        "content": user_input})

    # Submit 버튼을 누른 뒤 진행을 이미지로 표현.
    with st.spinner("Waiting for ChatGPT ..."):
    # openai에 api를 사용.
        gpt_response = openai.ChatCompletion.create(
            # 모델에 gpt 3.5 turbo를 사용
            model="gpt-3.5-turbo",
            # 위에서 작성한 gpt prompt
            messages=gpt_prompt
    )

    # prompt라는 변수에 응답을 저장.
    prompt = gpt_response["choices"][0]["message"]["content"]
    st.write(prompt)

    with st.spinner("Waiting for DALL-E ..."):
        dalle_response = openai.Image.create(
                prompt=prompt,
                size=size
    )

    st.image(dalle_response["data"][0]["url"])