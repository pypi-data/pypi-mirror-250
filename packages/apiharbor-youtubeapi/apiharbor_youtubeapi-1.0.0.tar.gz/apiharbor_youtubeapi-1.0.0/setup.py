from setuptools import setup, find_packages

setup(
    name='apiharbor_youtubeapi',
    version='1.0.0',
    author='apiharbor',
    author_email='apiharborcom@gmail.com',
    description='Want to dive deeper into the YouTube scene? Our YouTube Channel Details API is just what you need, especially if you\'re a marketer, researcher, or content creator. It\'s not just about getting contact info; it\'s about discovering those little gems like social media and location details of YouTube channels. Imagine the possibilities - like when one of our users found the perfect collaboration opportunity just by using these insights!',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://rapidapi.com/dataocean/api/the-better-youtube-channel-details',
    packages=find_packages(),
    install_requires=[
		'aiohttp',
		'purl'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
	keywords=[
        "youtube",
        "api",
        "youtube-api",
        "channel-details",
        "youtube-data",
        "youtube-analytics",
        "contact-information",
        "social-media-analysis",
        "youtube-marketing",
        "content-creation",
        "influencer-research",
        "video-analytics",
        "youtube-content",
        "media-analysis",
        "digital-marketing"
    ],
    python_requires='>=3.6'
)