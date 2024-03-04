# Setup environment
conda create --name py310 python=3.10

conda activate py310

pip install numpy pandas matplotlib seaborn streamlit babel

# Run streamlit app
streamlit run dashboard.py

# URL Streamlit
https://bike-sharing-rent-8qdsrawqwvar9gfm3ry2er.streamlit.app/
