import streamlit as st
import os
import requests


def call_api(endpoint, method, params={}, body={}):
    url = f"http://127.0.0.1:8000{endpoint}"
    if method == "get":
        response = requests.get(url, params=params)
    elif method == "post":
        response = requests.post(url, params=params, json=body)
    else:
        raise Exception(f"Method {method} not supported")
    return response


def load_api_schema():
    response = call_api("/openapi.json", "get", {})
    if response.status_code == 200:
        return response.json()
    else:
        return {}


def update_state():
    if "logs" not in st.session_state:
        st.session_state.logs = ""
    path = os.getcwd()
    logs_file = path + "/example_mls/logs.json"
    if os.path.exists(logs_file):
        with open(logs_file, "r") as f:
            logs = f.read()
            st.session_state.logs = logs


st.title("MLbull Dashboard")
st.write(
    "This is a dashboard for MLbull. It will display the logs from the MLbull app."
)
st.write("You can also use it to test the MLbull app.")
st.write(
    "If you want to see the logs from the MLbull app, but you use API click the button below."
)

if st.button("Show logs"):
    update_state()

if "logs" not in st.session_state:
    st.session_state.logs = ""

if "logs" in st.session_state:
    st.text_area(label="Output Data:", value=st.session_state.logs, height=350)

api_schema = load_api_schema()

if st.button("Refresh api schema"):
    api_schema = load_api_schema()

endpoints = {}
for path, methods in api_schema["paths"].items():
    for method in methods:
        endpoints[f"{method.upper()} {path}"] = (path, method)

st.subheader("Here you can test API")
st.write("You can use the dropdown below to test the MLbull app.")
st.write("Select the function you want to test and fill in the parameters.")
st.write(
    "Then click the button below to run the function and see the response."
)

selected_endpoint = st.selectbox("Select API Function", list(endpoints.keys()))

user_params = {}
user_body = {}
if selected_endpoint:
    path, method = endpoints[selected_endpoint]
    params = api_schema["paths"][path].get(method, {}).get("parameters", [])
    requestBody = (
        api_schema["paths"][path].get(method, {}).get("requestBody", {})
    )
    if params:
        for param in params:
            required = param.get("required", False)
            user_params[param["name"]] = st.text_input(
                param["name"],
                "",
                key=param["name"],
                placeholder="Required" if required else "Optional",
            )
    if requestBody:
        content = requestBody["content"]
        for content_type, content_data in content.items():
            schema = content_data["schema"]
            user_body[schema["title"]] = st.text_input(
                schema["title"], "", key=schema["title"]
            )


if st.button("Run Function"):
    response = call_api(path, method, user_params, user_body)
    if response:
        try:
            st.write("Response:")
            st.write(response.json())
        except:
            st.write("Response is not JSON, displaying raw response:")
            st.write(response.text)
    else:
        st.write("No response from API")
        st.write(response.text)
        st.write("response status code: ", response.status_code)
        st.warning("Please check the logs for more information.")
