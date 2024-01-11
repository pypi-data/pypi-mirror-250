import setuptools
import os
import re

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            tem=os.path.join(path, filename)
            tem=re.sub('AnnoSINE/','',tem)
            paths.append(tem)
    return paths

path=package_files("AnnoSINE/Dfam_hmm")
p2=package_files("AnnoSINE/Family_Seq")
p3=package_files("AnnoSINE/Input_Files")
path=path+p2
path=path+p3
#print(path)
#exit()
path.append("TSD_Searcher_multi.js")
path.append("paf2blast6_chunking2_parallel3_ordered_parts.py")
path.append("SINEFinder.py")
#path.append("parameters.yaml")
#path.append("allmeta.tsv")
#path.append("higra.libs/libtbb-d697f7e9.so.2")
#print(path)
#exit()


setuptools.setup(
    name="annosine2",
    version="1.0.5",
    author="Herui Liao, Shujun Ou, and Yang Li",
    author_email="heruiliao2-c@my.cityu.edu.hk",
    description="AnnoSINE_v2 - SINE Annotation Tool for Plant and Animal Genomes",
    long_description="AnnoSINE_v2 is a SINE annotation tool for plant/animal genomes. The program is designed to generate high-quality non-redundant SINE libraries for genome annotation.",
    long_description_content_type="text/markdown",
    url="https://github.com/liaoherui/AnnoSINE_v2",
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=True,
    #package_data={"GDmicro":["feature_select_model_nodirect.R","feature_select_model.R","norm_features.R","parameters.yaml","higra.libs/libtbb-d697f7e9.so.2"]},
    package_data={"AnnoSINE":path},
    install_requires=[
    "cycler",
    "kiwisolver",
    "matplotlib",
    "numpy",
    "Pillow",
    "pyparsing",
    "python-dateutil",
    "six"
    ],
    entry_points={
        'console_scripts':[
        "AnnoSINE_v2 = AnnoSINE.AnnoSINE_v2:main",
        ]
    },
)
