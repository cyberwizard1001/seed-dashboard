mkdir -p ~/.streamlit/
mkdir data
mkdir -p ~/.streamlit/data

tee ~/.streamlit/config.toml <<EOF
[server]
headless = true
enableCORS=false
port = $PORT
EOF
