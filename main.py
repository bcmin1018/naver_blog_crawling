from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()

# HTML 파일 제공
@app.get("/", response_class=HTMLResponse)
async def read_form():
    with open("index.html", "r") as file:
        return file.read()

# CSV 파일 업로드 및 파싱
@app.post("/upload/")
async def upload_csv(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_csv(contents.decode("utf-8"))
    summarized_data = summarize_data(df)
    return summarized_data

def summarize_data(df):
    summarized_data = {}
    current_date = None

    for index, row in df.iterrows():
        date = datetime.strptime(row['Date'], '%Y-%m-%d %H:%M:%S').date()
        user = row['User']
        message = row['Message']

        if current_date != date:
            current_date = date
            if current_date not in summarized_data:
                summarized_data[current_date] = []

        if not is_task_completed(date, user, message):
            summarized_data[current_date].append(message)

    return summarized_data

# 작업이 완료되었는지 확인
def is_task_completed(date, user, message):
    # 여기에 작업이 완료되었는지를 확인하는 로직을 추가해야 합니다.
    # 예를 들어, 데이터베이스에 이미 해당 작업이 완료되었는지를 확인하는 등의 방법을 사용할 수 있습니다.
    return False  # 기본적으로는 작업이 완료되지 않았다고 가정합니다.

# ChatGPT에게 요약된 데이터를 전달하여 응답 받기 위한 추상 메소드
def request_gpt_summary(data):
    # 여기에는 ChatGPT에 요청을 보내는 코드를 작성해야 합니다.
    pass  # 여기서는 추상 메소드로만 남겨둡니다.def summarize_data(df):
    summarized_data = {}
    current_date = None

    for index, row in df.iterrows():
        date = datetime.strptime(row['Date'], '%Y-%m-%d %H:%M:%S').date()
        user = row['User']
        message = row['Message']

        if current_date != date:
            current_date = date
            if current_date not in summarized_data:
                summarized_data[current_date] = []

        if not is_task_completed(date, user, message):
            summarized_data[current_date].append(message)

    return summarized_data

# 작업이 완료되었는지 확인
def is_task_completed(date, user, message):
    # 여기에 작업이 완료되었는지를 확인하는 로직을 추가해야 합니다.
    # 예를 들어, 데이터베이스에 이미 해당 작업이 완료되었는지를 확인하는 등의 방법을 사용할 수 있습니다.
    return False  # 기본적으로는 작업이 완료되지 않았다고 가정합니다.

# ChatGPT에게 요약된 데이터를 전달하여 응답 받기 위한 추상 메소드
def request_gpt_summary(data):
    # 여기에는 ChatGPT에 요청을 보내는 코드를 작성해야 합니다.
    pass  # 여기서는 추상 메소드로만 남겨둡니다.