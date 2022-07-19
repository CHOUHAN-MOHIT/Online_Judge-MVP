import subprocess

expout = open('exp_out.txt' , 'r')
inputfile = open('input.txt' , 'r')
generated_output = open('output.txt' , 'w')

subprocess.run(['g++' , 'temp.cpp' , '-o' , 'temp'])
subprocess.call(['temp.exe'],stdin=inputfile ,stdout=generated_output,shell=True)