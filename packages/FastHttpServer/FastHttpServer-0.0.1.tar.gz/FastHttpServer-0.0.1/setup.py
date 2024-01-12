import setuptools 

with open("README.md", "r") as fh: 
	description = fh.read() 

setuptools.setup( 
	name="FastHttpServer", 
	version="0.0.1", 
	author="Mulham Alamry", 
	author_email="mulhamreacts@gmail.com", 
	packages=["FastHttpServer"], 
	description="An extremely lightweight and fast http server", 
	long_description=description, 
	long_description_content_type="text/markdown", 
	url="https://github.com/D4r3d3vil/FastHttp", 
	license='MIT', 
	python_requires='>=3.0', 
	install_requires=[] 
) 
