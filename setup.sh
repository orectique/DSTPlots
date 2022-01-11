mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
[theme]\n\
primaryColor=\"#c0d6df\"\n\
backgroundColor=\"#eaeaea\"\n\
secondaryBackgroundColor=\"#F0F2F6\"\n\
textColor=\"#262730\"\n\
font=\"sans serif\"\n\
" > ~/.streamlit/config.toml