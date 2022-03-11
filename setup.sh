mkdir -p ~/.streamlit/

tee ~/.streamlit/config.toml <<EOF
[server]
headless = true
enableCORS=false
port = $PORT
EOF
