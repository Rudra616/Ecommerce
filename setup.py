from setuptools import setup, find_packages

setup(
    name="project",  # ✅ Change to match your actual package name
    version="0.1.0",
    description="My Django Project",
    author="Panchal Rudra M",
    author_email="your-email@example.com",
    packages=find_packages(),  # ✅ This should now correctly find "project"
    include_package_data=True,
    install_requires=[
        "Django>=5.1.6",
        "gunicorn>=23.0.0",
        "python-dotenv>=1.0.1",
        "pillow>=11.1.0",
        "requests>=2.32.3",
        "sqlparse>=0.5.3",
    ],
)
