import streamlit as st
from theme.styles import apply_theme
from components.logo import render_logo
from components.modal import render_analysis_modal

# UI Setup
apply_theme()
render_logo()

# Main Content
render_analysis_modal()
