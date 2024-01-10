from setuptools import setup
from setuptools.command.install import install
import subprocess

class CustomInstallCommand(install):
    def run(self):
       # Esegui il comando per scaricare il modello spaCy
      subprocess.run(['py', '-m', 'spacy', 'download', 'it_core_news_lg'])
      # Chiamare l'implementazione originale della classe padre per eseguire l'installazione normale
      super().run()

setup(
    name='anon_testo',
    version='0.0.20',    
    description='Anonimizzatore di documenti GateNLP',
    url='https://github.com/RafVale/anon_testo',
    author='Raffaele Valendino',
    author_email='raffaele.valendino@gmail.com',
    license='MIT',
    packages=['anon_testo'],
    install_requires=['spacy >= 3.7.2',
                    'presidio-analyzer >= 2.2.351',
                    'presidio-anonymizer >= 2.2.351',
                      ],
    cmdclass={
       'install': CustomInstallCommand,
    },
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: Microsoft :: Windows :: Windows 10',        
        'Programming Language :: Python :: 3.10',
    ],
)
