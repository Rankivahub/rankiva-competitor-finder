import streamlit as st
from theme.styles import apply_theme
from components.logo import render_logo
from components.modal import render_analysis_modal

apply_theme()
render_logo()
render_analysis_modal()
