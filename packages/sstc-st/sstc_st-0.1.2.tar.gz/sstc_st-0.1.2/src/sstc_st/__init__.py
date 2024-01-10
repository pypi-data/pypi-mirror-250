import streamlit as st
from streamlit.components.v1 import html


def get_sidebar_container_width():
    """
    Get the width of the sidebar container

    Note: 
        This approach relies on the internal structure of Streamlit's HTML, which might change in future versions.

    Usage:
    ```
    # Place your sidebar elements
    with st.sidebar:
        get_container_width()
        # Other sidebar elements

    # Get the width passed from JavaScript
    if 'container_width' not in st.session_state:
        st.session_state.container_width = 300  # Default or initial value

    # Display the width
    st.write(f"Container width: {st.session_state.container_width}")
    ```

    Returns: width of the sidebar container
    """
    js = """
    <script>
    // Get the width of the sidebar container
    var width = document.querySelector('.stSidebar > div').clientWidth;

    // Use Streamlit's set method to pass the width back to Python
    window.parent.postMessage({type: 'streamlit:setComponentValue', value: width}, '*');
    </script>
    """
    html(js)