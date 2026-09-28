from setuptools import setup

setup(
    name="agrisense-ai-core",
    version="2.0.0",
    description="AgriSense AI - Enterprise Precision Agriculture & Multilingual Voice AI",
    py_modules=["app"],
    entry_points={
        "console_scripts": [
            "streamlit=app:start_server",
        ],
    },
)
