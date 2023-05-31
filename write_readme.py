def write_readme(readme):
    with open('README.md', 'w') as f:
        f.write(readme)


if __name__=='__main__':
    readme="""
    # Project logo or icon \n![Project Logo](./logo.png)\n\n# Introduction \nThis project is an AI model that analyzes photos and provides a classification of the theme. Currently, it can classify photos into the following categories: 'childlike', 'christmas', 'city', 'dragonboat', 'east_building', 'excting_sport', 'food', 'inhome', 'leisure_sport', 'nature', 'night', 'pet', 'portrait', 'shop', 'snow', 'spring', 'transport', 'west_building'\n\n# Changelog\n<!-- Optional section. Include any significant changes, enhancements, or bug fixes that have been made to the project. If there have been no changes since the last release, omit this section. -->\n\n# Get Started \n## Prerequisites \nThe code has been tested on Python 3.8 or above. There are no other version requirements. The following packages need to be installed:\n\n```\npip install numpy\npip install torch\npip install torchvision\npip install opencv-python\npip install onnx\npip install onnxruntime\n# Optionally\npip install gradio\n```\n\n## Usage \nTo run the code, execute the following command:\n\n```\npython onnx_infer.py\n```\n\nThis will output the list of all supported categories, the confidence score for each category, and the final predicted label (ordered).\n\n# Contact or Citation \nAuthor: Shao-Hong Chen\nEmail: 611699999@qq.com\n\n# Contribute \n<!-- Optional section. Describe how other developers can contribute to the project. Include information on how to file bugs, request features, or submit pull requests. If contributions are not accepted, this section can be omitted. -->\n\n# License \nThe project is licensed under the GPL-3.0 License.1
    """

    write_readme(readme)