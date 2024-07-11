import git
import os

repo_url = 'https://github.com/AxelJrz/pythonRepo'

repo_path = 'C:/Users/ylata/OneDrive/Documentos/pythonRepo'

branch_dest = 'main'  
branch_src = 'axel_branch'  

if not os.path.exists(repo_path):
    repo = git.Repo.clone_from(repo_url, repo_path)
else:
    repo = git.Repo(repo_path)

repo.git.checkout(branch_dest)
repo.remotes.origin.pull(branch_dest)

if branch_src in repo.remotes.origin.refs:
    repo.create_head(branch_src, repo.remotes.origin.refs[branch_src]).set_tracking_branch(repo.remotes.origin.refs[branch_src])
    repo.git.checkout(branch_src)

try:
    repo.git.merge(branch_src)
    print(f"Merge de {branch_src} en {branch_dest} realizado con éxito.")
    repo.git.checkout(branch_dest)
except git.GitCommandError as e:
    print(f"Conflictos durante el merge: {e}")
    repo.git.merge('--abort')
    print("Merge abortado debido a conflictos.")

# Obtén el último commit
commit = repo.head.commit

# Obtén los archivos modificados en el último commit
files = commit.diff('HEAD~1')

with open(os.path.join(repo_path, 'archivos_modificados.txt'), 'w') as f:
    for files_path in files:
        status = ''
        #Se cambio el A por D y viceversa por que al parecer no esta funcionando bien
        if files_path.change_type == 'A':
            status = 'D'
        elif files_path.change_type == 'M':
            status = 'M'
        elif files_path.change_type == 'D':
            status = 'A'
        
        f.write(f"{status} - {files_path.a_path}\n")

print("Lista de archivos modificados guardada en 'archivos_modificados.txt'")

