import os
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _custom_grid_plot = components.declare_component(
        
        "custom_grid_plot", 
        
        url="http://localhost:3001",
    )
else:
    
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _custom_grid_plot = components.declare_component("custom_grid_plot", path=build_dir)

def custom_grid_plot(damageType=None, styles=None, default=None, key=None):
    
    component_value = _custom_grid_plot(damageType=damageType, styles=styles, key=key, default=default)

    return component_value
