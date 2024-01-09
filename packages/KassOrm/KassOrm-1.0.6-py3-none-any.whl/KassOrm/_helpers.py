from pathlib import Path
import os

def getStub(name:str):   
    """Pega um arquivo stub e retorna se conteudo

    Args:
        name (str): nome do arquivo stub

    Returns:
        str: conteudo do arquivo
    """
    
    dir = os.path.dirname(__file__)
    
    stub = open(Path(f"{dir}/stubs/{name}") ,'r+')
    stub_content = stub.read()
    stub.close()    
    
    return stub_content