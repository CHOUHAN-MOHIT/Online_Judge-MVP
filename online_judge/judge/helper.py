import subprocess
import docker

def get_verdict(codefile , inputfile):
    client = docker.from_env()
    containers = client.containers.list()
    if containers:
        container = containers[0]
        if container.status == 'running':
            codedest = container.id + ':code.cpp'
            filedest = container.id + ':input.txt'
            outfile = container.id + ':output.txt'
            inputfile = 'media/' + inputfile
            subprocess.run(['docker' , 'cp', codefile , codedest])
            subprocess.run(['docker' , 'cp', inputfile , filedest])
            subprocess.run(['docker' , 'exec' , container.id , 'g++' , 'code.cpp' , '-o' , 'code'])
            subprocess.run(['docker' , 'exec' , container.id ,'sh', '-c', './code < input.txt > output.txt'])
            subprocess.run(['docker' , 'cp', outfile , 'output.txt'])
            return 0
        
    else:
        container = client.containers.run('gcc' , detach=True , tty=True)
        status = container.status
        codedest = container.id + ':code.cpp'
        filedest = container.id + ':input.txt'
        outfile = container.id + ':output.txt'
        inputfile = 'media/' + inputfile
        subprocess.run(['docker' , 'cp', codefile , codedest])
        subprocess.run(['docker' , 'cp', inputfile , filedest])
        subprocess.run(['docker' , 'exec' , container.id , 'g++' , 'code.cpp' , '-o' , 'code'])
        subprocess.run(['docker' , 'exec' , container.id ,'sh', '-c', './code < input.txt > output.txt'])
        subprocess.run(['docker' , 'cp', outfile , 'output.txt'])
        return 12
