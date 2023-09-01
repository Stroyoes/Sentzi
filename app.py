import streamlit as st

from lib.ui import set_init_state, reset_results, sidebar

# set the init values
set_init_state()

# create sidebar
sidebar()

st.write('# `Sentzi`')

st.divider()

st.write("## Let's begin ! ")
